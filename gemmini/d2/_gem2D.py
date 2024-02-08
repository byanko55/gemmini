
from gemmini.misc import *
from gemmini.calc.coords import dist

class Geometry2D:
    def __init__(
        self,
        gem_type:str,
        **kwargs
    ) -> None:
        """
        Basic structure of gemmini geometry instance
        It also includes a collection of transformation operations.

        All subclasses should overwrite 
            1) `_base_coords`, a list of original (x, y) coordinates of vertices.
            2) `__len__`, which is expected to return the diameter of the given geometry.
            3) `__getitem__`, supporting fetching a pixel point for a given index.

        Args:
            gem_type (str): explicit type of a geometric object
        """

        self.gem_type = gem_type
        self._op_queue = list()
        self._coords = self._base_coords()

    def _base_coords(self) -> np.ndarray:
        """
        Calculate the positions of original pixel's coordinate
        """
        raise NotImplementedError

    def coords(self) -> np.ndarray:
        """
        Returns a list of (x, y) coordinates for the pixels
        """
        # Do transfrom operations at once, and save the intermediate results to `_coords`
        for op in self._op_queue:
            continue
        
        return self._coords

    def coordsXY(self) -> np.ndarray:
        """
        Returns a list of coordinates for each axis
        """
        cd = self.coords()
        
        return cd[:, 0], cd[:, 1]

    def bounding_box(self) -> Tuple[float, float, float, float]:
        """
        border's coordinates on the X and Y axes that enclose a geometric object

        Returns:
            (x_min, y_min, x_max, y_max): the minimum/maximum position of x, y axes
        """
        xs, ys = self.coordsXY()

        return min(xs), min(ys), max(xs), max(ys)

    def center(self) -> Tuple[float, float]:
        """
        Returns The centroid of a geometric object
        """
        xs, ys = self.coordsXY()

        return np.mean(xs), np.mean(ys)

    def dim(self) -> Tuple[float, float]:
        """
        Returns the width and height
        """
        mx, my, Mx, My = self.bounding_box()

        return Mx-mx, My-my

    def rad(self) -> float:
        """
        Returns the diameter
        """
        mx, my, Mx, My = self.bounding_box()

        return dist((mx, my), (Mx, My))/2

    def __len__(self) -> int:
        """
        Returns the number of pixels
        """
        raise NotImplementedError

    def __getitem__(self, item:int) -> Tuple[Any, Any]:
        raise NotImplementedError