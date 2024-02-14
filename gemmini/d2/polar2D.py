from gemmini.misc import *
from gemmini.d2._gem2D import *
from gemmini.calc.coords import polar_pixels

class Circle(Geometry2D):
    def __init__(
        self,
        r:float = None,
        nD:int = None,
        **kwargs
    ):
        """
        A circle

        Args:
            r | radius (float): radius of a circle
            nD | num_dot (int): number of dots consisting of the border of a circle
        """

        gem_type = self.__class__.__name__
        
        self.rD, self.nD = assignArg(
            gem_type, 
            [r, nD], 
            ['radius', 'num_dot'], 
            kwargs
        )

        super().__init__(gem_type=gem_type, polar=True, **kwargs)
        
    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*np.ones_like(theta)

        coord = polar_pixels(rad, theta)

        return coord

    def __len__(self) -> int:
        return self.nD
    
class Arc(Geometry2D):
    def __init__(
        self,
        r:float = None,
        nD:int = None,
        a:float = None, 
        **kwargs
    ):
        """
        A segment of a differentiable curve

        Args:
            r | radius (float): radius of an arc
            nD | num_dot (int): number of dots consisting of an arc
            a | angle (float): interior angle (unit: degrees, °) of an arc
        """

        gem_type = self.__class__.__name__
        
        self.rD, self.nD, self.aG = assignArg(
            gem_type, 
            [r, nD, a], 
            ['radius', 'num_dot', 'angle'], 
            kwargs
        )

        super().__init__(gem_type=gem_type, polar=True, **kwargs)

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, min(360, self.aG)*np.pi/180, self.nD)
        rad = self.rD*np.ones_like(theta)

        coord = polar_pixels(rad, theta)

        return coord

    def __len__(self) -> int:
        return self.nD
    
class Ellipse(Geometry2D):
    def __init__(
        self,
        h:float = None,
        w:float = None,
        nD:int = None,
        **kwargs
    ):
        """
        Ellipse is a plane curve surrounding two focal points, such that for all points on the curve, 
        the sum of the two distances to the focal points is a constant.

        Args:
            h | height (float): length of minor axis
            w | width (float): length of major axis
            nD | num_dot (int): number of dots consisting of the border of a ellipse
        """

        gem_type = self.__class__.__name__

        self.rH, self.rW, self.nD = assignArg(
            gem_type, 
            [h, w, nD], 
            ['height', 'width', 'num_dot'], 
            kwargs
        )

        super().__init__(gem_type=gem_type, polar=True, **kwargs)

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        coord = np.stack((self.rW*np.cos(theta), -self.rH*np.sin(theta)), axis=1)/2
        
        return coord

    def __len__(self) -> int:
        return self.nD
    
class Spiral(Geometry2D):
    def __init__(
        self,
        r:float = None,
        nD:int = None,
        a:float = None,
        **kwargs
    ):
        """
        A curve on a plane that winds around a fixed center point 
        at a continuously increasing or decreasing distance from the point.

        Args:
            r | radius (float): radius of the spiral
            nD | num_dot (int): number of dots consisting of the curve
            a | angle (float): interior angle (unit: radian)
        """
        
        gem_type = self.__class__.__name__

        self.rD, self.nD, self.aG = assignArg(
            gem_type, 
            [r, nD, a], 
            ['radius', 'num_dot', 'angle'], 
            kwargs
        )

        self.draw_func = None

        if 'draw_func' in kwargs:
            self.draw_func = kwargs['draw_func']

        super().__init__(gem_type=gem_type, polar=True, **kwargs)

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, self.aG, self.nD+1)[1:]

        if self.draw_func == None:
            rad = self.rD*theta/self.aG
            coord = polar_pixels(rad, theta)
            
            return coord
        else :
            return self.draw_func(self.rD, theta)

    def __len__(self) -> int:
        return self.nD
    
