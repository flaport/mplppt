import sys; sys.path.append('..')

import mplppt

rect = mplppt.ppt.Rectangle()
shape = mplppt.ppt.Line()
ppt = rect + shape
ppt.save('test.pptx')