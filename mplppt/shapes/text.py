""" Powerpoint text representations """


#############
## Imports ##
#############

import numpy as np
from scipy.interpolate import interp1d

from .base import Object
from ..templates import TEXT
from ..templates import RECTANGLE
from ..utils.colors import color2hex
from ..utils.strings import random_name
from ..utils.constants import ALIGNMENTS
from ..utils.constants import POINTSPERINCH
from ..utils.constants import PIXELSPERPOINT
from ..utils.mpl import get_plotting_area


##########
## Text ##
##########


class Text(Object):
    """ A text box """

    def __init__(
        self,
        text="",
        x=0,
        y=0,
        cx=None,
        cy=None,
        size=18,
        font="Arial",
        color="000000",
        ha="c",
        va="c",
        slidesize=(6, 4),
    ):
        """ create a text box in powerpoint

        Args:
            text: str: the text to place in a powerpoint textbox
            x: the x-location of the textbox
            y: the y-location of the textbox
            cx: the x-width of the textbox
            cy: the y-height of the textbox
            size: the fontsize of the text in the textbox
            font: the font of the text in the textbox
            color: the color of the text in the textbox
            ha: the horizontal alignment of the text in the textbox
            va: the vertical alignment of the text in the textbox
            slidesize: the size of the slide to place the textbox into
        """
        Object.__init__(self, name="", slidesize=slidesize)
        self.text = text
        self._x = x
        self._y = y
        self.cx = cx
        self.cy = cy
        self.ha = ALIGNMENTS[ha]
        self.va = ALIGNMENTS[va]
        self.size = size
        self.color = color
        self.font = font
        self._xml = RECTANGLE.replace("</p:sp>", "\n" + TEXT + "\n</p:sp>\n")

    @property
    def x(self):
        """ get the effective x-location of the text adjusted for its horizontal alignment """
        if self.ha == "c":
            return self._x - 0.5 * self.cx
        if self.ha == "r":
            return self._x - self.cx
        return self._x

    @property
    def y(self):
        """ get the effective y-location of the text, adjusted for its vertical alignment """
        if self.va == "c":
            return self._y - 0.5 * self.cy
        if self.va == "b":
            return self._y - self.cy
        return self._y

    @classmethod
    def from_mpl(cls, mpl_text):
        """ Create a text box starting from a matplotlib Text object

        Args:
            mpl_text: the matplotlib text to convert into powerpoint text.
        
        """

        # TODO: The code below gets repeated a lot over the different shapes.
        #       Create a method in the Object class that extrapolates the
        #       x and y values.

        # Get slidesize from matplotlib figure
        slidesize = (mpl_text.figure.get_figwidth(), mpl_text.figure.get_figheight())
        f = cls._mpl_shrink_factor

        # Get plotting area
        slide_x0, slide_x1, slide_y1, slide_y0 = get_plotting_area(mpl_text.figure)

        # Translate text location data to locations on slide
        plot_x0, plot_x1 = mpl_text.axes.get_xlim()
        plot_y0, plot_y1 = mpl_text.axes.get_ylim()

        x = interp1d(
            [plot_x0, plot_x1], [slide_x0, slide_x1], fill_value="extrapolate"
        )(mpl_text._x)
        y = interp1d(
            [plot_y0, plot_y1], [slide_y0, slide_y1], fill_value="extrapolate"
        )(mpl_text._y)

        # HACK: If an object is partly outside the plotting area, we map the values outside to the
        # margin area (over which the (white?) rectangles of the Canvas will later be drawn)
        # TODO: Implement this

        # If object is completely outside plotting area, then we shouldnt show it at all:
        # TODO: Implement this check

        # Get texbox size
        bbox = np.array(
            mpl_text.get_window_extent(renderer=mpl_text.figure.canvas.get_renderer())
        )
        cx, cy = 1.1 * (bbox[1] - bbox[0])

        # Create Textbox
        text = cls(
            text=mpl_text._text,
            x=x,
            y=y,
            cx=abs(cx),
            cy=abs(cy),
            size=mpl_text.get_fontsize(),
            font=mpl_text.get_fontname(),
            color=mpl_text.get_color(),
            ha=mpl_text._horizontalalignment,
            va=mpl_text._verticalalignment,
            slidesize=slidesize,
        )

        return text

    def xml(self):
        """ Get xml representation of the text 
        
        Returns:
            xml: str: the xml representation of the text
        """
        if self.text.replace(" ", "").replace("\n", "") == "":
            return ""  # Return empty string, if no characters are written

        # Get width and height of textbox
        cx = self.cx
        if cx is None:
            cx = self.size * max([len(line) for line in self.text.splitlines()])
        cy = self.cy
        if cy is None:
            cy = self.size + 2

        # Return xml representation
        xml = self._xml.format(
            text=self.text,
            size=int(self.size * 100),
            color=color2hex(self.color),
            font=self.font,
            name=self.text.splitlines()[0],
            x=int(self.x * PIXELSPERPOINT) + 1,
            y=int(self.y * PIXELSPERPOINT) + 1,
            cx=int(cx * PIXELSPERPOINT),
            cy=int(cy * PIXELSPERPOINT),
            lw=int(0.2 * PIXELSPERPOINT),
            colorspec=self.colorspec(None),
            bgcolorspec=self.colorspec(None),
        )
        return xml
