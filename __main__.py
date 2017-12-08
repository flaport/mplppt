import sys
from convert import dir2pptx, pptx2dir

if sys.argv[2] == 'dir':
    pptx2dir(sys.argv[1])

if sys.argv[2] == 'ppt':
    dir2pptx(sys.argv[1])