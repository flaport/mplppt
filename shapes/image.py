#############
## Imports ##
#############

from matplotlib.pyplot import imread, imsave

from .base import Object
from ..templates import IMAGE
from ..utils.string import random_name
from ..utils.contextmanagers import chdir
from ..utils.constants import PIXELSPERPOINT


###############
## Rectangle ##
###############

class Image(Object):
    ''' An Image '''
    def __init__(self, source, name='', x=0, y=0, cx=None, cy=None, slidesize=(6,4)):
        name = '.'.join(source.split('.')[:-1]) if name=='' else name
        Object.__init__(self, name=name, slidesize=slidesize)
        self.array = imread(source)
        self.id = 'lv6c7'#random_name(5)
        self.source = source
        self.target = self.name + '_' + self.id + '.' + source.split('.')[-1]
        self.x = x
        self.y = y

        self.cx = 10000*self.array.shape[1] / PIXELSPERPOINT if cx is None else cx
        self.cy = 10000*self.array.shape[0] / PIXELSPERPOINT if cy is None else cy
        self._xml = IMAGE
    
    def rels(self):
        ''' Get relationship representation of the image together with the source location and the target location '''
        rels = '<Relationship Id="{id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{target}"/>'
        rels = rels.format(
            id = self.id,
            target = self.target,
        )
        print(self.source)
        print(self.target)
        return [(rels, self.source, self.target)]

    def xml(self):
        ''' Get xml representation of the rectangle '''
        xml = self._xml.format(
            name = self.name,
            x  = int(self.x*PIXELSPERPOINT)+1,
            y  = int(self.y*PIXELSPERPOINT)+1,
            cx = int(self.cx*PIXELSPERPOINT),
            cy = int(self.cy*PIXELSPERPOINT),
            id = self.id,
        )
        return xml