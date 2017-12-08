import os
import string
import random
from contextlib import contextmanager

PIXELSPERINCH = 914400
PIXELSPERPOINT = 12700
POINTSPERINCH = PIXELSPERINCH//PIXELSPERPOINT

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
  return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))

def get_content(filename):
  with open(filename, 'r') as file:
    content = file.read()
  return content

def rgba2hex(tup):
  tup = [int(c*255) for c in tup]
  if tup[-1] == 0:
    return None
  color = hex(tup[0])[-2:] + hex(tup[1])[-2:] + hex(tup[2])[-2:]
  return color