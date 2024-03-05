from gemmini.misc import *
from gemmini.d2._gem2D import Geometry2D
from gemmini.calc.coords import to_cartesian


class Curve2D(Geometry2D):
    def __init__(
        self,
        r:float = None,
        points:Union[list, np.ndarray] = None,
        **kwargs
    ) -> None:
        """
        Parent class fot the figures that can be represented as polar coordinates.

        Args:
            r (float): radius of the geometry.
            points (list | np.ndarray): set of points on the curve.
        """
        if not hasattr(self, 'gem_type'):
            self.gem_type = 'Curve2D'
        
        self.rD = r
        self.v = points

        if self.rD <= 0:
            raise ValueError(" \
                [ERROR] %s: Got a non-positive value for the `radius`. \
                "%(self.gem_type)
            )
        
        super().__init__( 
            **kwargs
        )

    def rad(self) -> float:
        return self.rD
    
    def _base_coords(self) -> np.ndarray:
        return self.v
    
    def _linear_paths(self) -> Tuple[list, list]:
        if isinstance(self, (Arc, Spiral, Cycloid)):
            return [linear_seq(len(self))], []

        return [linear_ring(len(self))], []
    
    def __len__(self) -> int:
        return len(self.v)
    
    def __hash__(self) -> int:
        return super().__hash__()


class Circle(Curve2D):
    @geminit({'radius':'r', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        A round plane figure whose boundary consists of points equidistant from a fixed point.

        Args:
            r | radius (float): radius of the circle.
            n | num_dot (int): number of dots consisting of the border of the circle.
        """
        self.rD, self.nD = r, n

        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*np.ones_like(theta)

        coord = to_cartesian(rad, theta)

        super().__init__(
            r=self.rD,
            points=coord,
            planar=True,
            **kwargs
        )
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nD))
    
    
class Arc(Curve2D):
    @geminit({'radius':'r', 'angle':'a', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        a:float = pi/2,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        A portion of a circumference (perimeter of a circle).

        Args:
            r | radius (float): radius of the arc.
            a | angle (float): central angle (unit: radian) of the arc.
            n | num_dot (int): number of dots consisting of the arc.
        """
        self.rD, self.aG, self.nD = r, a, n

        if self.aG <= 0 or self.aG > 2*pi:
            raise ValueError(" \
                [ERROR] Arc: The argument `angle` must be in range (0, 2π]. \
            ")

        theta = np.linspace(0, self.aG, self.nD)
        rad = self.rD*np.ones_like(theta)

        coord = to_cartesian(rad, theta)

        super().__init__(
            r=self.rD,
            points=coord,
            planar=False,
            **kwargs
        )

    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nD, self.aG))

    
