import sys; sys.path.append('..')

import mplppt

rect = mplppt.ppt.Rectangle()
shape = mplppt.ppt.Shape()
ppt = rect + shape
ppt.save('test.pptx')