import webcolors

from utility_functions import *
from configparser import ConfigParser

# Load Config and generate main if required
config = ConfigParser()
config.read('config.ini')


def conversion():
    # Dictionary to return
    colour_types = {"sRGB8 [0,255]": [0, 0, 0], "sRGB' [0,1]": [0, 0, 0], "sRGB [0,1]": [0, 0, 0]}
    # ---- Find current colour type from settings ---- #
    conversion_type = c_type
    # ---- Fetch values ---- #
    values = entry

    # If given "sRGB8 [0,255]"
    if conversion_type == "sRGB8 [0,255]":
        # -- Store sRGB8 [0,255]
        colour_types["sRGB8 [0,255]"] = values
        # -- Convert to sRGB' [0,1]
        colour_types["sRGB' [0,1]"] = RGB8toNLSRGB(values)
        # -- Convert to SRGB [0,1]
        colour_types["sRGB [0,1]"] = RGB8toLSRGB(values)

    # If given "sRGB' [0,1]"
    if conversion_type == "sRGB' [0,1]":
        # -- Store "sRGB' [0,1]"
        colour_types["sRGB' [0,1]"] = values
        # -- Convert to sRGB8 [0,1]
        colour_types["sRGB8 [0,255]"] = NLSRGBtoSRGB8(values)
        # -- Convert to SRGB [0,1]
        colour_types["sRGB [0,1]"] = RGB8toLSRGB(NLSRGBtoSRGB8(values))

    # If given "sRGB [0,1]"
    if conversion_type == "sRGB [0,1]":
        # -- Store "sRGB [0,1]"
        colour_types["sRGB [0,1]"] = values
        # -- Convert to "sRGB8 [0,255]"
        colour_types["sRGB8 [0,255]"] = LSRGBtoSRGB8(values)
        # -- Convert to SRGB' [0,1]
        colour_types["sRGB [0,1]"] = RGB8toNLSRGB(LSRGBtoSRGB8(values))

    return colour_types


def update():
    pass


c_type = "sRGB' [0,1]"

entry = [0.5, 0.5, 0.5]


conversion()