class Ellipse(Curve2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        A plane curve surrounding two focal points such that for all points on the curve, 
        the sum of the two distances to the focal points is a constant.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): length of minor axis.
            w | width (float): length of major axis.
            n | num_dot (int): number of dots consisting of the border of the ellipse.
        """
        self.rH, self.rW, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.rH, self.rW = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Ellipse: Argument `size` must be either a single number or a pair of numbers. \
                ")
                
            self.rH, self.rW = s[0], s[1]

        if self.rH <= 0 or self.rW <= 0 :
            raise(" \
                [ERROR] Ellipse: The length of axes should be longer than 0. \
            ")

        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        coord = np.stack((self.rW*np.cos(theta), self.rH*np.sin(theta)), axis=1)/2

        super().__init__(
            r=max(self.rH, self.rW)/2,
            points = coord,
            planar=True,
            **kwargs
        )

    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rH, self.rW, self.nD))


class Spiral(Curve2D):
    @geminit({'radius':'r', 'angle':'a', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        a:float = 2*pi,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        A curve on a plane that winds around a fixed center point at a continuously 
        increasing or decreasing distance from the point.

        Args:
            r | radius (float): radius of the spiral.
            a | angle (float): determines the range of theta in polar equation (r, θ) of
                the spiral (0 ≤ θ ≤ `a`, unit: radian).
            n | num_dot (int): number of dots consisting of the spiral.
        """
        self.rD, self.aG, self.nD = r, a, n

        if self.aG <= 0:
            raise ValueError(" \
                [ERROR] Spiral: Tried to assign non-positive value to the argument `angle`. \
            ")

        self.draw_func = None

        if 'draw_func' in kwargs:
            self.draw_func = kwargs['draw_func']

        theta = np.linspace(0, self.aG, self.nD+1)[1:]

        if self.draw_func == None:
            rad = self.rD*theta/self.aG
            coord = to_cartesian(rad, theta)
        else :
            coord = self.draw_func(self.rD, theta)

        super().__init__(
            r=self.rD,
            points=coord,
            planar=False,
            **kwargs
        )
        
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nD, self.aG))

    
def HyperbolicSpiral(
    r:float = None,
    a:float = 2*pi,
    n:int = 32,
    **kwargs
) -> Spiral:
    """
    A type of spiral with a pitch angle that increases with distance from its center.

    Args:
        r | radius (float): radius of the spiral.
        a | angle (float): determines the range of theta in polar equation (r, θ) of
            the spiral (0 ≤ θ ≤ `a`, unit: radian).
        n | num_dot (int): number of dots consisting of the spiral.
    """
    def _draw_curve(radius, theta):
        aG = np.max(theta)
        n = len(theta)
        _x = np.array(list(range(1, n+1)))[::-1]
        _theta = aG/_x
        
        rad = radius * _theta[0]/_theta
        coord = to_cartesian(rad, _theta)

        return coord

    return Spiral(r, a, n, draw_func=_draw_curve, **kwargs)


def ParabolicSpiral(
    r:float = None,
    a:float = 2*pi,
    n:int = 32,
    **kwargs
) -> Spiral:
    """
    A plane curve with the property that the area between any two consecutive full turns
    around the spiral is invariant.

    Args:
        r | radius (float): radius of the spiral.
        a | angle (float): determines the range of theta in polar equation (r, θ) of
            the spiral (0 ≤ θ ≤ `a`, unit: radian).
        n | num_dot (int): number of dots consisting of the spiral.
    """
    def _draw_curve(radius, theta):
        log_theta = np.sqrt(theta)
        rad = radius * log_theta/log_theta[-1]

        if len(log_theta)%2 == 0 :
            coord_pos = to_cartesian(rad[::2], theta[::2])
            coord_neg = to_cartesian(-rad[::2], theta[::2])
        else :
            coord_pos = to_cartesian(rad[1::2], theta[1::2])
            coord_neg = to_cartesian(-rad[::2], theta[::2])

        coord = np.concatenate((np.flip(coord_pos, axis=0), coord_neg), axis=0)

        return coord

    return Spiral(r, a, n, draw_func=_draw_curve, **kwargs)


def LituusSpiral(
    r:float = None,
    a:float = 2*pi,
    n:int = 32,
    **kwargs
) -> Spiral:
    """
    lituus spiral is a spiral in which the angle θ is inversely proportional to 
    the square of the radius r.

    Args:
        r | radius (float): radius of the spiral.
        a | angle (float): determines the range of theta in polar equation (r, θ) of
            the spiral (0 ≤ θ ≤ `a`, unit: radian).
        n | num_dot (int): number of dots consisting of the spiral.
    """
    def _draw_curve(radius, theta):
        log_theta = np.power(theta, -1/2)
        rad = radius * log_theta[-1]/log_theta

        coord = to_cartesian(rad, theta)

        return coord

    return Spiral(r, a, n, draw_func=_draw_curve, **kwargs)


