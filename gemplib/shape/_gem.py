
from gemplib.misc import *
from math import log10

class Geometry:
    def __init__(
        self,
        gem_type:str,
        **kwargs
    ) -> None:
        """
        Basic structure of gemplib geometry instance
        It also includes a collection of transformation operations.

        All subclasses should overwrite 
            1) `coords`, a list of (x, y) coordinates of vertices.
            2) `size`, indicating the diameter (or the longest distance between two different pixels).
            3) `__len__`, which is expected to return the diameter of the given geometry.
            4) `__getitem__`, supporting fetching a pixel point for a given index.

        Args:
            gem_type (str): explicit type of a geometric object
        """
        self.gem_type = gem_type

    def x_and_y(self) -> Tuple[Any, Any]:
        """
        Returns the list of pixel position on x axis and y axis, respectively  
        """
        cd = self.coords()
        return cd[:, 0], cd[:, 1]

    def coords(self) -> np.ndarray:
        """
        Returns a list of (x, y) coordinates for the pixels
        """
        raise NotImplementedError

    def size(self) -> float:
        """
        Returns the diameter
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """
        Returns the number of pixels
        """
        raise NotImplementedError

    def __getitem__(self, item:int) -> Tuple[Any, Any]:
        raise NotImplementedError