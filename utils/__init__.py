import os
import string
import random
import shutil
from contextlib import contextmanager

PIXELSPERINCH = 914400
PIXELSPERPOINT = 12700
POINTSPERINCH = PIXELSPERINCH//PIXELSPERPOINT

MPLCOLORS = {'C0': '1f77b4', 'C1': 'ff7f0e', 'C2': '2ca02c', 'C3': 'd62728', 'C4': '9467bd', 'C5': '8c564b', 'C6': 'e377c2', 'C7': '7f7f7f', 'C8': 'bcbd22', 'C9': '17becf', 'aliceblue': 'F0F8FF', 'antiquewhite': 'FAEBD7', 'aqua': '00FFFF', 'aquamarine': '7FFFD4', 'azure': 'F0FFFF', 'beige': 'F5F5DC', 'bisque': 'FFE4C4', 'black': '000000', 'blanchedalmond': 'FFEBCD', 'blue': '0000FF', 'blueviolet': '8A2BE2', 'brown': 'A52A2A', 'burlywood': 'DEB887', 'cadetblue': '5F9EA0', 'chartreuse': '7FFF00', 'chocolate': 'D2691E', 'coral': 'FF7F50', 'cornflowerblue': '6495ED', 'cornsilk': 'FFF8DC', 'crimson': 'DC143C', 'cyan': '00FFFF', 'darkblue': '00008B', 'darkcyan': '008B8B', 'darkgoldenrod': 'B8860B', 'darkgray': 'A9A9A9', 'darkgreen': '006400', 'darkgrey': 'A9A9A9', 'darkkhaki': 'BDB76B', 'darkmagenta': '8B008B', 'darkolivegreen': '556B2F', 'darkorange': 'FF8C00', 'darkorchid': '9932CC', 'darkred': '8B0000', 'darksalmon': 'E9967A', 'darkseagreen': '8FBC8F', 'darkslateblue': '483D8B', 'darkslategray': '2F4F4F', 'darkslategrey': '2F4F4F', 'darkturquoise': '00CED1', 'darkviolet': '9400D3', 'deeppink': 'FF1493', 'deepskyblue': '00BFFF', 'dimgray': '696969', 'dimgrey': '696969', 'dodgerblue': '1E90FF', 'firebrick': 'B22222', 'floralwhite': 'FFFAF0', 'forestgreen': '228B22', 'fuchsia': 'FF00FF', 'gainsboro': 'DCDCDC', 'ghostwhite': 'F8F8FF', 'gold': 'FFD700', 'goldenrod': 'DAA520', 'gray': '808080', 'green': '008000', 'greenyellow': 'ADFF2F', 'grey': '808080', 'honeydew': 'F0FFF0', 'hotpink': 'FF69B4', 'indianred': 'CD5C5C', 'indigo': '4B0082', 'ivory': 'FFFFF0', 'khaki': 'F0E68C', 'lavender': 'E6E6FA', 'lavenderblush': 'FFF0F5', 'lawngreen': '7CFC00', 'lemonchiffon': 'FFFACD', 'lightblue': 'ADD8E6', 'lightcoral': 'F08080', 'lightcyan': 'E0FFFF', 'lightgoldenrodyellow': 'FAFAD2', 'lightgray': 'D3D3D3', 'lightgreen': '90EE90', 'lightgrey': 'D3D3D3', 'lightpink': 'FFB6C1', 'lightsalmon': 'FFA07A', 'lightseagreen': '20B2AA', 'lightskyblue': '87CEFA', 'lightslategray': '778899', 'lightslategrey': '778899', 'lightsteelblue': 'B0C4DE', 'lightyellow': 'FFFFE0', 'lime': '00FF00', 'limegreen': '32CD32', 'linen': 'FAF0E6', 'magenta': 'FF00FF', 'maroon': '800000', 'mediumaquamarine': '66CDAA', 'mediumblue': '0000CD', 'mediumorchid': 'BA55D3', 'mediumpurple': '9370DB', 'mediumseagreen': '3CB371', 'mediumslateblue': '7B68EE', 'mediumspringgreen': '00FA9A', 'mediumturquoise': '48D1CC', 'mediumvioletred': 'C71585', 'midnightblue': '191970', 'mintcream': 'F5FFFA', 'mistyrose': 'FFE4E1', 'moccasin': 'FFE4B5', 'navajowhite': 'FFDEAD', 'navy': '000080', 'oldlace': 'FDF5E6', 'olive': '808000', 'olivedrab': '6B8E23', 'orange': 'FFA500', 'orangered': 'FF4500', 'orchid': 'DA70D6', 'palegoldenrod': 'EEE8AA', 'palegreen': '98FB98', 'paleturquoise': 'AFEEEE', 'palevioletred': 'DB7093', 'papayawhip': 'FFEFD5', 'peachpuff': 'FFDAB9', 'peru': 'CD853F', 'pink': 'FFC0CB', 'plum': 'DDA0DD', 'powderblue': 'B0E0E6', 'purple': '800080', 'rebeccapurple': '663399', 'red': 'FF0000', 'rosybrown': 'BC8F8F', 'royalblue': '4169E1', 'saddlebrown': '8B4513', 'salmon': 'FA8072', 'sandybrown': 'F4A460', 'seagreen': '2E8B57', 'seashell': 'FFF5EE', 'sienna': 'A0522D', 'silver': 'C0C0C0', 'skyblue': '87CEEB', 'slateblue': '6A5ACD', 'slategray': '708090', 'slategrey': '708090', 'snow': 'FFFAFA', 'springgreen': '00FF7F', 'steelblue': '4682B4', 'tan': 'D2B48C', 'teal': '008080', 'thistle': 'D8BFD8', 'tomato': 'FF6347', 'turquoise': '40E0D0', 'violet': 'EE82EE', 'wheat': 'F5DEB3', 'white': 'FFFFFF', 'whitesmoke': 'F5F5F5', 'yellow': 'FFFF00', 'yellowgreen': '9ACD32', 'tab:blue': '1f77b4', 'tab:orange': 'ff7f0e', 'tab:green': '2ca02c', 'tab:red': 'd62728', 'tab:purple': '9467bd', 'tab:brown': '8c564b', 'tab:pink': 'e377c2', 'tab:gray': '7f7f7f', 'tab:olive': 'bcbd22', 'tab:cyan': '17becf', 'tab:grey': '7f7f7f', 'b': '0000FF', 'g': '007F00', 'r': 'FF0000', 'c': '00BFBF', 'm': 'BF00BF', 'y': 'BFBF00', 'k': '000000', 'w': 'FFFFFF'}

