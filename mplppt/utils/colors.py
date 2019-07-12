#############
## Imports ##
#############

from .constants import MPLCOLORS

#####################
## Color Functions ##
#####################


def rgb2hex(tup, max=1):
    tup = [int(c * 255 / max) for c in tup]
    color = ""
    for c in tup:
        if c < 16:
            c = "0" + hex(c)[-1:]
        else:
            c = hex(c)[-2:]
        color += c
    return color.upper()


def rgba2hex(tup, max=1, keep_alpha=True):
    alpha = tup[-1]
    color = rgb2hex(tup[:-1])
    if keep_alpha:
        return color, alpha
    else:
        return color


def color2hex(color):
    if type(color) is str:
        if len(color) == 6:
            return color
        elif len(color) == 7 and color[0] == "#":
            return color[1:]
        elif color in MPLCOLORS:
            return MPLCOLORS[color]
    else:
        if type(color) is int:
            return rgb2hex((color, color, color), max=255)
        if type(color) is float:
            return rgb2hex((color, color, color))
        if len(color) == 4:
            return rgba2hex(color)
        if len(color) == 3:
            return rgb2hex(color)
        if len(color) == 2:
            return color
    raise ValueError("invalid color " + str(color))
