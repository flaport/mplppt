""" Base objects for powerpoint """

#############
## Imports ##
#############

from ..new import new


###################
## Object Parent ##
###################


class Object(object):
    """ An abstract powerpoint object
    
    a powerpoint object can be any base object or a group of other objects.
    """

    # scaling factor for matplotlib figures
    # if this factor is 1, the whole slide will be covered by the plot
    _mpl_shrink_factor = 0.9

    def __init__(self, name="", slidesize=(6, 4)):
        """ powerpoint object initialization

        Args:
            name: str="": the name of the object to embed in the powerpoint presentation
            slidesize=(6,4): the size of the slide the object is embedded in.        
        """

        # TODO: Create a slide object to embed all the slide properties in.

        self.name = name
        self._xml = ""
        self.slidesize = slidesize

    def rels(self):
        """ Get relationship representation of current object 
        
        Returns:
            rels: list: the list of relationships to other objects.
        """
        return []

    def xml(self):
        """ Get xml representation of current object 
        
        Returns:
            xml: str: the xml representation of this object
        """
        return self._xml

    def save(self, filename):
        """ Save current object as powerpoint presentation 
        
        Args:
            filename: str: the filename to save this object under.
        """
        new(filename, xml=self.xml(), rels=self.rels(), slidesize=self.slidesize)

    def colorspec(self, color):
        """ Xml representation of the color of the object. 
        
        Args:
            color: None|str|tuple: color can be a hexstring of format 'aaaaaa', or a tuple consisting of a
                hexstring and an alpha value between 0 and 1. If `None` a `noFill` xml tag will be returned.

        Returns:
            xml: the xml representation for the color of the object.
        """
        if color is None:
            return "<a:noFill/>"
        else:
            if not isinstance(color, str):
                color, alpha = color
                alpha = str(int(alpha * 100000))
            else:
                alpha = "100000"
            return (
                '<a:solidFill><a:srgbClr val="'
                + color
                + '"><a:alpha val="'
                + alpha
                + '"/></a:srgbClr></a:solidFill>'
            )

    def __add__(self, other):
        """ Objects can be added together to form a Group of objects 
        
        Args:
            other: Object: the object to add this object together with into a group

        Returns:
            group: Group: a group of two objects containing this object and the other object.
        """
        return Group(objects=[self, other], slidesize=self.slidesize)

    def __radd__(self, other):
        """ Objects can be added together to form a Group of objects

        [same behavior as __add__]
        
        Args:
            other: Object: the object to add this object together with into a group

        Returns:
            group: Group: a group of two objects containing this object and the other object.
        """
        return self + other


##################
## Object Group ##
##################


class Group(Object):
    """ A Group consists out of a collection of smaller objects (other groups are allowed).

    NOTE: A mplppt Group does NOT correspond to a Powerpoint Group. It is just a group in
    python and acts as an abstract object.
    """

    # TODO: Implement the expected behavior such that an mplppt group corresponds to a powerpoint group.

    def __init__(self, name="ppt", objects=[], slidesize=(6, 4)):
        Object.__init__(self, name=name, slidesize=slidesize)
        self.objects = objects

    def rels(self):
        """ Get relationship representation of current object 
        
        Returns:
            rels: list: the list of relationships to other objects.
        """
        rels = []
        for obj in self.objects:
            rels += obj.rels()
        return rels

    def xml(self):
        """ Get xml representation of current object 
        
        Returns:
            xml: str: the xml representation of this object
        """
        xml = ""
        for obj in self.objects:
            xml += "\n" + obj.xml() + "\n"
        return xml

    def __add__(self, other):
        """ Objects can be added together to form a Group of objects 
        
        Args:
            other: Object: the object to add this object together with into a group

        Returns:
            group: Group: a group of two objects containing this object and the other object.
        """
        # TODO: remove this method in favor of the more generic __add__ method of Object.
        if other is None: # if nothing is added to the group, one should return the original group
            return self
        # prefer this slidesize if it's defined, otherwise take over the slidesize of the other group
        slidesize = other.slidesize if len(self.objects) == 0 else self.slidesize
        if hasattr(other, "objects"): # if the other object is a group, merge the two groups
            return Group(objects=self.objects + other.objects, slidesize=slidesize)
        else: # if the other object is an object, add it to the objects
            return Group(objects=self.objects + [other], slidesize=slidesize)

    def __iadd__(self, other):
        """ Objects can be added into the group 
        
        Args:
            other: Object: the object to add into the group
        
        Returns:
            group: Group: the resulting group after the addition of the other object
        """
        if other is not None:
            self.slidesize = (
                other.slidesize if len(self.objects) == 0 else self.slidesize
            )
            if hasattr(other, "objects"):
                self.objects += other.objects
            else:
                self.objects += [other]
        return self

    def __sub__(self, other):
        """ Objects can be removed from the group 
        
        Args:
            other: Object: the object to remove from the group
        
        Returns:
            group: Group: the resulting group after the removal of the object
        """
        if other is None:
            return self
        if other not in self.objects:
            raise ValueError("Group does not contain object %s" % object.name)
        return Group(
            objects=[obj for obj in self.objects if obj is not other],
            slidesize=self.slidesize,
        )

    def __isub__(self, other):
        """ Objects can be removed from the group 
        
        Args:
            other: Object: the object to remove from the group
        
        Returns:
            group: Group: the resulting group after the removal of the object
        """
        if other is not None:
            i = self.objects.index(other)
            del self.objects[i]
        return self
