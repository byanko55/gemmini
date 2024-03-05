from gemmini.misc import *
from gemmini.d2._gem2D import Geometry2D


class PointSet2D(Geometry2D):
    def __init__(
        self,
        points:Union[list, np.ndarray],
        planar:bool = False,
        **kwargs
    ) -> None:
        """
        A discrete set of data points in 2D space.

        Args:
            points (list): set of cartesian coordinates (x, y).
            planar (bool): True, if the geometry has explicit boundary formed by its edges.
        """
        if not hasattr(self, 'gem_type'):
            self.gem_type = 'PointSet2D'

        self.points = np.array(points)
        
        if len(self.points.shape) != 2 or self.points.shape[1] != 2 :
            raise ValueError(" \
                [ERROR] PointSet2D: Input matrix does not match the format of 2D-point set. \
            ")
        
        super().__init__(
            planar=planar,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        return self.points
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [], []

    def __len__(self) -> int:
        return len(self.points)
    
    def __hash__(self) -> int:
        return super().__hash__()


class Point2D(PointSet2D):
    @geminit()
    def __init__(
        self, 
        px:float, 
        py:float, 
        **kwargs
    ) -> None:
        """
        A single pixel.

        Args:
            px (float): x-coordinate.
            py (float): y-coordinate.
        """
        self.px = px
        self.py = py

        super().__init__(
            points=[[px, py]],
            planar=False,
            **kwargs
        )
        
    def __hash__(self) -> int:
        return hash((self.gem_type, self.px, self.py))


class Pointcloud2D(PointSet2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:int = 16,
        **kwargs
    ) -> None:
        """
        Points that randomly scattered in a 2D Euclidean space.
        
        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): maximum vertical distance.
            w | width (float): maximum horizontal distance.
            n | num_dot (int): determines how many dots consist of the point cloud.
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
        
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Pointcloud2D: Argument `size` must be either a single number or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]

        points = np.random.rand(self.nD, 2)
        points[:, 0] *= self.w
        points[:, 1] *= self.h

        super().__init__(
            points=points,
            planar=False,
            **kwargs
        )
        
    def __hash__(self) -> int:
        return hash((self.gem_type, self.h, self.w, self.nD))


class Grid(PointSet2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:Union[int, Tuple[int, int]] = 16,
        **kwargs
    ) -> None:
        """
        A four-sided polygon with four right angles.
        
        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): length of vertical sides.
            w | width (float): length of horizontal sides.
            n | num_dot (int | (int, int)): determines the number of row/column.
                If a single number is given, then the grid will have equal number of rows and columns.
                Or, you can give a tuple (N, M), to generate `N`-by-`M` grid.
                ex) num_dot = (2,4): grid with 2 rows and 4 columns
        """
        self.h, self.w = h, w
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
        
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Grid: Argument `size` must be either a single number or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]

        if isNumber(n):
            self.nr, self.nc = map(int, [n]*2)
        else :
            self.nr, self.nc = n

        if self.nr < 2 or self.nc < 2 :
            raise ValueError(" \
                [ERROR] Grid: Each row/column should consist of at least 2 dots. \
            ")
        
        x, y = np.meshgrid(
            np.linspace(-self.w/2, self.w/2, self.nc), 
            np.linspace(-self.h/2, self.h/2, self.nr)
        )

        x, y = x.flatten(), y.flatten()
        points = np.vstack((x, y)).T

        super().__init__(
            points=points,
            planar=False,
            **kwargs
        )
    
    def __hash__(self) -> int:
        return hash((self.gem_type, self.h, self.w, self.nr, self.nc))