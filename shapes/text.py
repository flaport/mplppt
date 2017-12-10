#############
## Imports ##
#############

import numpy as np
from scipy.interpolate import interp1d

from .base import Object
from ..templates import TEXT
from ..templates import RECTANGLE
from ..utils.colors import color2hex
from ..utils.colors import random_name
from ..utils.constants import ALIGNMENTS
from ..utils.constants import POINTSPERINCH
from ..utils.constants import PIXELSPERPOINT

from .base import Object


##########
## Text ##
##########

class Text(Object):
    ''' A text box '''
    def __init__(self, text='', x=0, y=0, cx=None, cy=None, size=18, font='Arial', color='000000', ha='c', va='c', slidesize=(6,4)):
        Object.__init__(self, name='', slidesize=slidesize)
        self.text = text
        self.x = x
        self.y = y
        self.cx = cx
        self.cy = cy
        self.ha = ALIGNMENTS[ha]
        self.va = ALIGNMENTS[va]
        self.size = size
        self.color = color
        self.font = font
        self._xml = RECTANGLE.replace('</p:sp>','\n'+TEXT+'\n</p:sp>\n')

        if self.ha == 'c':
            self.x -= 0.5*self.cx
        elif self.ha == 'r':
            self.x -= self.cx
        if self.va == 'c':
            self.y -= 0.5*self.cy
        elif self.va == 'b':
            self.y -= self.cy

    @classmethod
    def from_mpl(cls, mpl_text):
        slidesize = (mpl_text.figure.get_figwidth(), mpl_text.figure.get_figheight())
        f = cls._mpl_shrink_factor

        slide_x0 = 0.5*(1-f)*slidesize[0]*POINTSPERINCH
        slide_x1 = slide_x0 + f*slidesize[0]*POINTSPERINCH
        plot_x0, plot_x1 = mpl_text.axes.get_xlim()

        slide_y1 = 0.5*(1-f)*slidesize[1]*POINTSPERINCH
        slide_y0 = slide_y1+f*slidesize[1]*POINTSPERINCH
        plot_y0, plot_y1 = mpl_text.axes.get_ylim()

        x = interp1d([plot_x0,plot_x1],[slide_x0,slide_x1], fill_value='extrapolate')(mpl_text._x)
        y = interp1d([plot_y0,plot_y1],[slide_y0,slide_y1], fill_value='extrapolate')(mpl_text._y)

        bbox = np.array(mpl_text.get_window_extent(renderer=mpl_text.figure.canvas.get_renderer()))
        cx, cy = bbox[1] - bbox[0]

        text = cls(
            text = mpl_text._text,
            x = x,
            y = y,
            cx = 1.1*abs(cx),
            cy = 1.1*abs(cy),
            size = mpl_text.get_fontsize(),
            font = mpl_text.get_fontname(),
            color = mpl_text.get_color(),
            ha = mpl_text._horizontalalignment,
            va = mpl_text._verticalalignment,
            slidesize = slidesize,
        )
            
        return text

    def xml(self):
        if self.text.replace(' ','').replace('\n','') == '':
            return ''
        cx = self.cx
        if cx is None:
            cx = self.size*max([len(line) for line in self.text.splitlines()])
        cy = self.cy
        if cy is None:
            cy = self.size+2
        xml = self._xml.format(
            text = self.text,
            size = int(self.size*100),
            color = color2hex(self.color),
            font = self.font,
            name = self.text.splitlines()[0],
            x  = int(self.x*PIXELSPERPOINT)+1,
            y  = int(self.y*PIXELSPERPOINT)+1,
            cx = int(cx*PIXELSPERPOINT),
            cy = int(cy*PIXELSPERPOINT),
            lw = int(0.2*PIXELSPERPOINT),
            colorspec = self.colorspec(None),
            bgcolorspec = self.colorspec(None),
        )
        return xml