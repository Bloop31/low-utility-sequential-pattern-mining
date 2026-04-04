from multiprocessing import Pool
from src.prefix_miner import mine_lusp
from config import N_WORKERS


def worker(args):
    item = args[0]
    items = args[1]
    utility_db = args[2]
    min_util = args[3]
    max_len = args[4]
    vertical_db = args[5]
    model = args[6]
    use_ml = args[7]

    results = []

    mine_lusp(
        [item],
        items,
        utility_db,
        results,
        min_util,
        max_len,
        vertical_db,
        model,
        use_ml
    )

    return results


def run_parallel(vertical_db, utility_db, min_util, max_len,
                 ml_model=None, use_ml=False):

    items = list(vertical_db.keys())

    args = [
        (item, items, utility_db, min_util, max_len, vertical_db, ml_model, use_ml)
        for item in items
    ]

    with Pool(N_WORKERS) as p:
        outputs = p.map(worker, args)

    results = []
    for out in outputs:
        results.extend(out)

    return results