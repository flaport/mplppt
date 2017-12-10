#############
## Imports ##
#############

from .base import Object
from ..templates import RECTANGLE
from ..utils.colors import color2hex
from ..utils.string import random_name
from ..utils.constants import POINTSPERINCH
from ..utils.constants import PIXELSPERPOINT


###############
## Rectangle ##
###############

class Rectangle(Object):
    ''' A rectangle '''
    def __init__(self, name='Rect', x=0, y=0, cx=100, cy=50, lw=1, ec='000000', fc='eeeeee', slidesize=(6,4)):
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
        slidesize = (mpl_rect.figure.get_figwidth(), mpl_rect.figure.get_figheight())
        f = cls._mpl_shrink_factor

        slide_x0 = 0.5*(1-f)*slidesize[0]
        slide_x1 = slide_x0 + f*slidesize[0]
        plot_x0, plot_x1 = mpl_rect.axes.get_xlim()
        mx = (slide_x0-slide_x1)/(plot_x0 - plot_x1)
        x = mx*(mpl_rect._x-plot_x0) + slide_x0
        cx = mx*mpl_rect._width
        if cx < 0:
            x += cx
            cx *= -1

        slide_y1 = 0.5*(1-f)*slidesize[1]
        slide_y0 = slide_y1+f*slidesize[1]
        plot_y0, plot_y1 = mpl_rect.axes.get_ylim()
        my = (slide_y0-slide_y1)/(plot_y0 - plot_y1)
        y = my*(mpl_rect._y-plot_y0) + slide_y0
        cy = my*mpl_rect._height
        if cy < 0:
            y += cy
            cy*=-1

        rect = cls(
            name='mplrect_' + random_name(5),
            x=x*POINTSPERINCH,
            y=y*POINTSPERINCH,
            cx=cx*POINTSPERINCH,
            cy=cy*POINTSPERINCH,
            lw = mpl_rect._linewidth,
            ec = color2hex(mpl_rect._edgecolor),
            fc = color2hex(mpl_rect._facecolor),
            slidesize = slidesize,
        )
        return rect

    def xml(self):
        xml = self._xml.format(
            name = self.name,
            x  = int(self.x*PIXELSPERPOINT)+1,
            y  = int(self.y*PIXELSPERPOINT)+1,
            cx = int(self.cx*PIXELSPERPOINT),
            cy = int(self.cy*PIXELSPERPOINT),
            lw = int(self.lw*PIXELSPERPOINT),
            colorspec = self.colorspec(self.ec),
            bgcolorspec = self.colorspec(self.fc),
        )
        return xml