import os
import sys
import shutil
import zipfile

from contextlib import contextmanager

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

def dir2pptx(dirname, target=None):
  ''' Create ppt file from folder with right ppt structure '''
  # check target
  if target is None:
    target = dirname + '.pptx'
  elif not target.endswith('.pptx'):
    target = target + '.pptx'
  # create zip (pptx) file
  with zipfile.ZipFile(target, "w") as zf:
    # go to folder where zip (pptx) file needs to be created
    with chdir(dirname):
      # add content of folder to zip (pptx) file
      for dir, subdirs, files in os.walk('.'):
        zf.write(dir)
        for file in files:
          zf.write(os.path.join(dir, file))

def parse_xml(filename):
    ''' Parse xml file and introduce enters '''
    # check filename
    if not filename.endswith('.xml'):
        filename = filename + '.xml'
    
    # read content
    with open(filename, 'r') as file:
        content = file.read()
    
    # replace 
    content = content.replace('><','>\n<')

    # overwrite
    with open(filename, 'w') as file:
        file.write(content)

def pptx2dir(filename, target=None):
  ''' Create folder from pptx file '''
  # check filename:
  if filename.endswith('.pptx'):
    filename = filename.replace('.pptx','')
  
  # check target
  if target is None:
    target = filename

  # unzip
  with zipfile.ZipFile(filename+'.pptx', 'r') as zf:
    zf.extractall(target)

  # parse dir for more readable xml files:
  for dir, subdirs, files in os.walk(target):
    for file in files:
      if file.endswith('.xml'):
        parse_xml(os.path.join(dir,file))


if __name__ == '__main__':
    name = sys.argv[1]

    if sys.argv[2] == 'ppt':
      dir2pptx(name)

    if sys.argv[2] == 'dir':
      pptx2dir(name)