import os
from ..utils import chdir, get_content

TEMPLATESPATH = __file__.replace('__init__.pyc','').replace('__init__.py','')
PPTXPATH = os.path.join(TEMPLATESPATH,'pptx')

# XML CONTENT
with chdir(TEMPLATESPATH):
  RECT = get_content('rect.xml')
  LINE = get_content('line.xml')
  SHAPE = get_content('shape.xml')