ALIGNMENTS = {'top':'t','bottom':'b','btm':'b','t':'t','b':'b','c':'c','ctr':'c','center':'c', 'center_baseline':'c', 'baseline':'b', 'left':'l','right':'r','l':'l','r':'r'}


def random_name(N=10):
  return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))

@contextmanager
def chdir(path):
  ''' 
  Handy working directory changing context manager that returns to 
  original folder if something goes wrong 
  '''
  try:
    old_dir = os.getcwd()
    os.chdir(path)
    yield
  finally:
    os.chdir(old_dir)


@contextmanager
def tempdir(source=None):
  '''
  Creates a temporary folder (empty if no source provided).
  The folder gets automatically removed if something goes wrong.
  '''
  try:
    dirname = random_name()
    if source is None:
      os.mkdir(dirname)
    else:
      shutil.copytree(source, dirname)
    yield dirname
  finally:
    shutil.rmtree(dirname)


def get_content(filename):
  with open(filename, 'r') as file:
    content = file.read()
  return content

def rgb2hex(tup, max=1):
  tup = [int(c*255/max) for c in tup]
  color = ''
  for c in tup:
    if c < 16:
      c = '0'+hex(c)[-1:]
    else:
      c = hex(c)[-2:]
    color += c
  return color.upper()

def rgba2hex(tup, max=1):
  tup = [int(c*255/max) for c in tup]
  if tup[-1] == 0:
    return None
  return rgb2hex(tup[:-1], max=255)

def color2hex(color):    
  if type(color) is str:
    if len(color) == 6:
      return color
    elif len(color) == 7 and color[0] == '#':
      return color[1:]
    elif color in MPLCOLORS:
      return MPLCOLORS[color]
  else:
    if type(color) is int:
      return rgb2hex((color,color,color), max=255)
    if type(color) is float:
      return rgb2hex((color,color,color))
    if len(color) == 4:
      return rgba2hex(color)
    if len(color) == 3:
      return rgb2hex(color)
  raise ValueError('invalid color '+str(color))

