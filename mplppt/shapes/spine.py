""" Matplotlib spine represented as a powerpoint line """


#############
## Imports ##
#############

import numpy as np
from scipy.interpolate import interp1d

from .line import Line
from ..templates import LINE
from ..utils.colors import color2hex
from ..utils.strings import random_name
from ..utils.constants import POINTSPERINCH
from ..utils.constants import PIXELSPERPOINT


###########
## Spine ##
###########
class Spine(Line):
    @classmethod
    def from_mpl(cls, mpl_spine):
        """ Create a line starting from a matplotlib Spine object
        
        Args:
            mpl_spine: the matplotlib spine object to convert to a powerpoint line
        
        """
        # Get slidesize from matplotlib figure
        slidesize = (mpl_spine.figure.get_figwidth(), mpl_spine.figure.get_figheight())

        # Get shape
        shape = np.array(mpl_spine.get_extents())

        # Create Line
        spine = cls(
            name="mplspine_" + random_name(5),
            shape=shape,
            lw=mpl_spine._linewidth,
            ec="000000",
            fc=None,
            closed=False,
            slidesize=slidesize,
        )
        return spine
