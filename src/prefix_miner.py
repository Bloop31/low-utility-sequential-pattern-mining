from src.utility_engine import compute_pattern_utility_fast
from src.feature_extractor import extract_features
from config import ML_THRESHOLD


def mine_lusp(prefix, items, utility_db, results,
              min_util, max_len, vertical_db,
              ml_model=None, use_ml=False):

    # -------------------------
    # 🔹 STOP CONDITIONS
    # -------------------------
    if len(prefix) > max_len:
        return

    for item in items:

        # avoid permutations
        if prefix and item < prefix[-1]:
            continue

        new_pattern = prefix + [item]

        # avoid patterns like [a,a,a]
        if len(new_pattern) >= 2 and new_pattern.count(new_pattern[0]) == len(new_pattern):
            continue

        # -------------------------
        # 🔥 BASIC PRUNING
        # -------------------------
        if item not in vertical_db:
            continue

        if len(vertical_db[item]["sids"]) < 2:
            continue

        # -------------------------
        # 🔥 PATTERN PRUNING
        # -------------------------
        sid_sets = [vertical_db[i]["sids"] for i in new_pattern if i in vertical_db]

        if not sid_sets:
            continue

        sids = min(sid_sets, key=len).copy()

        for s in sid_sets:
            if s is not sids:
                sids &= s
                if not sids:
                    break

        if len(sids) < 2:
            continue

        # -------------------------
        # 🔥 ML PRUNING
        # -------------------------
        if use_ml and ml_model and len(new_pattern) >= 3:
            try:
                features = extract_features(new_pattern, vertical_db)
                prob = ml_model.predict_proba(features)

                if prob < ML_THRESHOLD:
                    continue
            except:
                pass

        # -------------------------
        # 🔥 UTILITY COMPUTATION
        # -------------------------
        util = compute_pattern_utility_fast(
            new_pattern,
            vertical_db,
            utility_db
        )

        # -------------------------
        # 🔥 LUSPM CONDITION
        # -------------------------
        if util <= min_util:
            results.append((tuple(new_pattern), util))
        else:
            continue

        # early pruning
        if util > min_util * 2:
            continue

        # -------------------------
        # 🔥 RECURSION
        # -------------------------
        mine_lusp(
            new_pattern,
            items,
            utility_db,
            results,
            min_util,
            max_len,
            vertical_db,
            ml_model,
            use_ml
        )