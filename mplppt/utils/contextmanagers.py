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
    """ 
  Handy working directory changing context manager that returns to 
  original folder if something goes wrong 
  """
    try:
        old_dir = os.getcwd()
        os.chdir(path)
        yield
    finally:
        os.chdir(old_dir)


@contextmanager
def tempdir(source=None):
    """
  Creates a temporary folder (empty if no source provided).
  The folder gets automatically removed if something goes wrong.
  """
    try:
        dirname = random_name()
        if source is None:
            os.mkdir(dirname)
        else:
            shutil.copytree(source, dirname)
        yield dirname
    finally:
        shutil.rmtree(dirname)
