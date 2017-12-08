import os
import shutil
import random
from ..templates import PPTXPATH, LINE, RECT, SHAPE
from ..convert import dir2pptx
from ..utils import chdir, random_name, PIXELSPERPOINT

def new(filename, xml=None):
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

        # Work on slide one (the only slide created)
        slidename = os.path.join(tempdirname, 'ppt/slides/slide1.xml')

        # Insert custom xml
        with open(slidename, 'r') as file:
            content = file.read()
        content = content.replace('{objects}',xml)
        with open(slidename,'w') as file:
            file.write(content)
        
        # Convert temporary folder to pptx
        dir2pptx(tempdirname, filename)
        shutil.rmtree(tempdirname)


class Object(object):
    def __init__(self, name=''):
        self.name = ''
        self._xml = ''
    def xml(self):
        return self._xml
    def save(self, filename):
        new(filename, self.xml())
    def colorspec(self, color):
        if self.color is None:
            colorspec = '<a:noFill/>'
        else:
            colorspec = '<a:solidFill><a:srgbClr val="'+color+'"/></a:solidFill>'
        return colorspec
    def __add__(self, obj):
        return PPT(objects=[self, obj])

class PPT(Object):
    ''' Powerpoint presentation object '''
    def __init__(self, objects=[]):
        self.objects = []
    def xml(self):
        xml = ''
        for obj in self.objects:
            xml = '\n'+obj.xml()+'\n'
    def save(self, filename):
        new(filename, self.xml())
    def __add__(self, obj):
        self.objects.append(obj)

class Line(Object):
    def __init__(self, name='Line', x=10, y=10, cx=100, cy=50, lw=1, color='000000'):
        self.name = name
        self.x = x
        self.y = y
        self.cx = cx
        self.cy = cy
        self.lw = lw
        self.color = color
        self._xml = LINE
    def xml(self):
        xml = self._xml.format(
            name = self.name,
            x = self.x*PIXELSPERPOINT+1,
            y = self.y*PIXELSPERPOINT+1,
            cx = self.cx*PIXELSPERPOINT,
            cy = self.cy*PIXELSPERPOINT,
            lw = self.lw*PIXELSPERPOINT,
            color = self.color,
            )
        return xml

class Rectangle(Object):
    def __init__(self, name='Rect', x=10, y=10, cx=100, cy=50, lw=1, color='000000', bgcolor='eeeeee'):
        self.name = name
        self.x = x
        self.y = y
        self.cx = cx
        self.cy = cy
        self.lw = lw
        self.color = color
        self.bgcolor = bgcolor
        self._xml = RECT
    def xml(self):
        xml = self._xml.format(
            name = self.name,
            x = self.x*PIXELSPERPOINT+1,
            y = self.y*PIXELSPERPOINT+1,
            cx = self.cx*PIXELSPERPOINT,
            cy = self.cy*PIXELSPERPOINT,
            lw = self.lw*PIXELSPERPOINT,
            colorspec = self.colorspec(self.color),
            bgcolorspec = self.colorspec(self.bgcolor),
        )
        return xml


class Shape(Object):
    def __init__(self, name='Shape', offset=(0,0), shape=[(0,0),(0,100),(50,0)], color='000000', bgcolor='eeeeee', closed=True):
        self.name = name
        self.offset = offset
        self.shape = shape
        self.color = color
        self.bgcolor = bgcolor
        self.closed = closed
        self._xml = SHAPE
    def xml(self):
        xml = self._xml.format(
            name = self.name,
            x = self.offset[0]*PIXELSPERPOINT+1,
            y = self.offset[1]*PIXELSPERPOINT+1,
            shapespec = self.shapespec(self.shape, self.closed),
            colorspec = self.colorspec(self.color),
            bgcolorspec = self.colorspec(self.bgcolor),
        )
        print(xml)
        return xml
    def shapespec(self, shape, closed):
        if len(shape) == 0:
            return '\n'
        shapespec = '<a:moveTo><a:pt x="{x}" y="{y}"/></a:moveTo>\n'.format(
            x=shape[0][0]*PIXELSPERPOINT, 
            y=shape[0][1]*PIXELSPERPOINT,
        )
        for x,y in shape[1:]:
            shapespec = shapespec + '<a:lnTo><a:pt x="{x}" y="{y}"/></a:lnTo>\n'.format(
                x=x*PIXELSPERPOINT,
                y=y*PIXELSPERPOINT,
            )
        if closed:
            shapespec = shapespec + '<a:close/>\n'
        return shapespec