import os
import shutil
import random
from ..templates import PPTXPATH, LINE, RECT, SHAPE
from ..convert import dir2pptx
from ..utils import chdir, random_name, rgba2hex
from ..utils import POINTSPERINCH, PIXELSPERPOINT, PIXELSPERINCH

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
        tempdirname = random_name()
        shutil.copytree(PPTXPATH, tempdirname)

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
        shutil.rmtree(tempdirname)


class Object(object):
    ''' An abstract powerpoint object '''
    def __init__(self, name='', slidesize=(6,4)):
        self.name = ''
        self._xml = ''
        self.slidesize = slidesize
    def xml(self):
        return self._xml
    def save(self, filename):
        new(filename, xml=self.xml(), slidesize=self.slidesize)
    def colorspec(self, ec):
        if ec is None:
            colorspec = '<a:noFill/>'
        else:
            colorspec = '<a:solidFill><a:srgbClr val="'+ec+'"/></a:solidFill>'
        return colorspec
    def __add__(self, obj):
        return PPT(objects=[self, obj])

class PPT(Object):
    ''' Powerpoint presentation object. This object consits out of a collection of objects.'''
    def __init__(self, name='ppt', objects=[], slidesize=(6,4)):
        Object.__init__(self, name, slidesize)
        self.objects = objects
    def xml(self):
        xml = ''
        for obj in self.objects:
            xml += '\n'+obj.xml()+'\n'
        return xml
    def __add__(self, other):
        if hasattr(other, 'objects'):
            return PPT(objects=self.objects+other.objects, slidesize=self.slidesize)
        else:
            return PPT(objects=self.objects+[other], slidesize=self.slidesize)

class Line(Object):
    ''' A simple straight line object '''
    def __init__(self, name='Line', x=0, y=0, cx=100, cy=50, lw=1, ec='000000', slidesize=(6,4)):
        Object.__init__(self, name, slidesize)
        self.x = x
        self.y = y
        self.cx = cx
        self.cy = cy
        self.lw = lw
        self.ec = ec
        self._xml = LINE
    def xml(self):
        xml = self._xml.format(
            name = self.name,
            x  = int(self.x*PIXELSPERPOINT)+1,
            y  = int(self.y*PIXELSPERPOINT)+1,
            cx = int(self.cx*PIXELSPERPOINT),
            cy = int(self.cy*PIXELSPERPOINT),
            lw = int(self.lw*PIXELSPERPOINT),
            ec = self.ec,
            )
        return xml

class Rectangle(Object):
    ''' A rectangle '''
    def __init__(self, name='Rect', x=0, y=0, cx=100, cy=50, lw=1, ec='000000', fc='eeeeee', slidesize=(6,4)):
        Object.__init__(self, name, slidesize)
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
        slide_x0, slide_x1 = 0, mpl_rect._axes.figure.get_figwidth()
        plot_x0, plot_x1 = mpl_rect._axes.get_xlim()
        mx = (slide_x0-slide_x1)/(plot_x0 - plot_x1)
        x = mx*(mpl_rect._x-plot_x0) + slide_x0
        cx = mx*mpl_rect._width
        if cx < 0:
            x += cx
            cx *= -1

        slide_y0, slide_y1 = mpl_rect._axes.figure.get_figheight(), 0
        plot_y0, plot_y1 = mpl_rect._axes.get_ylim()
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
            ec = rgba2hex(mpl_rect._edgecolor),
            fc = rgba2hex(mpl_rect._facecolor),
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
        print(xml)
        return xml


class Shape(Object):
    ''' A custom shape '''
    def __init__(self, name='Shape', shape=[(0,0),(0,100),(50,0)], offset=(0,0), ec='000000', fc='eeeeee', closed=True, slidesize=(6,4)):
        Object.__init__(self, name, slidesize)
        self.shape = shape
        self.offset = offset
        self.ec = ec
        self.fc = fc
        self.closed = closed
        self._xml = SHAPE
    def xml(self):
        xml = self._xml.format(
            name = self.name,
            x = int(self.offset[0]*PIXELSPERPOINT)+1,
            y = int(self.offset[1]*PIXELSPERPOINT)+1,
            shapespec = self.shapespec(self.shape, self.closed),
            colorspec = self.colorspec(self.ec),
            bgcolorspec = self.colorspec(self.fc),
        )
        return xml
    def shapespec(self, shape, closed):
        if len(shape) == 0:
            return '\n'
        shapespec = '<a:moveTo><a:pt x="{x}" y="{y}"/></a:moveTo>\n'.format(
            x=int(shape[0][0]*PIXELSPERPOINT), 
            y=int(shape[0][1]*PIXELSPERPOINT),
        )
        for x,y in shape[1:]:
            shapespec = shapespec + '<a:lnTo><a:pt x="{x}" y="{y}"/></a:lnTo>\n'.format(
                x=int(x*PIXELSPERPOINT),
                y=int(y*PIXELSPERPOINT),
            )
        if closed:
            shapespec = shapespec + '<a:close/>\n'
        return shapespec