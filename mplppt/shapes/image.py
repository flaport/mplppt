#############
## Imports ##
#############

import os
import numpy as np
from matplotlib.pyplot import imread, imsave
from scipy.interpolate import interp2d

from .base import Object
from ..templates import IMAGE
from ..utils.strings import random_name
from ..utils.contextmanagers import chdir
from ..utils.constants import PIXELSPERPOINT
from ..utils.constants import POINTSPERINCH
from ..utils.mpl import get_plotting_area


###############
## Rectangle ##
###############


class Image(Object):
    """ An Image """

    def __init__(self, source, name="", x=0, y=0, cx=None, cy=None, slidesize=(6, 4)):
        name = ".".join(source.split(".")[:-1]) if name == "" else name
        Object.__init__(self, name=name, slidesize=slidesize)
        self.array = imread(source)
        self.id = random_name(5)
        self.source = source
        self.target = self.name + "_" + self.id + "." + source.split(".")[-1]
        self.x = x
        self.y = y

        self.cx = 10000 * self.array.shape[1] / PIXELSPERPOINT if cx is None else cx
        self.cy = 10000 * self.array.shape[0] / PIXELSPERPOINT if cy is None else cy
        self._xml = IMAGE

    def rels(self):
        """ Get relationship representation of the image together with the source location and the target location """
        rels = '<Relationship Id="{id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{target}"/>'
        rels = rels.format(id=self.id, target=self.target)
        return [(rels, self.array, self.target)]

    def xml(self):
        """ Get xml representation of the rectangle """
        xml = self._xml.format(
            name=self.name,
            x=int(self.x * PIXELSPERPOINT) + 1,
            y=int(self.y * PIXELSPERPOINT) + 1,
            cx=int(self.cx * PIXELSPERPOINT),
            cy=int(self.cy * PIXELSPERPOINT),
            id=self.id,
        )
        return xml


class Mesh(Image):
    """ Matplotlib QuadMesh (plt.pcolormesh) """

    @classmethod
    def from_mpl(cls, mpl_mesh):
        xlim = mpl_mesh.axes.get_xlim()
        ylim = mpl_mesh.axes.get_ylim()
        X = mpl_mesh._coordinates[:-1, :-1, 0]
        Y = mpl_mesh._coordinates[:-1, :-1, 1]
        xmin, xmax = max(np.min(X), min(xlim)), min(np.max(X), max(xlim))
        ymin, ymax = max(np.min(Y), min(ylim)), min(np.max(Y), max(ylim))

        Z = mpl_mesh._A.reshape(mpl_mesh._meshHeight, mpl_mesh._meshWidth).data

        # Get plotting area
        slide_x0, slide_x1, slide_y1, slide_y0 = get_plotting_area(mpl_mesh.figure)

        # Get slidesize from matplotlib figure
        slidesize = (mpl_mesh.figure.get_figwidth(), mpl_mesh.figure.get_figheight())

        # Translate plot data to locations on slide
        plot_x0, plot_x1 = mpl_mesh.axes.get_xlim()
        mx = (slide_x0 - slide_x1) / (plot_x0 - plot_x1)
        x = mx * (xmin - plot_x0) + slide_x0
        cx = mx * (xmax - xmin)
        if cx < 0:
            x += cx
            cx *= -1

        plot_y0, plot_y1 = mpl_mesh.axes.get_ylim()
        my = (slide_y0 - slide_y1) / (plot_y0 - plot_y1)
        y = my * (ymin - plot_y0) + slide_y0
        cy = my * (ymax - ymin)
        if cy < 0:
            y += cy
            cy *= -1

        id = random_name(5)
        _x, _y = np.where(((X > xmin) & (X < xmax) & (Y > ymin) & (Y < ymax)))
        imsave(id + ".png", Z[max(_x) : min(_x) : -1, min(_y) : max(_y)])

        mesh = cls(
            source=id + ".png", name=id, x=x, y=y, cx=cx, cy=cy, slidesize=slidesize
        )
        os.remove(id + ".png")
        mesh.id = id
        mesh.target = id + ".png"
        return mesh
