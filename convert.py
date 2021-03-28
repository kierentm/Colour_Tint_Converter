# Python Module to convert to sRGB

# Function to convert linear-srgb value to SRGB8
def LSRGBtoSRGB8(lsrgb):
    rgb_list = []
    for nlvalue in lsrgb:
        if nlvalue < 0.0031308:
            # Converts SRGB Linear to SRGB Non-Linear
            lvalue = nlvalue * 12.92
            # Converts Non-Linear SRGB to SRGB8 and ints
            value8 = int(256 * lvalue)
            rgb_list.append(value8)
        else:
            lvalue = 1.055 * nlvalue ** (1 / 2.4) - 0.055
            value8 = int(256 * lvalue)
            rgb_list.append(value8)
    # Returns int tuple for entry into webcolor function
    return tuple(rgb_list)


# Tests if correct input is entered and returns false if incorrect
def KierensStupidTest(value):
    if not value == "":
        if not value == ".":
            try:
                if not 0 <= float(value) <= 1:
                    return False
                else:
                    return True
            except ValueError:
                return False
        else:
            return True
    else:
        return True


# Converts SRGB8 values from colour picker to SRBG
def RGBtoNLSRGB(rgbt):
    lsrgb_list = []
    for rbg_val in rgbt:
        nlsrgb = rbg_val / 255
        if nlsrgb < 0.04045:
            lsrgb = nlsrgb / 12.92
            lsrgb_list.append(lsrgb)
        else:
            lsrgb = ((nlsrgb + 0.055) / 1.055) ** 2.4
            lsrgb_list.append(lsrgb)
    return tuple(lsrgb_list)

# If greater than 1 return 1
def ifgreaterthan1(value):
    if value > 0:
        return 1
    else:
        return value