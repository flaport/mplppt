""" Filetype conversions """


#############
## Imports ##
#############

import os
import sys
import shutil
import zipfile

from .utils.strings import parse_xml
from .utils.contextmanagers import chdir


#################
## Conversions ##
#################


def dir2pptx(dirname, target=None):
    """ Create ppt file from folder with right ppt structure 
    
    Args:
        dirname: str: name of the directory to convert to a powerpoint file
        target=None: the filename of the resulting pptx file
    """
    # check target
    if target is None:
        target = dirname + ".pptx"
    elif not target.endswith(".pptx"):
        target = target + ".pptx"
    # create zip (pptx) file
    with zipfile.ZipFile(target, "w") as zf:
        # go to folder where zip (pptx) file needs to be created
        with chdir(dirname):
            # add content of folder to zip (pptx) file
            for dir, subdirs, files in os.walk("."):
                zf.write(dir)
                for file in files:
                    zf.write(os.path.join(dir, file))


def dir2zip(dirname, target=None):
    """ Create zip file from folder 
    
    Args:
        dirname: str: name of the directory to convert to a zip file
        target=None: the filename of the resulting zip file.
    """
    # check target
    if target is None:
        target = dirname + ".zip"
    elif not target.endswith(".zip"):
        target = target + ".zip"
    # create zip file
    with zipfile.ZipFile(target, "w") as zf:
        # go to folder where zip file needs to be created
        with chdir(dirname):
            # add content of folder to zip file
            for dir, subdirs, files in os.walk("."):
                zf.write(dir)
                for file in files:
                    zf.write(os.path.join(dir, file))


def pptx2dir(filename, target=None):
    """ Create folder from pptx file
    
    Args:
        filename: str: name of the pptx file to unzip into a directory
        target=None: the filename of the resulting directory
    """
    # check filename:
    filename, ext = os.path.splitext(filename)
    if ext == "":
        ext = ".pptx"

    # check target
    if target is None:
        target = filename

    # unzip
    with zipfile.ZipFile(filename + ext, "r") as zf:
        zf.extractall(target)

    # parse dir for more readable xml files:
    for dir, subdirs, files in os.walk(target):
        for file in files:
            if file.endswith(".xml"):
                parse_xml(os.path.join(dir, file))


def zip2dir(filename, target=None):
    """ Create folder from zip file
    
    Args:
        filename: str: name of the zip file to unzip into a directory
        target=None: the filename of the resulting directory
    """
    # check filename
    filename, ext = os.path.splitext(filename)
    if ext == "":
        ext = ".zip"
    return pptx2dir(filename + ext, target)


def pptx2zip(filename, target=None):
    """ Create zip file from pptx file

    Args:
        filename: str: name of the pptx file to convert to a zip file
        target=None: the filename of the resulting zip file
    """
    # check filename:
    filename, ext = os.path.splitext(filename)
    if ext == "":
        ext = ".pptx"
    filename = filename + ext

    # check target
    if target is None:
        target = filename.replace(".pptx", ".zip")

    # rename
    if os.path.exists(target):
        os.remove(target)
    shutil.copy(filename, target)


def zip2pptx(filename, target=None):
    """ Create pptx file from zip file

    Args:
        filename: str: name of the zip file to convert to a pptx file
        target=None: the filename of the resulting pptx file
    """
    # check filename:
    filename, ext = os.path.splitext(filename)
    if ext == "":
        ext = ".zip"
    filename = filename + ext

    # check target
    if target is None:
        target = filename.replace(".zip", ".pptx")

    # rename
    if os.path.exists(target):
        os.remove(target)
    shutil.copy(filename, target)
