# Python Module to convert to sRGB
def linearsrgbtolinear(rnl):
    if rnl < 0.0031308:
        rl = rnl * 12.92
    else:
        rl = 1.055 * rnl ** (1 / 2.4) - 0.055
    return rl