import os
import string
import random
from contextlib import contextmanager

PIXELSPERPOINT = 12700

@contextmanager
def chdir(path):
  ''' 
  Handy working directory changing context manager that returns to 
  original folder if something goes wrong 
  '''
  old_dir = os.getcwd()
  os.chdir(path)
  yield
  os.chdir(old_dir)


def random_name(N=10):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def get_content(filename):
  with open(filename, 'r') as file:
    content = file.read()
  return content