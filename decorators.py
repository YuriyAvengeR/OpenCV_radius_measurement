def text_size(r):
    if r < 100:
        return 0.5, 1
    else:
        return 0.9, 2


def size_checker(y, r, x):
    if r < 100:
        if r >= 38:
            y = (y - r) - (r * 0.2)
            x = x - r
            return y, x
        elif r < 20:
            y = (y - r) - (r * 0.4)
            x = (x - r) - (x * 0.04)
            return y, x
        else:
            y = y - (y * 0.01)
            return y, x
    elif r < 20:
        y = (y - r) - (r * 0.4)
        x = (x - r) - (x * 0.04)
        return y, x
    else:
        y = y - (y * 0.01)
        return y, x

