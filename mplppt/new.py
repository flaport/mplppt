#############
## Imports ##
#############

import os
import shutil
from matplotlib.pyplot import imsave


from .convert import dir2pptx
from .templates import PPTXPATH
from .utils.contextmanagers import chdir
from .utils.contextmanagers import tempdir
from .utils.constants import PIXELSPERINCH


#############
## New PPT ##
#############


def new(filename, xml=None, rels=None, slidesize=(6, 4)):
    """ Creates a new blank powerpoint with a single slide 
    
    Args:
        filename: str: the filename of the new pptx file
        xml: additional xml to insert into the pptx file
        rels: additional rels to insert into the pptx file
        slidesize: the slidesize of the slides in the pptx file
    """
    # check filename
    if filename.endswith(".pptx"):
        filename = filename[:-5]

    # xml should be a string
    if xml is None:
        xml = ""

    # rels should be a list:
    if rels is None:
        rels = []

    # Split path into folder and filename
    splitted_path = os.path.split(filename)
    if splitted_path[:-1] == ("",):
        dir = "."
    else:
        dir = os.path.join(splitted_path[:-1])
    filename = splitted_path[-1]

    # Go to folder
    with chdir(dir):
        # Create a temporary folder to work in
        with tempdir(PPTXPATH) as tempdirname:
            # Change slide size
            presname = os.path.join(tempdirname, "ppt/presentation.xml")
            with open(presname, "r") as file:
                content = file.read()
            content = content.format(
                cx=int(slidesize[0] * PIXELSPERINCH),
                cy=int(slidesize[1] * PIXELSPERINCH),
            )
            with open(presname, "w") as file:
                file.write(content)

            # Insert custom xml
            slidename = os.path.join(tempdirname, "ppt/slides/slide1.xml")
            with open(slidename, "r") as file:
                content = file.read()
            content = content.replace("{objects}", xml)
            with open(slidename, "w") as file:
                file.write(content)

            # Insert custom relationships (for images)
            relsname = os.path.join(tempdirname, "ppt/slides/_rels/slide1.xml.rels")
            with open(relsname, "r") as file:
                content = file.read()
            relationships = ""
            for rel, array, target in rels:
                imsave(os.path.join(tempdirname, "ppt/media", target), array)
                relationships += rel
            content = content.format(relationships=relationships)
            with open(relsname, "w") as file:
                file.write(content)

            # Convert temporary folder to pptx
            dir2pptx(tempdirname, filename)
