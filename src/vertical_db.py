def build_vertical_db(utility_db):
    vertical = {}

    for sid, seq in utility_db:
        for pos, (item, util) in enumerate(seq):
            if item not in vertical:
                vertical[item] = {
                    "data": [],
                    "sids": set()
                }

            vertical[item]["data"].append((sid, pos, util))
            vertical[item]["sids"].add(sid)

    return vertical