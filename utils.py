def uniq(values):
    d = {}
    result = []
    for v in values:
        if v in d:
            continue
        d[v] = 1
        result.append(v)
    return result
