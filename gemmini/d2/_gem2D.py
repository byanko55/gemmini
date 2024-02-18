
from gemmini.misc import *
from gemmini.calc.coords import dist, interior_pixels
from gemmini.d2.transform2D import *

import copy

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

        Args:
            gem_type (str): explicit type of a geometric object
        """

        self.gem_type = gem_type
        self._op_queue = list()
        self._exterior = self._base_coords()
        self._interior = None
        self._density = None
        self._fill = False

    def _base_coords(self) -> np.ndarray:
        """
        Calculate the positions of original pixel's coordinate
        """
        raise NotImplementedError

    def coords(self) -> np.ndarray:
        """
        Returns a list of (x, y) coordinates for the pixels
        """
        update_interior = len(self._op_queue) > 0 or type(self._interior) == type(None)
        
        # Do transfrom operations at once, and save the intermediate results to `_exterior`
        while self._op_queue:
            args = self._op_queue.pop()
            
            if type(args) == tuple:
                op = args[0]
                self._exterior = op(self._exterior, *args[1:])
            else :
                op = args
                self._exterior = op(self._exterior)
        
        if not self._fill:
            return self._exterior
        
        if update_interior:
            self._interior = interior_pixels(self._exterior, self._density)
            
        return np.concatenate((self._exterior, self._interior), axis=0)

    def coordsXY(self) -> np.ndarray:
        """
        Returns a list of coordinates for each axis
        """
        cd = self.coords()
        
        return cd[:, 0], cd[:, 1]
    
    def copy(self) -> object:
        """
        Return a copy of the given geometric object.
        """
        gem = copy.deepcopy(self)
        return gem

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
    
    def fill(self, density:int = 16) -> None:
        """
        Draw interior pixels of geometric object
        
        Args:
            density (int): A higher value will result in more pixels.
        """
        self._fill = True
        self._density = density
    
    def scale(self, sx:float, sy:float = None) -> None:
        """
        Resizes the figure on 2D plane.

        Args:
            sx (float): the scaling factor to apply on the x-coordinate
            sy (float): the scaling factor to apply on the y-coordinate
        """
        self._op_queue.append((scale, sx, sy))
        
    def scaleX(self, s:float = None, **kwargs) -> None:
        """
        Resizes the figure along the x-axis (horizontally)

        Args:
            s | scale (float): the scaling factor to apply on the x-coordinate
        """
        s = assignArg("scaleX", [s], ['scale'], kwargs)
        
        self._op_queue.append((scaleX, s))
        
    def scaleY(self, s:float = None, **kwargs) -> None:
        """
        Resizes the figure along the y-axis (vertically)

        Args:
            s | scale (float): the scaling factor to apply on the y-coordinate
        """
        s = assignArg("scaleY", [s], ['scale'], kwargs)

        self._op_queue.append((scaleY, s))
        
    def translate(self, mx:float, my:float) -> None:
        """
        Re-locate the figure on the 2D plane

        Args:
            mx (float): represents shift along x-axis
            my (float): represents shift along y-axis
        """
        self._op_queue.append((translate, mx, my))
        
    def translateX(self, mx:float) -> None:
        """
        Re-locate the figure horizontally on the 2D plane

        Args:
            mx (float): represents shift along x-axis
        """
        self._op_queue.append((translateX, mx))
        
    def translateY(self, my:float) -> None:
        """
        Re-locate the figure vertically on the 2D plane

        Args:
            my (float): represents shift along y-axis
        """ 
        self._op_queue.append((translateY, my))
        
    def rotate(self, a:float = None, **kwargs) -> None:
        """
        Rotate the figure by `a` radian in the xy-plane (= z-axis).

        Args:
            a | angle (float): angle (in radian) of rotation
        """
        a = assignArg("rotate", [a], ['angle'], kwargs)
        
        self._op_queue.append((rotate, a))
        
    def rotateX(self, a:float = None, **kwargs) -> None:
        """
        Rotate the figure by `a` radian in the yz-plane (= x-axis).

        Args:
            a | angle (float): angle (in radian) of rotation
        """
        a = assignArg("rotateX", [a], ['angle'], kwargs)
        
        self._op_queue.append((rotateX, a))
        
    def rotateY(self, a:float = None, **kwargs) -> None:
        """
        Rotate the figure by `a` radian in the xz-plane (= y-axis).

        Args:
            a | angle (float): angle (in radian) of rotation
        """
        a = assignArg("rotateY", [a], ['angle'], kwargs)
        
        self._op_queue.append((rotateY, a))
        
    def rotateZ(self, a:float = None, **kwargs) -> None:
        """
        Rotate the figure by `a` radian in the xy-plane (= z-axis).

        Args:
            a | angle (float): angle (in radian) of rotation
        """
        a = assignArg("rotateZ", [a], ['angle'], kwargs)
        
        self._op_queue.append((rotateZ, a))
        
    def rotate3D(self, a1:float = None, a2:float = None, a3:float = None, **kwargs) -> None:
        """
        3D rotation

        Args:
            a1 | yaw (float): counterclockwise rotation about the z-axis
            a2 | pitch (float): counterclockwise rotation about the y-axis
            a3 | roll (float): counterclockwise rotation about the x-axis
        """
        a1, a2, a3 = assignArg(
            "rotate3D", 
            [a1, a2, a3], 
            ['yaw', 'pitch', 'roll'], 
            kwargs
        )
        
        self._op_queue.append((rotate3D, a1, a2, a3))
        
    def skew(self, a:float = None, ax:float=None, ay:float=None, **kwargs) -> None:
        """
        Skews the figure on the 2D plane.

        Args:
            a | angle (float): angle to use to distort the figure on the 2D plane 
                same with skew(coord, ax=`a`, ay=`a`)
            ax (float, optional): angle to use to distort the figure along the x-axis.
            ay (float, optional): angle to use to distort the figure along the y-axis
        """
        if 'angle' in kwargs:
            a = kwargs['angle']
            
        self._op_queue.append((skew, a, ax, ay))
        
    def skewX(self, a:float = None, **kwargs) -> None:
        """
        Skews the figure in the horizontal direction on the 2D plane

        Args:
            a | angle (float): angle (in radian) to use to distort the figure along the x-axis
        """
        a = assignArg("skewX", [a], ['angle'], kwargs)
        
        self._op_queue.append((skewX, a))
        
    def skewY(self, a:float = None, **kwargs) -> None:
        """
        Skews the figure in the vertical direction on the 2D plane

        Args:
            a | angle (float): angle (in radian) to use to distort the figure along the y-axis
        """
        a = assignArg("skewY", [a], ['angle'], kwargs)
        
        self._op_queue.append((skewY, a))
        
    def reflect(self, p:Tuple[float, float]) -> None:
        """
        Flip the figure about the specific point (x, y),
        and merge it with the original figure

        Args:
            p (tuple): a point along which to flip over
        """
        self._op_queue.append((reflect, p))
    
    def reflectX(self) -> None:
        """
        Flip the figure about the x-axis,
        and merge it with the original figure
        """
        self._op_queue.append((reflectX))
        
    def reflectY(self) -> None:
        """
        Flip the figure about the y-axis,
        and merge it with the original figure
        """
        self._op_queue.append((reflectY))
        
    def reflectXY(self) -> None:
        """
        Flip the figure about the origin (0, 0),
        and merge it with the original figure
        """
        self._op_queue.append((reflectXY))
        
    def reflectDiagonal(self) -> None:
        """
        Flip the figure about the line: y = x,
        and merge it with the original figure
        """
        self._op_queue.append((reflectDiagonal))
        
    def flip(self, p:Tuple[float, float]) -> None:
        """
        Flip about the given point (x, y)

        Args:
            p (tuple): a point along which to flip over
        """
        self._op_queue.append((flip, p))
        
    def flipX(self) -> None:
        """
        Flip about the x-axis
        """
        self._op_queue.append((flipX))
        
    def flipY(self) -> None:
        """
        Flip about the y-axis
        """
        self._op_queue.append((flipY))
        
    def flipXY(self) -> None:
        """
        Flip about the origin (0, 0)
        """
        self._op_queue.append((flipXY))
        
    def flipDiagonal(self) -> None:
        """
        Flip about the line: y = x 
        """
        self._op_queue.append((flipDiagonal))
        
    def dot(self, m:np.ndarray) -> None:
        """
        Dot product of its coordinates and a matrix with dimension: (2, 2)

        Args:
            m (np.ndarray): 2 x 2 matrix for the matrix multiplication
        """
        self._op_queue.append((dot, m))
        
    def distort(self, method='barrel', rate:float = 0.5) -> None:
        """
        Distorts the figure using various distorting methods.

        Args:
            method (string): it can be either `barrel` or `pincushion`.
                - barrel: magnification decreases with distance from the optical axis.
                - pincushion: magnification increases with the distance from the optical axis.
            rate (float) : distortion coefficients
        """
        self._op_queue.append((distort, method, rate))
        
    def focus(self, p:Tuple[float, float], rate:float = 0.5) -> None:
        """
        Pull the figure into a given pivot point

        Args:
            p (float, float): (x, y) positions of pivot point
            rate (float) : distortion factor to apply
        """
        self._op_queue.append((focus, p, rate))
        
    def shatter(self, p:Tuple[float, float], rate:float = 0.5) -> None:
        """
        Repel the figure away from a given pivot point

        Args:
            p (float, float): (x, y) positions of pivot point
            rate (float) : distortion factor to apply
        """
        self._op_queue.append((shatter, p, rate))

    def __len__(self) -> int:
        """
        Returns the number of pixels
        """
        raise NotImplementedError

    def __getitem__(self, item:int) -> Tuple[Any, Any]:
        coord = self.coords()

        return coord[item].tolist()