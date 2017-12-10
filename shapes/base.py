#############
## Imports ##
#############

from .ppt import new


###################
## Object Parent ##
###################

class Object(object):
    ''' An abstract powerpoint object '''

    _mpl_shrink_factor = 0.9 # scaling factor for matplotlib figures

    def __init__(self, name='', slidesize=(6,4)):
        self.name = name
        self._xml = ''
        self.slidesize = slidesize

    def xml(self):
        ''' Get xml representation of current object '''
        return self._xml

    def save(self, filename):
        ''' Save current object as powerpoint presentation '''
        new(filename, xml=self.xml(), slidesize=self.slidesize)

    def colorspec(self, color):
        ''' Xml representation of color. If color is None, a noFill xml tag is returned '''
        if color is None:
            colorspec = '<a:noFill/>'
        else:
            colorspec = '<a:solidFill><a:srgbClr val="'+color+'"/></a:solidFill>'
        return colorspec

    def __add__(self, obj):
        ''' Objects can be added together in a Group '''
        return Group(objects=[self, obj])


##################
## Object Group ##
##################

class Group(Object):
    ''' Powerpoint group object. This object consists out of a collection of smaller objects (other groups are allowed).'''

    def __init__(self, name='ppt', objects=[], slidesize=(6,4)):
        Object.__init__(self, name=name, slidesize=slidesize)
        self.objects = objects

    def xml(self):
        ''' The xml representation of a group consists of the total string of the seperate objects '''
        xml = ''
        for obj in self.objects:
            xml += '\n'+obj.xml()+'\n'
        return xml

    def __add__(self, other):
        ''' Objects can be added to the group '''
        if other is None:
            return self
        if hasattr(other, 'objects'):
            return Group(objects=self.objects+other.objects, slidesize=self.slidesize)
        else:
            return Group(objects=self.objects+[other], slidesize=self.slidesize)