""" Powerpoint line representations """


#############
## Imports ##
#############

import numpy as np
from scipy.interpolate import interp1d

from .base import Object
from ..templates import LINE
from ..utils.colors import color2hex
from ..utils.strings import random_name
from ..utils.constants import POINTSPERINCH
from ..utils.constants import PIXELSPERPOINT
from ..utils.mpl import get_plotting_area


##########
## Line ##
##########


class Line(Object):
    """ A Line """

    def __init__(
        self,
        name="Line",
        shape=[(0, 0), (0, 100), (50, 0)],
        lw=1,
        ec="000000",
        fc=None,
        closed=False,
        slidesize=(6, 4),
    ):
        """ Create a line in powerpoint

        Args:
            name: the xml name of the line
            shape: the shape of the line: a list of tuples
            lw: the linewidth to draw the line in
            ec: the edgecolor to draw the line in
            fc: the facecolor to draw the line in
            closed: wether to close the line or not (connect the last point with the first point of the line)
            slidesize=(6,4): the slidesize in which to embed the line.
        """
        Object.__init__(self, name=name, slidesize=slidesize)
        self.shape = np.array(shape)
        self.lw = lw
        self.ec = ec
        self.fc = fc
        self.closed = closed
        self._xml = LINE

    @property
    def x(self):
        """ X location of the upper left corner of the shape """
        return np.min(self.shape, axis=0)[0]

    @property
    def y(self):
        """ Y location of the upper left corner of the shape """
        return np.min(self.shape, axis=0)[1]

    @property
    def cx(self):
        """ Total width of the shape """
        return (np.max(self.shape, axis=0) - np.min(self.shape, axis=0))[0]

    @property
    def cy(self):
        """ Total height of the shape """
        return (np.max(self.shape, axis=0) - np.min(self.shape, axis=0))[1]

    def get_adjusted_shape(self):
        """ To draw a resize box around the shape, we need to give the coordinates of the
        shape relative to the the upper left corner of the shape

        Returns:
            shape: list: the shape of the line relative to the upper left corner
        """
        shape = self.shape.copy()
        shape[:, 0] -= self.x
        shape[:, 1] -= self.y
        return shape

    @classmethod
    def from_mpl(cls, mpl_line):
        """ Create a line starting from a matplotlib Line2D object

        Args:
            mpl_line: the matplotlib line to convert into a ppt line
        """

        # TODO: The code below gets repeated a lot over the different shapes.
        #      Create a method in the Object class that extrapolates the
        #      x and y values.

        # Get slidesize from matplotlib figure
        slidesize = (mpl_line.figure.get_figwidth(), mpl_line.figure.get_figheight())

        # Get plotting area
        slide_x0, slide_x1, slide_y1, slide_y0 = get_plotting_area(mpl_line.figure)

        # Translate plot data to locations on slide
        plot_x0, plot_x1 = mpl_line.axes.get_xlim()
        plot_y0, plot_y1 = mpl_line.axes.get_ylim()

        mx = (slide_x1 - slide_x0) / (plot_x1 - plot_x0)
        sx = 0.5 * slide_x0
        px = sx / mx

        my = (slide_y1 - slide_y0) / (plot_y1 - plot_y0)
        sy = 0.5 * slide_y0
        py = sy / my

        x = interp1d(
            [plot_x0, plot_x1], [slide_x0, slide_x1], fill_value="extrapolate"
        )(mpl_line._x)
        y = interp1d(
            [plot_y0, plot_y1], [slide_y0, slide_y1], fill_value="extrapolate"
        )(mpl_line._y)

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
        line = cls(
            name="mplline_" + random_name(5),
            shape=shape,
            lw=mpl_line._linewidth,
            ec=color2hex(mpl_line.get_color()),
            fc=None,
            closed=False,
            slidesize=slidesize,
        )
        return line

    def xml(self):
        """ Get the xml representation of the whole object containing the line 
        
        Returns:
            xml: str: the xml representation of the whole object containing the line
        """
        xml = self._xml.format(
            name=self.name,
            x=int(self.x * PIXELSPERPOINT) + 1,
            y=int(self.y * PIXELSPERPOINT) + 1,
            cx=int(self.cx * PIXELSPERPOINT),
            cy=int(self.cy * PIXELSPERPOINT),
            lw=int(self.lw * PIXELSPERPOINT),
            shapespec=self.shapespec(self.get_adjusted_shape(), self.closed),
            colorspec=self.colorspec(self.ec),
            bgcolorspec=self.colorspec(self.fc),
        )
        return xml

    def shapespec(self, shape, closed):
        """ Get the xml representation of just the line. """
        # check if shape is empty
        if len(shape) == 0:
            return ""

        # first point in shape
        shapespec = '<a:moveTo><a:pt x="{x}" y="{y}"/></a:moveTo>\n'.format(
            x=int(shape[0][0] * PIXELSPERPOINT), y=int(shape[0][1] * PIXELSPERPOINT)
        )

        # other points in shape
        for x, y in shape[1:]:
            shapespec = shapespec + '<a:lnTo><a:pt x="{x}" y="{y}"/></a:lnTo>\n'.format(
                x=int(x * PIXELSPERPOINT), y=int(y * PIXELSPERPOINT)
            )

        # close shape
        if closed:
            shapespec = shapespec + "<a:close/>\n"

        return shapespec
