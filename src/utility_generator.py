import random

def generate_utility_db(seq_db, seed=42):
    random.seed(seed)

    ext_util = {}
    utility_db = []

    # External utility
    for _, seq in seq_db:
        for item in seq:
            if item not in ext_util:
                ext_util[item] = random.randint(1, 10)

    # Internal utility
    for sid, seq in seq_db:
        new_seq = []
        for item in seq:
            internal = random.randint(1, 5)
            new_seq.append((item, internal * ext_util[item]))
        utility_db.append((sid, new_seq))

    return utility_db, ext_util