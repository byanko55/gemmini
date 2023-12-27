from gemplib.misc import *
from gemplib.shape._gem import *

__all__ = [
    "Point"
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
        super().__init__(gem_type="Point", **kwargs)

        self.px = px
        self.py = py

    def coords(self) -> np.ndarray:
        return np.array([[self.px, self.py]])
    
    def size(self) -> float:
        return 0

    def __len__(self) -> int:
        return 1