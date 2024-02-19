from gemmini.misc import *
from gemmini.calc.coords import _isNumber
from gemmini.d2._gem2D import *


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
        gem_type = 'Pointcloud'

        if 'gem_type' in kwargs:
            gem_type = kwargs['gem_type']
            del kwargs['gem_type']

        self.points = np.array(points)
        
        if len(self.points.shape) != 2 or self.points.shape[1] != 2 :
            raise ValueError(" \
                [ERROR] %s: check every points to conform the 2D format (x, y) \
            "%(gem_type))
        
        super().__init__(gem_type=gem_type, **kwargs)

    def area(self) -> float:
        warnings.warn("[WARN] Computing area is not available for this geometry class")
        return 0
        
    def fill(self) -> None:
        warnings.warn("[WARN] Drawing interior pixels is not available for this geometry class")
        
    def _base_coords(self) -> np.ndarray:
        return self.points

    def __len__(self) -> int:
        return len(self.points)


class Point2D(Pointcloud2D):
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

        super().__init__(points=[[px, py]], gem_type=gem_type, **kwargs)


class Grid(Pointcloud2D):
    def __init__(
        self,
        h:float = None,
        w:float = None,
        nD:Union[int, Tuple[int, int]] = None,
        **kwargs
    ):
        """
        A four-sided polygon with four right angles.
        
        Args:
            h | height (float): length of vertical sides
            w | width (float): length of horizontal sides
            nD | num_dot (int | (int, int)): number of dots consisting of a row/column
                If a single numeric value is given, then both the row and column have the same number of dots.
                Or, you can determine the number of dots in each sides differently by giving a tuple for the `num_dot` argument. 
                ex) num_dot = (2,4): grid with 2 rows and 4 columns
        """
        gem_type = self.__class__.__name__

        self.h, self.w, nD = assignArg(
            gem_type, 
            [h, w, nD], 
            ['height', 'width', 'num_dot'], 
            kwargs
        )

        if _isNumber(nD):
            self.nr, self.nc = map(int, [nD]*2)
        else :
            self.nr, self.nc = nD

        if self.nr < 2 or self.nc < 2 :
            raise ValueError("[ERROR] %s: each row/column should consist of at least 2 dots"%(gem_type))
        
        x, y = np.meshgrid(
            np.linspace(-self.w/2, self.w/2, self.nc), 
            np.linspace(-self.h/2, self.h/2, self.nr)
        )

        x, y = x.flatten(), y.flatten()
        points = np.vstack((x, y)).T

        super().__init__(points=points, gem_type=gem_type, **kwargs)