import numpy as np
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


def regression(x, y):
    cor = {}
    m_x = mean(x)
    m_y = mean(y)
    s_y = sko(y)
    s_x = sko(x)
    cor['cov'] = 0
    for i in range(len(x)):
        cor['cov'] += (x[i] - m_x) * (y[i] - m_y)
    cor['cov'] /= (len(x) - 1)
    cor['regression'] = cor['cov'] / (s_y * s_x)
    cor['slope'] = (s_y / s_x) * (cor['regression'])
    cor['intercept'] = m_y + np.abs(cor['slope'] * m_x)

    return cor
