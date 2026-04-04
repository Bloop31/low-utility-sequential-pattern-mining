feature_cache = {}

def extract_features(sequence, vertical_db):
    key = tuple(sequence)

    if key in feature_cache:
        return feature_cache[key]

    length = len(sequence)

    try:
        sid_sets = [vertical_db[item]["sids"]
                    for item in sequence if item in vertical_db]

        support = len(set.intersection(*sid_sets)) if sid_sets else 0
    except:
        support = 0

    freq = sum(len(vertical_db.get(item, {}).get("data", []))
               for item in sequence)

    diversity = len(set(sequence))

    result = [
        length,
        support,
        freq,
        diversity,
        freq / (length + 1),
        support / (length + 1)
    ]

    feature_cache[key] = result   # 🔥 YOU MISSED THIS

    return result