def LogarithmicSpiral(
    r:float = None,
    a:float = 2*pi,
    n:int = 32,
    **kwargs
) -> Spiral:
    """
    A logarithmic spiral, equiangular spiral, or growth spiral.

    Args:
        r | radius (float): radius of the spiral.
        a | angle (float): determines the range of theta in polar equation (r, θ) of
            the spiral (0 ≤ θ ≤ `a`, unit: radian).
        n | num_dot (int): number of dots consisting of the spiral.
    """
    def _draw_curve(radius, theta):
        aG = np.max(theta)
        n = len(theta)
        _x = [log(i/n) for i in range(1, n+1)]
        _x = np.array(_x)
        _theta = _x + aG
        
        exp_theta = np.exp(_theta)
        rad = radius * exp_theta/exp_theta[-1]

        coord = to_cartesian(rad, _theta)

        return coord

    return Spiral(r, a, n, draw_func=_draw_curve, **kwargs)


def BoundedSpiral(
    r:float = None,
    a:float = 2*pi,
    n:int = 32,
    **kwargs
) -> Spiral:
    """
    A spiral bounded in a circle with radius `r`.

    Args:
        r | radius (float): radius of the spiral.
        a | angle (float): determines the range of theta in polar equation (r, θ) of
            the spiral (0 ≤ θ ≤ `a`, unit: radian).
        n | num_dot (int): number of dots consisting of the spiral.
    """
    def _draw_curve(radius, theta):
        arc_theta = np.arctan(theta/(2*pi))
        rad = radius * arc_theta/np.max(arc_theta)

        coord = to_cartesian(rad, theta)

        return coord

    return Spiral(r, a, n, draw_func=_draw_curve, **kwargs)