def HyperbolicSpiral(
    r:float = None,
    nD:int = None,
    a:float = None,
    **kwargs
):
    """
    A type of spiral with a pitch angle that increases with distance from its center.

    Args:
        r | radius (float): radius of the spiral
        nD | num_dot (int): number of dots consisting of the curve
        a | angle (float): interior angle (unit: radian)
    """
    def _draw_curve(radius, theta):
        rad = radius * theta[0]/theta
        coord = polar_pixels(rad, theta)

        return coord

    return Spiral(r, nD, a, draw_func=_draw_curve, **kwargs)

def ParabolicSpiral(
    r:float = None,
    nD:int = None,
    a:float = None,
    **kwargs
):
    """
    A plane curve with the property that the area 
    between any two consecutive full turns around the spiral is invariant.

    Args:
        r | radius (float): radius of the spiral
        nD | num_dot (int): number of dots consisting of the curve
        a | angle (float): interior angle (unit: radian)
    """
    def _draw_curve(radius, theta):
        log_theta = np.sqrt(theta)
        rad = radius * log_theta/log_theta[-1]

        if len(log_theta)%2 == 0 :
            coord_pos = polar_pixels(rad[::2], theta[::2])
            coord_neg = polar_pixels(-rad[::2], theta[::2])
        else :
            coord_pos = polar_pixels(rad[1::2], theta[1::2])
            coord_neg = polar_pixels(-rad[::2], theta[::2])

        coord = np.concatenate((np.flip(coord_pos, axis=0), coord_neg), axis=0)

        return coord

    return Spiral(r, nD, a, draw_func=_draw_curve, **kwargs)

def LituusSpiral(
    r:float = None,
    nD:int = None,
    a:float = None,
    **kwargs
):
    """
    lituus spiral is a spiral in which the angle θ is 
    inversely proportional to the square of the radius r.

    Args:
        r | radius (float): radius of the spiral
        nD | num_dot (int): number of dots consisting of the curve
        a | angle (float): interior angle (unit: radian)
    """
    def _draw_curve(radius, theta):
        log_theta = np.power(theta, -1/2)
        rad = radius * log_theta[0]/log_theta

        coord = polar_pixels(rad, theta)

        return coord

    return Spiral(r, nD, a, draw_func=_draw_curve, **kwargs)

def LogarithmicSpiral(
    r:float = None,
    nD:int = None,
    a:float = None,
    **kwargs
):
    """
    A logarithmic spiral, equiangular spiral, or growth spiral

    Args:
        r | radius (float): radius of the spiral
        nD | num_dot (int): number of dots consisting of the curve
        a | angle (float): interior angle (unit: degrees, °)
    """
    def _draw_curve(radius, theta):
        exp_theta = np.exp(theta)
        rad = radius * exp_theta/exp_theta[-1]

        coord = polar_pixels(rad, theta)

        return coord

    return Spiral(r, nD, a, draw_func=_draw_curve, **kwargs)

class Cycloid(Geometry2D):
    def __init__(
        self,
        r:float = None,
        nD:int = None,
        a:float = None,
        **kwargs
    ):
        """
        Curve traced by a point on a circle as it rolls along a straight line without slipping
        
        Args:
            r | radius (float): radius of the spiral
            nD | num_dot (int): number of dots consisting of the curve
            a | angle (float): interior angle (unit: degrees, °)
        """
        
        gem_type = self.__class__.__name__

        self.rD, self.nD, self.aG = assignArg(
            gem_type, 
            [r, nD, a], 
            ['radius', 'num_dot', 'angle'], 
            kwargs
        )

        super().__init__(gem_type=gem_type, polar=True, **kwargs)

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, self.aG, self.nD)
        dx = self.rD*(theta - np.sin(theta))
        dy = self.rD*(1 - np.cos(theta))

        coord = np.stack((dx, dy), axis=1)/np.max(theta)
        coord[:, 0] -= self.rD/2

        return coord

    def __len__(self) -> int:
        return self.nD
    
