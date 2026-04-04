def load_spmf(path):
    db = []
    sid = 0

    with open(path) as f:
        for line in f:
            tokens = line.strip().split()
            seq = []

            for t in tokens:
                if t in ('-1', '-2'):
                    continue

                if t.startswith("SUtility"):
                    continue

                if '[' in t:
                    item = int(t.split('[')[0])
                else:
                    item = int(t)

                seq.append(item)

            if seq:
                db.append((sid, seq))
                sid += 1

    return db