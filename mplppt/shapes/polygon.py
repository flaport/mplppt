""" Powerpoint polygon representation """


#############
## Imports ##
#############

import numpy as np
from scipy.interpolate import interp1d

from .line import Line
from ..utils.colors import color2hex
from ..utils.strings import random_name
from ..utils.constants import POINTSPERINCH
from ..utils.constants import PIXELSPERPOINT
from ..utils.mpl import get_plotting_area


#############
## Polygon ##
#############


class Polygon(Line):
    """ A polygon. """

    def __init__(
        self,
        name="Polygon",
        shape=[(0, 0), (0, 100), (50, 0)],
        ec="000000",
        fc="eeeeee",
        slidesize=(6, 4),
    ):
        """ A Polygon is nothing more than a Line which is always closed. 
    
        Args:
            name: the xml name of the polygon
            shape: the shape of the polygon: a list of tuples
            lw: the linewidth to draw the polygon in
            ec: the edgecolor to draw the polygon in
            fc: the facecolor to draw the polygon in
            slidesize=(6,4): the slidesize in which to embed the polygon.
        
        """
        Line.__init__(
            self, name=name, shape=shape, ec=ec, fc=fc, closed=True, slidesize=slidesize
        )

    @classmethod
    def from_mpl(cls, mpl_poly):
        """ Create a polygon starting from a matplotlib Polygon object

        Args:
            mpl_poly: the matplotlib polygon to convert into a ppt polygon
        """

        #TODO: The code below gets repeated a lot over the different shapes.
        #      Create a method in the Object class that extrapolates the
        #      x and y values.

        # Get slidesize from matplotlib figure
        slidesize = (mpl_poly.figure.get_figwidth(), mpl_poly.figure.get_figheight())

        # Get plotting area
        slide_x0, slide_x1, slide_y1, slide_y0 = get_plotting_area(mpl_poly.figure)

        # Translate plot data to locations on slide
        plot_x0, plot_x1 = mpl_poly.axes.get_xlim()
        plot_y0, plot_y1 = mpl_poly.axes.get_ylim()

        mx = (slide_x1 - slide_x0) / (plot_x1 - plot_x0)
        sx = 0.5 * slide_x0
        px = sx / mx

        my = (slide_y1 - slide_y0) / (plot_y1 - plot_y0)
        sy = 0.5 * slide_y0
        py = sy / my

        x, y = mpl_poly._get_xy().T

        x = interp1d(
            [plot_x0, plot_x1], [slide_x0, slide_x1], fill_value="extrapolate"
        )(x)
        y = interp1d(
            [plot_y0, plot_y1], [slide_y0, slide_y1], fill_value="extrapolate"
        )(y)

        # HACK: If an object is partly outside the plotting area, we map the values outside to the
        # margin area (over which the (white?) rectangles of the Canvas will later be drawn)
        x[x < 0.5 * slide_x0] = 0.5 * slide_x0
        x[x > slide_x1 + 0.5 * slide_x0] = slide_x1 + 0.5 * slide_x0
        y[y < 0.5 * slide_y1] = 0.5 * slide_y1
        y[y > slide_y0 + 0.5 * slide_y1] = slide_y0 + 0.5 * slide_y1

        shape = np.stack((x, y), axis=1)

        # If object is completely outside plotting area, then we shouldnt show it at all:
        if ((y < slide_y1) | (y > slide_y0) | (x < slide_x0) | (x > slide_x1)).all():
            return None

        # Create Line
        poly = cls(
            name="mplpolygon_" + random_name(5),
            shape=shape,
            ec=color2hex(mpl_poly._edgecolor),
            fc=None if not mpl_poly.fill else color2hex(mpl_poly._facecolor),
            slidesize=slidesize,
        )

        return poly
