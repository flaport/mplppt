#############
## Imports ##
#############

import os
import matplotlib as mpl
from matplotlib.pyplot import gcf
from matplotlib.pyplot import findobj
from matplotlib.pyplot import savefig as _savefig

from .shapes import Line
from .shapes import Text
from .shapes import Mesh
from .shapes import Group
from .shapes import Canvas
from .shapes import Polygon
from .shapes import Rectangle
from .utils.string import random_name


########################
## The Magic Function ##
########################

# This is te function this repository is all about

def savefig(filename, fig=None, canvas=dict(lw=0.8, ec='000000', fc='ffffff', axis=True)):
  ''' Export a matplotlib figure to a pptx file '''
  # Get figure to save
  if fig is None:
    fig = gcf()
    
  # Create ppt group
  p = Group(objects=[])
  
  # Parse mpl objects:
  for obj in findobj(fig):
    # only keep objects that have an axis:
    if obj.axes is not None:
      # convert lines:
      if type(obj) is mpl.lines.Line2D:
        p += Line.from_mpl(obj)
      # convert rectangles:
      if type(obj) is mpl.patches.Rectangle:
        p += Rectangle.from_mpl(obj)
      # convert polygons
      if type(obj) is mpl.patches.Polygon:
        p += Polygon.from_mpl(obj)
      # convert text
      if type(obj) is mpl.text.Text:
        p += Text.from_mpl(obj)
      # convert pcolormesh
      if type(obj) is mpl.collections.QuadMesh:
        p += Mesh.from_mpl(obj)
        
  # create a canvas
  # TODO: Create this with less parameters
  if canvas:
    # [HACK] Axis needs to be visualized by plotting the figure first. We choose png export:
    if canvas['axis']:
      fn = random_name() + '.png'
      _savefig(fn)
      os.remove(fn)
    canvas = Canvas.from_mpl(fig.axes[0], **canvas)
    p += canvas
  
  # save powerpoint group
  p.save(filename)
  
  # return powerpoint group
  return p


############################
## Other Useful Functions ##
############################

import pickle

def picklefig(filename, fig):
  with open(filename, 'wb') as file:
    pickle.dump((fig, fig.canvas), file)

def loadpicklefig(filename):
  with open(filename, 'rb') as file:
    fig, canvas = pickle.load(file, encoding='latin1')
  fig.canvas = canvas
  return fig