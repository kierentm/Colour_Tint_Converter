# Python Module to convert to sRGB

# ------------- Functions for converting linear SRGB (SRGB[0,1]) -------------

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

# Converts SRGB8 values from colour picker to SRBG
def RGB8toLSRGB(rgbt):
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

# ------------- Functions for converting non-linear SRGB (SRGB'[0,1]) -------------

# Converts non-linear SRGB to SRGB8
def NLSRGBtoSRGB8(nlsrgb):
    return tuple([int(256 * nl) for nl in nlsrgb])

# Converts SRGB8 to non-linear SRGB
def RGB8toNLSRGB(srgb8):
    return tuple([rgb / 255 for rgb in srgb8])

# ------------- Tests to confirm entries are as expected or warn/adjust as required -------------

# If greater than 1 return 1 (useful in print)
def ifgreaterthan1(value, conv_type):
    # Converts value over 1 to 1 to make printing make more sense and returns 0 for non numerical ones
    if not conv_type == "sRGB8 [0,255]":
        if 1.0 < value:
            return 1.0
        elif 0.0 <= value < 1.0:
            return value
        else:
            return 0.0
    # Converts value over 255 to 255 to make printing make more sense and returns 0 for non numerical ones
    else:
        if 255 < value:
            return 255
        elif 0 <= value < 255:
            return int(value)
        else:
            return 0

# Tests if correct input is entered and returns false if incorrect, this allows for box to display red
def KierensStupidTest(value, conv_type):
    if not conv_type == "sRGB8 [0,255]":
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
    else:
        if not value == "":
            try:
                if not 0 <= int(value) <= 255:
                    return False
                else:
                    return True
            except ValueError:
                return False
        else:
            return True

# Conversion for calculation to float or int and returns 0 if error
def get_entries_convert(get_entries, conv_type):
    converted_get_entries = []
    if conv_type == 'sRGB8 [0,255]':
        for entry in get_entries:
            try:
                int_entry = int(entry)
            except ValueError:
                int_entry = 0
            converted_get_entries.append(int_entry)
    else:
        for entry in get_entries:
            try:
                flt_entry = float(entry)
            except ValueError:
                flt_entry = 0.0
            converted_get_entries.append(flt_entry)
    return tuple(converted_get_entries)


# Warning to confirm if functions file was run independently
def main():
    print("Have you run the correct file?")


if __name__ == "__main__":
    main()