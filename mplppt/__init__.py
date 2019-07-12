""" `mplppt` seeks to implement an alternative `savefig` function for `matplotlib` figures. 
This `savefig` function saves a `matplotlib` figure with a single axis to a powerpoint 
presentation with a single slide containing the figure. """

__author__ = "Floris Laporte"
__version__ = "0.0.0"

##################
## Unicode Hack ##
## For Python 2 ##
##################

try:  # Python 2
    import sys

    reload(sys)
    sys.setdefaultencoding("utf8")
except NameError:  # Python 3
    pass

################
## Submodules ##
################

from . import shapes
from . import convert
from . import templates
from . import utils


############
## Shapes ##
############

from .shapes import Group
from .shapes import Line
from .shapes import Text
from .shapes import Canvas
from .shapes import Polygon
from .shapes import Rectangle


########################
## The Magic Function ##
########################

from .save import savefig


####################
## New powerpoint ##
####################

from .new import new

