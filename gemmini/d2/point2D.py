from gemmini.misc import *
from gemmini.d2._gem2D import Geometry2D


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
        if not hasattr(self, 'gem_type'):
            self.gem_type = 'Pointcloud2D'

        self.points = np.array(points)
        
        if len(self.points.shape) != 2 or self.points.shape[1] != 2 :
            raise ValueError(" \
                [ERROR] Pointcloud2D: Input matrix does not match the format of 2D-point set \
            ")
        
        super().__init__(
            planar=False,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        return self.points

    def __len__(self) -> int:
        return len(self.points)
    
    def __hash__(self) -> int:
        return super().__hash__()


class Point2D(Pointcloud2D):
    @geminit()
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

        super().__init__(
            points=[[px, py]],
            **kwargs
        )
        
    def __hash__(self) -> int:
        return hash((self.gem_type, self.px, self.py))


class Grid(Pointcloud2D):
    @geminit({'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        h:float = None,
        w:float = None,
        n:Union[int, Tuple[int, int]] = 16,
        **kwargs
    ):
        """
        A four-sided polygon with four right angles
        
        Args:
            h | height (float): length of vertical sides
            w | width (float): length of horizontal sides
            n | num_dot (int | (int, int)): determines the number of row/column
                If a single number is given, then the grid will have equal number of rows and columns
                Or, you can give a tuple (N, M), to generate `N`-by-`M` grid
                ex) num_dot = (2,4): grid with 2 rows and 4 columns
        """
        self.h, self.w = h, w

        if isNumber(n):
            self.nr, self.nc = map(int, [n]*2)
        else :
            self.nr, self.nc = n

        if self.nr < 2 or self.nc < 2 :
            raise ValueError(" \
                [ERROR] Grid: each row/column should consist of at least 2 dots \
            ")
        
        x, y = np.meshgrid(
            np.linspace(-self.w/2, self.w/2, self.nc), 
            np.linspace(-self.h/2, self.h/2, self.nr)
        )

        x, y = x.flatten(), y.flatten()
        points = np.vstack((x, y)).T

        super().__init__(
            points=points,
            **kwargs
        )
    
    def __hash__(self) -> int:
        return hash((self.gem_type, self.h, self.w, self.nr, self.nc))