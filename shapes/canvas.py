#############
## Imports ##
#############

import numpy as np
from scipy.interpolate import interp1d

from .line import Line
from .text import Text
from .base import Group
from .rectangle import Rectangle
from ..utils.constants import POINTSPERINCH


############
## Canvas ##
############

class Canvas(Group):
    def __init__(self, slidesize=(6,4)):
        f = self._mpl_shrink_factor
        x = 0.5*(1-f)*slidesize[0]
        y = 0.5*(1-f)*slidesize[1]
        cx = f*slidesize[0]
        cy = f*slidesize[1]
        self.rect = Rectangle(
            name='Canvas', 
            x=x*POINTSPERINCH, 
            y=y*POINTSPERINCH,
            cx=cx*POINTSPERINCH,
            cy=cy*POINTSPERINCH, 
            lw=0.8, 
            ec='000000', 
            fc=None, 
            slidesize=slidesize
        )
        self.left = Rectangle(
            name = 'Canvas_left',
            x = 0,
            y = 0,
            cx = x*POINTSPERINCH,
            cy = slidesize[1]*POINTSPERINCH,
            lw = 0.8,
            ec = None,
            fc = 'ffffff',
        )
        self.right = Rectangle(
            name = 'Canvas_right',
            x = (x+cx)*POINTSPERINCH,
            y = 0,
            cx = x*POINTSPERINCH,
            cy = slidesize[1]*POINTSPERINCH,
            lw = 0.8,
            ec = None,
            fc = 'ffffff',
        )
        self.top = Rectangle(
            name = 'Canvas_top',
            x = 0,
            y = 0,
            cx = slidesize[0]*POINTSPERINCH,
            cy = y*POINTSPERINCH,
            lw = 0.8,
            ec = None,
            fc = 'ffffff',
        )
        self.bottom = Rectangle(
            name = 'Canvas_bottom',
            x = 0,
            y = (y+cy)*POINTSPERINCH,
            cx = slidesize[0]*POINTSPERINCH,
            cy = y*POINTSPERINCH,
            lw = 0.8,
            ec = None,
            fc = 'ffffff',
        )
        Group.__init__(self, name='Canvas', objects=[self.left, self.right, self.top, self.bottom, self.rect])

    @classmethod
    def from_mpl(cls, mpl_ax):
        slidesize = (mpl_ax.figure.get_figwidth(), mpl_ax.figure.get_figheight())
        canvas = cls(
            slidesize = slidesize,
        )
        ylim = mpl_ax.get_ylim()
        for mpl_text in mpl_ax.xaxis.get_ticklabels():
            old_axes = mpl_text.axes
            old_text = mpl_text._text
            old_y = mpl_text._y

            mpl_text.axes = mpl_ax
            mpl_text._text = mpl_text._text.replace('\u2212','-')
            mpl_text._y = ylim[0]
            canvas = canvas + Text.from_mpl(mpl_text)

            mpl_text.axes = old_axes
            mpl_text._text = old_text
            mpl_text._y = old_y

        xlim = mpl_ax.get_xlim()
        for mpl_text in mpl_ax.yaxis.get_ticklabels():
            old_axes = mpl_text.axes
            old_text = mpl_text._text
            old_x = mpl_text._x

            mpl_text.axes = mpl_ax
            mpl_text._text = mpl_text._text.replace('\u2212','-')
            mpl_text._x = xlim[0]
            canvas = canvas + Text.from_mpl(mpl_text)

            mpl_text.axes = old_axes
            mpl_text._text = old_text
            mpl_text._x = old_x

        return canvas