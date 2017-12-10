#############
## Imports ##
#############

import os
from ..utils import chdir
from ..utils import tempdir
from ..convert import dir2pptx
from ..templates import PPTXPATH
from ..utils.constants import PIXELSPERINCH


#############
## New PPT ##
#############

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