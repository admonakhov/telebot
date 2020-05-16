def mean(arg):
    return round(sum(arg) / len(arg), 2)


def sko(arg):
    m = mean(arg)
    lsum = 0
    for n in arg:
        lsum += (n - m) ** 2
    return round((lsum / (len(arg) - 1)) ** 0.5, 2)


def cv(arg):
    return round(100 * sko(arg) / mean(arg), 2)


def median(arg):
    tmp = sorted(arg)
    if len(tmp) % 2 == 0:
        return (tmp[int(len(tmp) / 2)] + tmp[int(len(tmp) / 2) - 1]) / 2
    else:
        return tmp[int(len(tmp) / 2)]
