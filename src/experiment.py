from src.data_loader import load_spmf
from src.utility_generator import generate_utility_db
from src.vertical_db import build_vertical_db
from src.parallel_mining import run_parallel
from src.metrics import start_metrics, end_metrics
from src.ml_pruner import MLPruner
from src.feature_extractor import extract_features

import random
import time


def run_experiment(dataset, min_util, max_len):

    print("\n========== LOADING ==========")

    start_total = time.time()

    # ---------------- LOAD ----------------
    seq_db = load_spmf(dataset)

    # 🔥 LIMIT DATA EARLY (IMPORTANT)
    if len(seq_db) > 10000:
        seq_db = seq_db[:10000]

    utility_db, _ = generate_utility_db(seq_db)

    # ---------------- BUILD VERTICAL ----------------
    vertical = build_vertical_db(utility_db)

    # ---------------- TOTAL UTILITY ----------------
    total_util = 0
    for _, seq in utility_db:
        for _, util in seq:
            total_util += util

    min_util_abs = int(min_util * total_util)

    print("Total Utility:", total_util)
    print("Min Util (abs):", min_util_abs)

    # ---------------- ML TRAIN ----------------
    print("\n========== ML TRAIN ==========")

    random.seed(42)  # 🔥 reproducibility

    sample_size = min(300, len(utility_db))
    samples = random.sample(utility_db, sample_size)

    X, y = [], []

    for _, seq in samples:
        pattern = [item for item, _ in seq[:3]]
        utils = [sum(u for _, u in seq[:3]) for _, seq in samples]

        threshold = sorted(utils)[len(utils)//2]   # median

        for _, seq in samples:
            pattern = [item for item, _ in seq[:3]]
            util = sum(u for _, u in seq[:3])

            features = extract_features(pattern, vertical)
            X.append(features)

            if util <= threshold:
                y.append(1)
            else:
                y.append(0)

    # ---------------- ML MODEL ----------------
    if len(set(y)) < 2:
        print("⚠️ Only one class found → disabling ML")
        model = None
        use_ml = False
    else:
        model = MLPruner()
        model.train(X, y)
        use_ml = True

    # ---------------- FILTER ITEMS ----------------
    # 🔥 FIXED: use sids length
    vertical = dict(
        sorted(
            vertical.items(),
            key=lambda x: len(x[1]["sids"]),
            reverse=True
        )[:30]   # keep top 30 items
    )

    # ---------------- MINING ----------------
    print("\n========== MINING ==========")

    st, sm = start_metrics()

    mining_start = time.time()

    patterns = run_parallel(
        vertical,
        utility_db,
        min_util_abs,
        max_len,
        ml_model=model,
        use_ml=use_ml
    )

    mining_end = time.time()

    runtime, mem = end_metrics(st, sm)

    total_time = time.time() - start_total

    # ---------------- RESULTS ----------------
    print("\nPatterns:", len(patterns))
    print("Mining Runtime:", round(mining_end - mining_start, 3))
    print("Total Runtime:", round(total_time, 3))
    print("Memory:", round(mem, 2))