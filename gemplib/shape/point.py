from gemplib.misc import *
from gemplib.shape._gem import *
from gemplib.shape.coords import dist

__all__ = [
    "Point",
    "Pointcloud"
]

class Point(Geometry):
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
        self.px = px
        self.py = py
        
        super().__init__(gem_type="Point", **kwargs)

    def coords(self) -> np.ndarray:
        return np.array([[self.px, self.py]])
    
    def size(self) -> float:
        return 0

    def __len__(self) -> int:
        return 1
    

class Pointcloud(Geometry):
    def __init__(
        self,
        points:Union[list, np.ndarray],
        **kwargs
    ) -> None:
        """
        A discrete set of data points in 2D space

        Args:
            points (Union[list, np.ndarray]): set of cartesian coordinates (x, y)
        """
        self.points = np.array(points)
        
        if len(self.points.shape) != 2 or self.points.shape[1] != 2 :
            raise ValueError(" \
                [ERROR] Pointcloud: check every points to conform the 2D format (x, y) \
            ")
        
        super().__init__(gem_type="Pointcloud", **kwargs)
        
    def coords(self) -> np.ndarray:
        return self.points
    
    def size(self) -> float:
        mx, my, Mx, My = bounding_box(self)
        return dist((mx, my), (Mx, My))

    def __len__(self) -> int:
        return len(self.points)