class Epicycloid(Geometry2D):
    def __init__(
        self,
        p:int, 
        q:int,
        r:float = None,
        nD:int = None,
        **kwargs
    ):
        """
        A plane curve produced by tracing the path of a chosen point 
        on the circumference of a circle called an epicycle 
        which rolls without slipping around a fixed circle.
        
        Args:
            p, q (int) : determines the shape of the epicycloid.
                number of cusps can be represented as: k = p/q 
            r | radius (float): radius of the cycloid
            nD | num_dot (int): number of dots consisting of the curve
        """
        gem_type = self.__class__.__name__

        self.p = p
        self.q = q

        self.rD, self.nD = assignArg(
            gem_type, 
            [r, nD], 
            ['radius', 'num_dot'], 
            kwargs
        )

        super().__init__(gem_type=gem_type, polar=True, **kwargs)

    def _base_coords(self) -> np.ndarray:
        k = self.p/self.q
        theta = np.linspace(0, self.q*2*np.pi, self.nD+1)[:-1]

        dx = self.rD*((k+1)*np.cos(theta) - np.cos((k+1)*theta))
        dy = self.rD*((k+1)*np.sin(theta) - np.sin((k+1)*theta))
        coord = np.stack((dx, dy), axis=1)

        return coord

    def __len__(self) -> int:
        return self.nD
    
class Hypocycloid(Geometry2D):
    def __init__(
        self,
        p:int, 
        q:int,
        r:float = None,
        nD:int = None,
        **kwargs
    ):
        """
        A special plane curve generated by the trace of a fixed point 
        on a small circle that rolls within a larger circle.
        
        Args:
            p, q (int) : determines the shape of the hypocycloid.
                number of cusps can be represented as: k = p/q 
            r | radius (float): radius of the cycloid
            nD | num_dot (int): number of dots consisting of the curve
        """
        gem_type = self.__class__.__name__

        self.p = p
        self.q = q

        self.rD, self.nD = assignArg(
            gem_type, 
            [r, nD], 
            ['radius', 'num_dot'], 
            kwargs
        )

        super().__init__(gem_type=gem_type, polar=True, **kwargs)

    def _base_coords(self) -> np.ndarray:
        k = self.p/self.q
        theta = np.linspace(0, self.q*2*np.pi, self.nD+1)[:-1]

        dx = self.rD*((k-1)*np.cos(theta) + np.cos((k-1)*theta))
        dy = self.rD*((k-1)*np.sin(theta) - np.sin((k-1)*theta))
        coord = np.stack((dx, dy), axis=1)

        return coord

    def __len__(self) -> int:
        return self.nD

def CurvedPolygon(
    s:float = None,
    nD:int = None,
    nV:int = None,
    **kwargs
):
    """
    A polygon whose angles are all equal, and all sides have the same length.

    Args:
        s | size (float): distance between centroid and sharp corner
        nD | num_dot (int): number of dots consisting of the whole curve
        nV | num_vertex (int): number of corners
    """

    s, nV = assignArg('CurvedPolygon', [s, nV], ['size', 'num_vertex'], kwargs)

    if nV < 3 :
        raise ValueError("[ERROR] CurvedPolygon should have at least 3 corners")

    return Hypocycloid(nV, 1, s, nD, **kwargs)

class Lissajous(Geometry2D):
    def __init__(
        self,
        a:float,
        b:float,
        r:int = None,
        nD:int = None,
        **kwargs
    ):
        """
        A curve describe the superposition of two perpendicular oscillations
        in x and y directions of different angular frequency (a and b)

        Args:
            a, b (int) : frequency
            r | radius (float): radius of the curve
            nD | num_dot (int): number of dots consisting of the curve
        """

        gem_type = self.__class__.__name__

        self.a = a
        self.b = b

        self.rD, self.nD = assignArg(
            gem_type, 
            [r, nD], 
            ['radius', 'num_dot'], 
            kwargs
        )

        super().__init__(gem_type=gem_type, polar=True, **kwargs)
        
    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        
        dx = self.rD*(np.cos(self.a*theta))
        dy = self.rD*(np.sin(self.b*theta))

        coord = np.stack((dx, dy), axis=1)
        
        return coord

    def __len__(self) -> int:
        return self.nD