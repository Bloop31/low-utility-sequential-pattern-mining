def compute_pattern_utility_fast(pattern, vertical_db, utility_db):
    if not pattern:
        return 0

    # Precompute sid lists (no repeated set creation)
    sid_lists = []
    for item in pattern:
        if item not in vertical_db:
            return 0
        sid_lists.append(vertical_db[item]["sids"])

    # Fast intersection
    sids = set(sid_lists[0])
    for s in sid_lists[1:]:
        sids &= s

    if not sids:
        return 0

    total_util = 0

    # Only compute on filtered sequences
    for sid in sids:
        seq = utility_db[sid][1]

        # INLINE DP (avoid calling slow function)
        m = len(pattern)
        dp_cnt = [1] + [0] * m
        dp_util = [0] * (m + 1)

        for item, util in seq:
            for k in range(m - 1, -1, -1):
                if item == pattern[k]:
                    dp_cnt[k+1] += dp_cnt[k]
                    dp_util[k+1] += dp_util[k] + dp_cnt[k] * util

        total_util += dp_util[m]

    return total_util