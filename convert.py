# Python Module to convert to sRGB

# Function to convert non linear-srgb value to linear srb
def nonlinearsrgbtolinear(nlsrgb):
    lsrgb = []
    for nlvalue in nlsrgb:
        if nlvalue < 0.0031308:
            # Converts SRGB Linear to SRGB Non-Linear
            lvalue = nlvalue * 12.92
            # Converts Non-Linear SRGB to SRGB8 and ints
            value8 = int(255 * lvalue)
            lsrgb.append(value8)
        else:
            lvalue = 1.055 * nlvalue ** (1 / 2.4) - 0.055
            value8 = int(255 * lvalue)
            lsrgb.append(value8)
    # Returns int tuple for entry into webcolor function
    return tuple(lsrgb)
