#############
## Imports ##
#############

import numpy as np
from scipy.interpolate import interp1d

from .base import Object
from ..templates import LINE
from ..utils.colors import color2hex
from ..utils.string import random_name
from ..utils.constants import POINTSPERINCH
from ..utils.constants import PIXELSPERPOINT


##########
## Line ##
##########

class Line(Object):
    ''' A custom LINE '''
    def __init__(self, name='Line', shape=[(0,0),(0,100),(50,0)], ec='000000', fc='eeeeee', closed=False, slidesize=(6,4)):
        Object.__init__(self, name=name, slidesize=slidesize)
        self.shape = np.array(shape)
        self.ec = ec
        self.fc = fc
        self.closed = closed
        self.cx, self.cy = np.max(shape, axis=0) - np.min(shape, axis=0)
        self.x, self.y = np.min(shape, axis=0)
        self._xml = LINE
    
    def get_adjusted_shape(self):
        shape = self.shape.copy()
        shape[:,0] -= self.x
        shape[:,1] -= self.y
        return shape

    @classmethod
    def from_mpl(cls, mpl_line):
        slidesize = (mpl_line.figure.get_figwidth(), mpl_line.figure.get_figheight())
        f = cls._mpl_shrink_factor

        slide_x0 = 0.5*(1-f)*slidesize[0]*POINTSPERINCH
        slide_x1 = slide_x0 + f*slidesize[0]*POINTSPERINCH
        plot_x0, plot_x1 = mpl_line.axes.get_xlim()

        slide_y1 = 0.5*(1-f)*slidesize[1]*POINTSPERINCH
        slide_y0 = slide_y1+f*slidesize[1]*POINTSPERINCH
        plot_y0, plot_y1 = mpl_line.axes.get_ylim()
        
        mx = (slide_x1-slide_x0)/(plot_x1-plot_x0)
        sx = 0.5*slide_x0
        px = sx/mx

        my = (slide_y1-slide_y0)/(plot_y1-plot_y0)
        sy = 0.5*slide_y0
        py = sy/my

        x = interp1d([plot_x0,plot_x1],[slide_x0,slide_x1], fill_value='extrapolate')(mpl_line._x)
        x[x<0.5*slide_x0] = 0.5*slide_x0
        x[x>slide_x1+0.5*slide_x0] = slide_x1+0.5*slide_x0

        y = interp1d([plot_y0,plot_y1],[slide_y0,slide_y1], fill_value='extrapolate')(mpl_line._y)
        y[y<0.5*slide_y1] = 0.5*slide_y1
        y[y>slide_y0+0.5*slide_y1] = slide_y0+0.5*slide_y1

        shape = np.stack((x,y), axis=1)

        if ((y < slide_y1) | (y > slide_y0) | (x < slide_x0) | (x > slide_x1)).all():
            return None
 
        line = cls(
            name='mplline_' + random_name(5),
            shape=shape,
            ec = color2hex(mpl_line.get_color()),
            fc = None,
            closed = False,
            slidesize=slidesize,
        )

        return line
        
    def xml(self):
        xml = self._xml.format(
            name = self.name,
            x = int(self.x*PIXELSPERPOINT)+1,
            y = int(self.y*PIXELSPERPOINT)+1,
            cx = int(self.cx*PIXELSPERPOINT),
            cy = int(self.cy*PIXELSPERPOINT),
            shapespec = self.shapespec(self.get_adjusted_shape(), self.closed),
            colorspec = self.colorspec(self.ec),
            bgcolorspec = self.colorspec(self.fc),
        )
        return xml

    def shapespec(self, shape, closed):
        # check if shape is empty
        if len(shape) == 0:
            return ''

        # first point in shape
        shapespec = '<a:moveTo><a:pt x="{x}" y="{y}"/></a:moveTo>\n'.format(
            x=int(shape[0][0]*PIXELSPERPOINT), 
            y=int(shape[0][1]*PIXELSPERPOINT),
        )

        # other points in shape
        for x,y in shape[1:]:
            shapespec = shapespec + '<a:lnTo><a:pt x="{x}" y="{y}"/></a:lnTo>\n'.format(
                x=int(x*PIXELSPERPOINT),
                y=int(y*PIXELSPERPOINT),
            )
        
        # close shape
        if closed:
            shapespec = shapespec + '<a:close/>\n'

        return shapespec