# Python Module to convert to sRGB

# Function to convert non linear-srgb value to linear srb
def linearsrgbtolinear(nlsrgb):
    lsrgb = []
    for nlvalue in nlsrgb:
        if nlvalue < 0.0031308:
            lvalue = nlvalue * 12.92
            lsrgb.append(lvalue)
        else:
            lvalue = 1.055 * nlvalue ** (1 / 2.4) - 0.055
            lsrgb.append(lvalue)
    return lsrgb
