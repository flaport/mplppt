""" matplotlib figure tools """


#############
## Imports ##
#############

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from .strings import random_name


###############
## CONSTANTS ##
###############

visualized = {}


###############
## Functions ##
###############


def get_plotting_area(fig):
    """ get area which is visualized by matplotlib

    Args:
        fig: matplotlib figure to find the area for
    
    Returns:
        xmin, xmax, ymin, ymax: the bounds of the matplotlib figure
    """
    global visualized
    if fig not in visualized:
        # HACK: To get info about spine locations, the axis needs to be visualized first.
        # We choose png export:
        fn = random_name() + ".png"
        plt.savefig(fn)
        os.remove(fn)
        visualized[fig] = True
    spines = plt.findobj(fig, mpl.spines.Spine)
    bboxes = [np.array(spine.get_extents()) for spine in spines]
    xmin = np.min([np.min(bbox[:, 0]) for bbox in bboxes])
    xmax = np.max([np.max(bbox[:, 0]) for bbox in bboxes])
    ymin = np.min([np.min(bbox[:, 1]) for bbox in bboxes])
    ymax = np.max([np.max(bbox[:, 1]) for bbox in bboxes])
    return xmin, xmax, ymin, ymax
