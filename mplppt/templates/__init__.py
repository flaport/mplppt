#############
## Imports ##
#############

import os
from ..utils import chdir, get_content


###############
## Constants ##
###############

TEMPLATESPATH = __file__.replace("__init__.pyc", "").replace("__init__.py", "")
PPTXPATH = os.path.join(TEMPLATESPATH, "pptx")


###################
## XML Templates ##
###################

with chdir(TEMPLATESPATH):
    LINE = get_content("line.xml")
    TEXT = get_content("text.xml")
    RECTANGLE = get_content("rectangle.xml")
    IMAGE = get_content("image.xml")
