
from gemmini.misc import *
from gemmini.d2.transform2D import *
from gemmini.calc.coords import dist, interior_pixels, outer_product
from gemmini.calc.geometry import concave_hull

import copy
import random


def transform(func):
   def func_wrapper(self, *args, **kwargs):
       self._base_hash += get_hash(*args, **kwargs)
       self._exterior = None
       self._interior = None
       func(self, *args, **kwargs)
   return func_wrapper


class Geometry2D:
    def __init__(
        self,
        planar:bool,
        density:float = 16,
        **kwargs
    ) -> None:
        """
        Basic structure of gemmini geometry instance.
        It also includes a collection of transformation operations.

        All subclasses should overwrite 
            1) `_base_coords`, a list of original (x, y) coordinates of vertices.
            2) `__len__`, which is expected to return the diameter of the given geometry.

        Args:
            planar (bool): True, if the geometry has explicit boundary formed by its edges.
            density (float): density of points consisting of the geometry.
        """
        self._planar = planar
        self._exterior = None
        self._interior = None
        self._density = density
        self._base_hash = random.getrandbits(128)

        for attr_name in ['uS', 'h', 'w']:
            if hasattr(self, attr_name) and getattr(self, attr_name) <= 0 :
                raise ValueError(" \
                    [ERROR] %s: Arguments such as `size`, `height`, and `width` can't be non-positive. \
                "%(self.gem_type))

        self._points = self._base_coords()

        if not isinstance(self._points, np.ndarray):
            self._points = np.array(self._points)
        
        if len(self._points.shape) != 2 or self._points.shape[1] != 2 :
            raise ValueError(" \
                [ERROR] %s: Check every vertices to conform the 2D format (x, y). \
            "%(self.gem_type))

    def _base_coords(self) -> np.ndarray:
        """
        Calculate the positions of original pixel's coordinate.
        """
        raise NotImplementedError
    
    def interior(self, density:float = 16) -> np.ndarray:
        """
        Return the point grid enclosed by the exterior of the geometry.

        Args:
            gem_type (str): explicit type of a geometric object.
            density (float): density of points inside a result geometry.
        """
        if not self._planar:
            warnings.warn(" \
                [WARN] Can't find interior points from `%s` object \
                "%(self.gem_type)
            )
            
            return None

        if type(self._interior) != type(None) and self._density == density:
            return self._interior
        
        e = self.exterior()
        self._interior = interior_pixels(e, density=density)

        return self._interior
    
    def exterior(self) -> np.ndarray:
        """
        Return border of the geometric object.
        """
        if type(self._exterior) != type(None):
            return self._exterior

        exterior_points, _ = concave_hull(self._points)
        self._exterior = exterior_points

        return self._exterior

    def coords(self) -> np.ndarray:
        """
        Returns a list of (x, y) coordinates for the pixels (exterior only).
        """
        return self._points

    def coordsXY(self) -> np.ndarray:
        """
        Returns a list of coordinates for each axis.
        """
        return self._points[:, 0], self._points[:, 1]
    
    def coordsFull(self) -> np.ndarray:
        """
        Returns a list of (x, y) coordinates for the pixels (includes both interior & exterior).
        """
        _i = self.interior()
        _e = self.exterior()

        return np.concatenate((_i, _e), axis=0)
    
    def copy(self) -> object:
        """
        Return a copy of the given geometric object.
        """
        gem = copy.deepcopy(self)
        return gem

    def bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Border's coordinates on the X and Y axes that enclose a geometric object.

        Returns:
            (x_min, y_min, x_max, y_max): the minimum/maximum position of x, y axes.
        """
        xs, ys = self.coordsXY()

        return min(xs), min(ys), max(xs), max(ys)

    def center(self) -> Tuple[float, float]:
        """
        Returns The centroid of a geometric object.
        """
        xs, ys = self.coordsXY()

        return np.mean(xs), np.mean(ys)

    def dim(self) -> Tuple[float, float]:
        """
        Returns the width and height.
        """
        mx, my, Mx, My = self.bounding_box()

        return Mx-mx, My-my

    def rad(self) -> float:
        """
        Returns the diameter.
        """
        mx, my, Mx, My = self.bounding_box()

        return dist((mx, my), (Mx, My))/2
    
    @transform
    def scale(self, sx:float, sy:float = None) -> None:
        """
        Resizes the figure on 2D plane.

        Args:
            sx (float): the scaling factor to apply on the x-coordinate.
            sy (float): the scaling factor to apply on the y-coordinate.
        """
        self._points = scale(self._points, sx, sy)
        
    @transform
    def scaleX(self, s:float = None, **kwargs) -> None:
        """
        Resizes the figure along the x-axis (horizontally).

        Args:
            s | scale (float): the scaling factor to apply on the x-coordinate.
        """
        s = assignArg("scaleX", [s], ['scale'], kwargs)
        
        self._points = scaleX(self._points, s)
        
    @transform
    def scaleY(self, s:float = None, **kwargs) -> None:
        """
        Resizes the figure along the y-axis (vertically).

        Args:
            s | scale (float): the scaling factor to apply on the y-coordinate.
        """
        s = assignArg("scaleY", [s], ['scale'], kwargs)

        self._points = scaleY(self._points, s)
        
    @transform
    def translate(self, mx:float, my:float) -> None:
        """
        Re-locate the figure on the 2D plane.

        Args:
            mx (float): represents shift along x-axis.
            my (float): represents shift along y-axis.
        """
        self._points = translate(self._points, mx, my)
        
    @transform
    def translateX(self, mx:float) -> None:
        """
        Re-locate the figure horizontally on the 2D plane.

        Args:
            mx (float): represents shift along x-axis.
        """
        self._points = translateX(self._points, mx)
        
    @transform
    def translateY(self, my:float) -> None:
        """
        Re-locate the figure vertically on the 2D plane.

        Args:
            my (float): represents shift along y-axis.
        """ 
        self._points = translateY(self._points, my)
        
    @transform
    def rotate(self, a:float = None, **kwargs) -> None:
        """
        Rotate the figure by `a` radian in the xy-plane (= z-axis).

        Args:
            a | angle (float): angle (in radian) of rotation.
        """
        a = assignArg("rotate", [a], ['angle'], kwargs)
        
        self._points = rotate(self._points, a)
        
    @transform
    def rotateX(self, a:float = None, **kwargs) -> None:
        """
        Rotate the figure by `a` radian in the yz-plane (= x-axis).

        Args:
            a | angle (float): angle (in radian) of rotation.
        """
        a = assignArg("rotateX", [a], ['angle'], kwargs)

        self._points = rotateX(self._points, a)
        
    @transform
    def rotateY(self, a:float = None, **kwargs) -> None:
        """
        Rotate the figure by `a` radian in the xz-plane (= y-axis).

        Args:
            a | angle (float): angle (in radian) of rotation.
        """
        a = assignArg("rotateY", [a], ['angle'], kwargs)
        
        self._points = rotateY(self._points, a)
        
    @transform
    def rotateZ(self, a:float = None, **kwargs) -> None:
        """
        Rotate the figure by `a` radian in the xy-plane (= z-axis).

        Args:
            a | angle (float): angle (in radian) of rotation.
        """
        a = assignArg("rotateZ", [a], ['angle'], kwargs)
        
        self._points = rotateZ(self._points, a)
        
    @transform
    def rotate3D(self, a1:float = None, a2:float = None, a3:float = None, **kwargs) -> None:
        """
        3D rotation.

        Args:
            a1 | yaw (float): counterclockwise rotation about the z-axis.
            a2 | pitch (float): counterclockwise rotation about the y-axis.
            a3 | roll (float): counterclockwise rotation about the x-axis.
        """
        a1, a2, a3 = assignArg(
            "rotate3D", 
            [a1, a2, a3], 
            ['yaw', 'pitch', 'roll'], 
            kwargs
        )

        self._points = rotate3D(self._points, a1, a2, a3)
        
    @transform
    def skew(self, a:float = None, ax:float=None, ay:float=None, **kwargs) -> None:
        """
        Skews the figure on the 2D plane.

        Args:
            a | angle (float): angle to use to distort the figure on the 2D plane.
                same with skew(coord, ax=`a`, ay=`a`)
            ax (float, optional): angle to use to distort the figure along the x-axis.
            ay (float, optional): angle to use to distort the figure along the y-axis.
        """
        if 'angle' in kwargs:
            a = kwargs['angle']

        self._points = skew(self._points, a, ax, ay)
        
    @transform
    def skewX(self, a:float = None, **kwargs) -> None:
        """
        Skews the figure in the horizontal direction on the 2D plane.

        Args:
            a | angle (float): angle (in radian) to use to distort the figure along the x-axis.
        """
        a = assignArg("skewX", [a], ['angle'], kwargs)
        
        self._points = skewX(self._points, a)
        
    @transform
    def skewY(self, a:float = None, **kwargs) -> None:
        """
        Skews the figure in the vertical direction on the 2D plane.

        Args:
            a | angle (float): angle (in radian) to use to distort the figure along the y-axis.
        """
        a = assignArg("skewY", [a], ['angle'], kwargs)
        
        self._points = skewY(self._points, a)
        
    @transform
    def reflect(self, p:Tuple[float, float]) -> None:
        """
        Flip the figure about the specific point (x, y), and merge it with the original figure.

        Args:
            p (tuple): a point along which to flip over.
        """
        self._points = reflect(self._points, p)
    
    @transform
    def reflectX(self) -> None:
        """
        Flip the figure about the x-axis, and merge it with the original figure.
        """
        self._points = reflectX(self._points)
    
    @transform
    def reflectY(self) -> None:
        """
        Flip the figure about the y-axis, and merge it with the original figure.
        """
        self._points = reflectY(self._points)
        
    @transform
    def reflectXY(self) -> None:
        """
        Flip the figure about the origin (0, 0), and merge it with the original figure.
        """
        self._points = reflectXY(self._points)
        
    @transform
    def reflectDiagonal(self) -> None:
        """
        Flip the figure about the line: y = x, and merge it with the original figure.
        """
        self._points = reflectDiagonal(self._points)
        
    @transform
    def flip(self, p:Tuple[float, float]) -> None:
        """
        Flip about the given point (x, y).

        Args:
            p (tuple): a point along which to flip over.
        """
        self._points = flip(self._points, p)
        
    @transform
    def flipX(self) -> None:
        """
        Flip about the x-axis.
        """
        self._points = flipX(self._points)
        
    @transform
    def flipY(self) -> None:
        """
        Flip about the y-axis.
        """
        self._points = flipY(self._points)
        
    @transform
    def flipXY(self) -> None:
        """
        Flip about the origin (0, 0).
        """
        self._points = flipXY(self._points)
        
    @transform
    def flipDiagonal(self) -> None:
        """
        Flip about the line: y = x.
        """
        self._points = flipDiagonal(self._points)
        
    @transform
    def dot(self, m:np.ndarray) -> None:
        """
        Dot product of its coordinates and a matrix with dimension: (2, 2).

        Args:
            m (np.ndarray): 2 x 2 matrix for the matrix multiplication.
        """
        self._points = dot(self._points, m)
        
    @transform
    def distort(self, method='barrel', rate:float = 0.5) -> None:
        """
        Distorts the figure using various distorting methods.

        Args:
            method (string): it can be either `barrel` or `pincushion`.
                - barrel: magnification decreases with distance from the optical axis.
                - pincushion: magnification increases with the distance from the optical axis.
            rate (float) : distortion coefficients.
        """
        self._points = distort(self._points, method, rate)
        
    @transform
    def focus(self, p:Tuple[float, float], rate:float = 0.5) -> None:
        """
        Pull the figure into a given pivot point.

        Args:
            p (float, float): (x, y) positions of pivot point.
            rate (float) : distortion factor to apply.
        """
        self._points = focus(self._points, p, rate)
        
    @transform
    def shatter(self, p:Tuple[float, float], rate:float = 0.5) -> None:
        """
        Repel the figure away from a given pivot point.

        Args:
            p (float, float): (x, y) positions of pivot point.
            rate (float) : distortion factor to apply.
        """
        self._points = shatter(self._points, p, rate)

    def area(self) -> float:
        """
        Return the area enclosed by the geometric object.
        """
        if not self._planar:
            warnings.warn(" \
                [WARN] area: %s does not support calculating the area \
            "%(self.gem_type))
            
            return 0
        
        _ep, _ = concave_hull(self.coords())
        
        if len(_ep) <= 2 :
            return 0
        
        s = 0
        
        for i in range(1, len(_ep)-1):
            s += outer_product(_ep[0], _ep[i], _ep[i+1])/2
            
        return abs(s)

    def __len__(self) -> int:
        """
        Returns the number of pixels.
        """
        raise NotImplementedError

    def __getitem__(self, item:int) -> Tuple[Any, Any]:
        return self._points[item].tolist()
    
    def __bool__(self) -> bool:
        return len(self._points) > 0
    
    def __str__(self) -> str:
        return self.gem_type
    
    def __and__(self, other) -> object:
        return intersect((self, other))

    def __or__(self, other) -> object:
        return union((self, other))

    def __sub__(self, other) -> object:
        return differ(self, other)

    def __xor__(self, other) -> object:
        return symmetric_differ(self, other)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Geometry2D):
            return False

        return type(other) == type(self) and np.array_equal(self.exterior(), other.exterior())

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        return self._base_hash
    

def union(figures=Tuple[Geometry2D, ...], density:int = 16, **kwargs) -> Geometry2D:
    raise NotImplementedError(" \
        [ERROR] union: Tried to call a function unsupported, but it will be updated soon. \
    ")


def intersect(figures=Tuple[Geometry2D, ...], density:int = 16, **kwargs) -> Geometry2D:
    raise NotImplementedError(" \
        [ERROR] intersect: Tried to call a function unsupported, but it will be updated soon. \
    ")


def differ(fa:Geometry2D, fb:Geometry2D, density:int = 16, **kwargs) -> Geometry2D:
    raise NotImplementedError(" \
        [ERROR] differ: Tried to call a function unsupported, but it will be updated soon. \
    ")


def symmetric_differ(fa:Geometry2D, fb:Geometry2D, density:int = 16, **kwargs) -> Geometry2D:
    raise NotImplementedError(" \
        [ERROR] symmetric_differ: Tried to call a function unsupported, but it will be updated soon. \
    ")


def complement(f:Geometry2D, density:int = 16, **kwargs) -> Geometry2D:
    raise NotImplementedError(" \
        [ERROR] complement: Tried to call a function unsupported, but it will be updated soon. \
    ")