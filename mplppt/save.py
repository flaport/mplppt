#############
## Imports ##
#############

import os
import matplotlib as mpl
from matplotlib.pyplot import gcf
from matplotlib.pyplot import findobj

from .shapes import Line
from .shapes import Text
from .shapes import Mesh
from .shapes import Spine
from .shapes import Group
from .shapes import Canvas
from .shapes import Polygon
from .shapes import Rectangle
from .utils.strings import random_name


########################
## The Magic Function ##
########################

# This is the function this repository is all about

def savefig(filename, fig=None, axis=True):
    """ Export a matplotlib figure to a pptx file 
    
    Args:
        filename: str: the filename of the pptx file to save the matplotlib figure as
        fig: the figure to convert to a pptx slide. If None, plt.gcf() will be used to get the most recent figure.
        axis=True: wether to show the axis ticks and labels or not.
    
    Returns:
        group: the mplppt group containing all the objects that were converted from the matplotlib figure.
    """
    # Get figure to save
    if fig is None:
        fig = gcf()

    # Create ppt group
    p = Group(objects=[])

    # Parse mpl objects:
    for obj in findobj(fig):
        # only keep objects that have an axis:
        if obj.axes is not None:
            # convert lines:
            if isinstance(obj, mpl.lines.Line2D):
                p += Line.from_mpl(obj)
            # convert rectangles:
            if isinstance(obj, mpl.patches.Rectangle):
                p += Rectangle.from_mpl(obj)
            # convert polygons
            if isinstance(obj, mpl.patches.Polygon):
                p += Polygon.from_mpl(obj)
            # convert text
            if isinstance(obj, mpl.text.Text):
                p += Text.from_mpl(obj)
            # convert pcolormesh
            if isinstance(obj, mpl.collections.QuadMesh):
                p += Mesh.from_mpl(obj)

    # create a canvas
    # TODO: Create this with less parameters
    canvas = Canvas.from_mpl(fig.axes[0], axis=axis)
    p += canvas

    # save powerpoint group
    p.save(filename)

    # return powerpoint group
    return p


############################
## Other Useful Functions ##
############################

import pickle


def picklefig(filename, fig):
    with open(filename, "wb") as file:
        pickle.dump((fig, fig.canvas), file)


def loadpicklefig(filename):
    with open(filename, "rb") as file:
        try:
            fig, canvas = pickle.load(file, encoding="latin1")
        except TypeError:
            fig, canvas = pickle.load(file)
    fig.canvas = canvas
    return fig
