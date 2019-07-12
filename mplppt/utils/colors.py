""" color conversions """

#############
## Imports ##
#############

from .constants import MPLCOLORS

#####################
## Color Functions ##
#####################


def rgb2hex(tup, max=1):
    """ convert an rgb tuple into a hex color string representation

    Args:
        tup: tuple: tuple of length 3 representing the color
        max=1: the maximum value for the values in the tuple.
            This will be used to scale the tuple values as integers between 0 and 255.
    
    Returns:
        color: str: hex color string representation (format "aaaaaa" - no "#")
    """
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
    """ convert an rgba tuple into a hex color string representation and a transparency value (alpha value)

    Args:
        tup: tuple: tuple of length 4 representing the color and a transparency
        max=1: the maximum value for the values in the tuple.
            This will be used to scale the tuple values as integers between 0 and 255.
        keep_alpha=True: wether to keep the transparency or not.
    
    Returns:
        color: tuple: (hex color representation, alpha)
     OR color: str: hex color representation [if keep_alpha=False]
    """
    alpha = tup[-1]
    color = rgb2hex(tup[:-1])
    if keep_alpha:
        return color, alpha
    else:
        return color


def color2hex(color):
    """ Convert any kind of color representation to a hex string color representation 
    
    Args:
        color: any kind of color representation (hex string, tuple)
    
    Returns:
        color: hex string representation for the color (format "aaaaaa" - no "#")
    """
    if isinstance(color, str):
        if len(color) == 6:
            return color
        elif len(color) == 7 and color[0] == "#":
            return color[1:]
        elif color in MPLCOLORS:
            return MPLCOLORS[color]
    else:
        if isinstance(color, int):
            return rgb2hex((color, color, color), max=255)
        if isinstance(color, float):
            return rgb2hex((color, color, color))
        if len(color) == 4:
            return rgba2hex(color)
        if len(color) == 3:
            return rgb2hex(color)
        if len(color) == 2:
            return color
    raise ValueError("invalid color " + str(color))
