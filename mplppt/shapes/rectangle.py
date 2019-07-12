""" Powerpoint rectangle representation """


#############
## Imports ##
#############

from .base import Object
from ..templates import RECTANGLE
from ..utils.colors import color2hex
from ..utils.strings import random_name
from ..utils.constants import POINTSPERINCH
from ..utils.constants import PIXELSPERPOINT
from ..utils.mpl import get_plotting_area


###############
## Rectangle ##
###############


class Rectangle(Object):
    """ A rectangle """

    def __init__(
        self,
        name="Rect",
        x=0,
        y=0,
        cx=100,
        cy=50,
        lw=1,
        ec="000000",
        fc="eeeeee",
        slidesize=(6, 4),
    ):
        """ Create a powerpoint rectangle

        Args:
            name: the xml-name for the rectangle
            x=0: the x-location of the rectangle
            y=0: the y-location of the rectangle
            cx=0: the width of the rectangle
            cy=0: the height of the rectangle
            lw: the linewidth to draw the rectangle in
            ec: the edgecolor to draw the rectangle in
            fc: the facecolor to draw the rectangle in
            slidesize=(6,8): the slidesize to put the rectangle in
        """
        Object.__init__(self, name=name, slidesize=slidesize)
        self.x = x
        self.y = y
        self.cx = cx
        self.cy = cy
        self.lw = lw
        self.ec = ec
        self.fc = fc
        self._xml = RECTANGLE

    @classmethod
    def from_mpl(cls, mpl_rect):
        """ Create a rectangle starting from a matplotlib Rectangle object

        Args:
            mpl_rect: the matplotlib rectangle to convert to a powerpoint rectangle
        """

        # TODO: The code below gets repeated a lot over the different shapes.
        #       Create a method in the Object class that extrapolates the
        #       x and y values.

        # Get slidesize from matplotlib figure
        slidesize = (mpl_rect.figure.get_figwidth(), mpl_rect.figure.get_figheight())

        # Get plotting area
        slide_x0, slide_x1, slide_y1, slide_y0 = get_plotting_area(mpl_rect.figure)

        rx, ry = mpl_rect.xy

        # Translate plot data to locations on slide
        plot_x0, plot_x1 = mpl_rect.axes.get_xlim()
        mx = (slide_x0 - slide_x1) / (plot_x0 - plot_x1)
        x = mx * (rx - plot_x0) + slide_x0
        cx = mx * mpl_rect._width
        if cx < 0:
            x += cx
            cx *= -1

        plot_y0, plot_y1 = mpl_rect.axes.get_ylim()
        my = (slide_y0 - slide_y1) / (plot_y0 - plot_y1)
        y = my * (ry - plot_y0) + slide_y0
        cy = my * mpl_rect._height
        if cy < 0:
            y += cy
            cy *= -1

        # HACK: If an object is partly outside the plotting area, we map the values outside to the
        # margin area (over which the (white?) rectangles of the Canvas will later be drawn)
        # TODO: Implement this

        # If object is completely outside plotting area, then we shouldnt show it at all:
        # TODO: Implement this check

        # Create Rectangle
        rect = cls(
            name="mplrect_" + random_name(5),
            x=x,
            y=y,
            cx=cx,
            cy=cy,
            lw=mpl_rect._linewidth,
            ec=color2hex(mpl_rect._edgecolor),
            fc=color2hex(mpl_rect._facecolor),
            slidesize=slidesize,
        )
        return rect

    def xml(self):
        """ Get xml representation of the rectangle """
        xml = self._xml.format(
            name=self.name,
            x=int(self.x * PIXELSPERPOINT) + 1,
            y=int(self.y * PIXELSPERPOINT) + 1,
            cx=int(self.cx * PIXELSPERPOINT),
            cy=int(self.cy * PIXELSPERPOINT),
            lw=int(self.lw * PIXELSPERPOINT),
            colorspec=self.colorspec(self.ec),
            bgcolorspec=self.colorspec(self.fc),
        )
        return xml
