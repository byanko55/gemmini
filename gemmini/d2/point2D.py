from gemmini.misc import *
from gemmini.d2._gem2D import *

class Point2D(Geometry2D):
    def __init__(
        self, 
        px:float, 
        py:float, 
        **kwargs
    ) -> None:
        """
        A single pixel

        Args:
            px (float): x-coordinate
            py (float): y-coordinate
        """

        gem_type = self.__class__.__name__

        self.px = px
        self.py = py
        
        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
        return np.array([[self.px, self.py]])

    def __len__(self) -> int:
        return 1
    

class Pointcloud2D(Geometry2D):
    def __init__(
        self,
        points:Union[list, np.ndarray],
        **kwargs
    ) -> None:
        """
        A discrete set of data points in 2D space

        Args:
            points (list): set of cartesian coordinates (x, y)
        """

        gem_type = self.__class__.__name__

        self.points = np.array(points)
        
        if len(self.points.shape) != 2 or self.points.shape[1] != 2 :
            raise ValueError(" \
                [ERROR] %s: check every points to conform the 2D format (x, y) \
            "%(gem_type))
        
        super().__init__(gem_type=gem_type, **kwargs)
        
    def _base_coords(self) -> np.ndarray:
        return self.points

    def __len__(self) -> int:
        return len(self.points)