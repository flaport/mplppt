import os
import shutil
import random
import numpy as np
from scipy.interpolate import interp1d
from ..templates import PPTXPATH, LINE, RECT, LINE, TEXT
from ..convert import dir2pptx
from ..utils import chdir, tempdir, random_name, color2hex
from ..utils import POINTSPERINCH, PIXELSPERPOINT, PIXELSPERINCH, ALIGNMENTS

def new(filename, xml=None, slidesize=(6,4)):
    ''' Creates a new blank powerpoint with a single slide '''
    # check filename
    if filename.endswith('.pptx'):
        filename = filename[:-5]

    # xml should be a string
    if xml is None:
        xml = ''
    
    # Split path into folder and filename
    splitted_path = os.path.split(filename)
    if splitted_path[:-1] == ('',):
        dir = '.'
    else:
        dir = os.path.join(splitted_path[:-1])
    filename = splitted_path[-1]

    # Go to folder
    with chdir(dir):
        # Create a temporary folder to work in
        with tempdir(PPTXPATH) as tempdirname:
            # Change slide size
            presname = os.path.join(tempdirname, 'ppt/presentation.xml')
            with open(presname, 'r') as file:
                content = file.read()
            content = content.format(
                cx = int(slidesize[0]*PIXELSPERINCH),
                cy = int(slidesize[1]*PIXELSPERINCH),
            )
            with open(presname, 'w') as file:
                file.write(content)

            # Insert custom xml
            slidename = os.path.join(tempdirname, 'ppt/slides/slide1.xml')
            with open(slidename, 'r') as file:
                content = file.read()
            content = content.replace('{objects}',xml)
            with open(slidename,'w') as file:
                file.write(content)
            
            # Convert temporary folder to pptx
            dir2pptx(tempdirname, filename)


class Object(object):
    ''' An abstract powerpoint object '''

    _mpl_shrink_factor = 0.9 # scaling factor for matplotlib figures

    def __init__(self, name='', slidesize=(6,4)):
        self.name = name
        self._xml = ''
        self.slidesize = slidesize
    def xml(self):
        return self._xml
    def save(self, filename):
        new(filename, xml=self.xml(), slidesize=self.slidesize)
    def colorspec(self, color):
        if color is None:
            colorspec = '<a:noFill/>'
        else:
            colorspec = '<a:solidFill><a:srgbClr val="'+color+'"/></a:solidFill>'
        return colorspec
    def __add__(self, obj):
        return Group(objects=[self, obj])

class Group(Object):
    ''' Powerpoint presentation object. This object consists out of a collection of objects.'''
    def __init__(self, name='ppt', objects=[], slidesize=(6,4)):
        Object.__init__(self, name=name, slidesize=slidesize)
        self.objects = objects
    def xml(self):
        xml = ''
        for obj in self.objects:
            xml += '\n'+obj.xml()+'\n'
        return xml
    def __add__(self, other):
        if other is None:
            return self
        if hasattr(other, 'objects'):
            return Group(objects=self.objects+other.objects, slidesize=self.slidesize)
        else:
            return Group(objects=self.objects+[other], slidesize=self.slidesize)

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
        self._xml = RECT

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
        self._xml = RECT.replace('</p:sp>','\n'+TEXT+'\n</p:sp>\n')

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