class Cycloid(Curve2D):
    @geminit({'radius':'r', 'angle':'a', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        a:float = 2*pi,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        Curve traced by a point on a circle as it rolls along a straight line without slipping.
        
        Args:
            r | radius (float): radius of the circle rolling over the x-axis.
            a | angle (float): angle through which the rolling circle has rotated (unit: radian).
            n | num_dot (int): number of dots on the trail.
        """
        self.rD, self.aG, self.nD = r, a, n

        theta = np.linspace(0, self.aG, self.nD)
        dx = self.rD*(theta - np.sin(theta))
        dy = self.rD*(1 - np.cos(theta))

        coord = np.stack((dx, dy), axis=1)/np.max(theta)
        coord[:, 0] -= self.rD/2

        super().__init__(
            r=self.rD,
            points=coord,
            planar=True,
            **kwargs
        )
        
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nD, self.aG))

    
class Epicycloid(Curve2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        p:int, 
        q:int,
        s:float = None,
        n:int = 256,
        **kwargs
    ) -> None:
        """
        A plane curve produced by tracing the path of a chosen point on the circumference of 
        a circle called an epicycle which rolls without slipping around a fixed circle.
        
        Args:
            p, q (int) : determines the shape of the epicycloid.
                number of cusps can be represented as: k = p/q 
            s | size (float): height/width of the geometry.
            n | num_dot (int): number of dots on the trail.
        """
        self.p, self.q, self.uS, self.nD = p, q, s, n

        if p <= 0 or q <= 0 or type(p) != int or type(q) != int:
            raise ValueError(" \
                [ERROR] Epicycloid: Both `p` and `q` must be positive integers. \
            ")

        k = self.p/self.q
        theta = np.linspace(0, self.q*2*np.pi, self.nD+1)[:-1]

        dx = (k+1)*np.cos(theta) - np.cos((k+1)*theta)
        dy = (k+1)*np.sin(theta) - np.sin((k+1)*theta)
        coord = np.stack((dx, dy), axis=1)
        coord = self.uS/2 * coord / np.max(coord)

        super().__init__(
            r=self.uS/2,
            points=coord,
            planar=(self.q == 1),
            **kwargs
        )

    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.p, self.q, self.uS, self.nD))
    

class Hypocycloid(Curve2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        p:int, 
        q:int,
        s:float = None,
        n:int = 256,
        **kwargs
    ) -> None:
        """
        A special plane curve generated by the trace of a fixed point on a small circle
        that rolls within a larger circle.
        
        Args:
            p, q (int) : determines the shape of the hypocycloid.
                number of cusps can be represented as: k = p/q 
            s | size (float): height/width of the geometry.
            nD | num_dot (int): number of dots on the trail.
        """
        self.p, self.q, self.uS, self.nD = p, q, s, n

        if p <= 0 or q <= 0 or type(p) != int or type(q) != int:
            raise ValueError(" \
                [ERROR] Hypocycloid: Both `p` and `q` must be positive integers. \
            ")
        
        k = self.p/self.q
        theta = np.linspace(0, self.q*2*np.pi, self.nD+1)[:-1]

        dx = (k-1)*np.cos(theta) + np.cos((k-1)*theta)
        dy = (k-1)*np.sin(theta) - np.sin((k-1)*theta)
        coord = np.stack((dx, dy), axis=1)
        coord = self.uS/2 * coord / np.max(coord)

        super().__init__(
            r=self.uS/2,
            points=coord,
            planar=True,
            **kwargs
        )
        
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.p, self.q, self.uS, self.nD))


@alias({'size':'s', 'num_vertex':'v', 'num_dot':'n'})
def CurvedPolygon(
    s:float = None,
    v:int = None,
    n:int = 128,
    **kwargs
) -> Hypocycloid:
    """
    A curve alike regular polygon, but has rounded edges curved toward its center.

    Args:
        s | size (float): height/width of the geometry.
        v | num_vertex (int): number of corners.
        n | num_dot (int): number of dots consisting of the whole curve.
    """
    if v < 3 :
        raise ValueError(" \
            [ERROR] CurvedPolygon: To draw the geometry, at least 3 corners are required. \
        ")
    
    if s <= 0 :
        raise ValueError(" \
            [ERROR] CurvedPolygon: The size of the geometry must be greater than 0. \
        ")

    return Hypocycloid(v, 1, s, n, **kwargs)


class Lissajous(Curve2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        a:float,
        b:float,
        s:int = None,
        n:int = 128,
        **kwargs
    ) -> None:
        """
        A curve describe the superposition of two perpendicular oscillations
        in x and y directions of different angular frequency (a and b).

        Args:
            a, b (int) : frequencies of the vertical and horizontal sinusoidal inputs.
            s | size (float): the height/width of the geometry.
            n | num_dot (int): number of dots consisting of the curve.
        """
        self.a, self.b, self.uS, self.nD = a, b, s, n

        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        
        dx = self.uS*(np.cos(self.a*theta))/2
        dy = self.uS*(np.sin(self.b*theta))/2

        coord = np.stack((dx, dy), axis=1)

        super().__init__(
            r=self.uS/2,
            points=coord,
            planar=True,
            **kwargs
        )
        
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.a, self.b, self.uS, self.nD))
    
    
class Folium(Curve2D):
    @geminit({'radius':'r', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        The pedal of the deltoid with respect to one of its cuspidal points.

        Args:
            r | radius (float): radius of the geometry.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.rD, self.nD = r, n

        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*np.power(np.cos(theta), 3)

        coord = to_cartesian(rad, theta)
        coord[:, 0] -= self.rD/2

        super().__init__(
            r=self.rD,
            points=coord,
            planar=True,
            **kwargs
        )
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nD))
    
    
class Bifolium(Curve2D):
    @geminit({'radius':'r', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        A quartic plane curve with equation in Cartesian coordinates: (x² + y²)² = ax²y.

        Args:
            r | radius (float): radius of the geometry.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.rD, self.nD = r, n

        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*np.sin(theta)*np.power(np.cos(theta), 2)

        coord = to_cartesian(rad, theta)

        super().__init__(
            r=self.rD,
            points=coord,
            planar=True,
            **kwargs
        )
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nD))