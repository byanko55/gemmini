from gemplib.misc import *
from gemplib.shape._gem import *

__all__ = [
    "Point"
]

class Point(Geometry):
    def __init__(
        self, 
        px:int, 
        py:int, 
        **kwargs
    ):
        """
        A single pixel

        Args:
            px (int): x-coordinate
            py (int): y-coordinate
        """
        super().__init__(gem_type="point", **kwargs)

        self.px = px
        self.py = py

    def coords(self):
        return np.array([[self.px, self.py]])

    def length(self):
        return 1