""" useful context managers for mplppt """

#############
## Imports ##
#############

import os
import shutil
from contextlib import contextmanager

from .strings import random_name


######################
## Context Managers ##
######################


@contextmanager
def chdir(path):
    """ Handy working directory changing context manager that returns to
    original folder if something goes wrong

    Args:
        path: str: path of folder to cd into
    """
    old_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_dir)


@contextmanager
def tempdir(source=None):
    """ Creates a temporary folder (empty if no source provided).
    The folder gets automatically removed if something goes wrong.

    Args:
        source: the source folder to copy into the temporary folder
    """
    dirname = random_name()
    if source is None:
        os.mkdir(dirname)
    else:
        shutil.copytree(source, dirname)
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)
