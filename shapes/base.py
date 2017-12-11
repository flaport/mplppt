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
        '''
        An object needs a name and the size of the slide it is embedded in.
        
        TODO: Create a slide object to embed all the slide properties in.
        '''
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
        '''
        Xml representation of color. If color is None, a noFill xml tag is returned.

        color can be a hexstring of format 'aaaaaa', or a tuple consisting of a
        hexstring and an alpha value between 0 and 1.
        '''
        if color is None:
            return '<a:noFill/>'
        else:
            if type(color) is not str:
                color, alpha = color
                alpha = str(int(alpha*100000))
            else:
                alpha = '100000'
            return '<a:solidFill><a:srgbClr val="'+color+'"><a:alpha val="'+alpha+'"/></a:srgbClr></a:solidFill>'

    def __add__(self, obj):
        ''' Objects can be added together to form a Group of objects '''
        return Group(objects=[self, obj], slidesize=self.slidesize)

    def __radd__(self, obj):
        ''' Objects can be added together to form a Group of objects '''
        return self + obj


##################
## Object Group ##
##################

class Group(Object):
    '''
    This object consists out of a collection of smaller objects (other groups are allowed).

    NOTE: A mplppt Group does NOT correspond to a Powerpoint Group. It is just a group in
    python and acts as an abstract object.

    TODO: Implement this expected behavior such that a mplppt group corresponds to a powerpoint group.
    '''

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
        if other is None: return self
        slidesize = other.slidesize if len(self.objects) == 0 else self.slidesize
        if hasattr(other, 'objects'):
            return Group(objects=self.objects+other.objects, slidesize=slidesize)
        else:
            return Group(objects=self.objects+[other], slidesize=slidesize)
    
    def __iadd__(self, other):
        ''' Objects can be added to the group '''
        if other is not None:
            self.slidesize = other.slidesize if len(self.objects) == 0 else self.slidesize
            if hasattr(other, 'objects'):
                self.objects += other.objects
            else:
                self.objects += [other]
        return self

    def __sub__(self, other):
        ''' Objects can be removed from the group '''
        if other is None: return self
        if other not in self.objects: raise ValueError('Group does not contain object %s'%object.name)
        return Group(objects=[obj for obj in self.objects if obj is not other], slidesize=self.slidesize)

    def __isub__(self, other):
        ''' Objects can be removed from the group '''
        if other is not None:
            i = self.objects.index(other)
            del self.objects[i]
        return self

