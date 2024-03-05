from gemmini.misc import *
from gemmini.d2._gem2D import Geometry2D
from gemmini.calc.geometry import connect_edges
from gemmini.calc.coords import rotate_2D, to_cartesian
from gemmini.d2.line2D import Segment
from gemmini.d2.polygon2D import RegularPolygon, ConcaveKite
from gemmini.d2.polar2D import Circle, Arc, Epicycloid


class CircularSector(Geometry2D):
    @geminit({'radius':'r', 'angle':'a', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        a:float = pi,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        The portion of a disk (a closed region bounded by a circle) enclosed by two radii and an arc.

        Args:
            r | radius (float): radius of the sector.
            a | angle (float): central angle (unit: radian) of the sector.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.rD, self.aG, self.nD = r, a, n

        if self.aG <= 0 or self.aG > 2*pi:
            raise ValueError(" \
                [ERROR] CircularSector: The argument `angle` must be in range (0, 2π]. \
            ")

        if self.nD < 6 :
            raise ValueError(" \
                [Error] CircularSector: The argument `num_dot` is too small. \
            ")

        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = self.rD*(2 + self.aG)
        _nD = self.nD + 3
        nrD = int(_nD*self.rD/_s)
        naD = _nD - 2*nrD

        theta = np.linspace(0, min(2*pi, self.aG), naD)
        rad = self.rD*np.ones_like(theta)

        coord_arc = to_cartesian(rad, theta)
        
        r1 = Segment(p1=(0,0), p2=(coord_arc[0][0], coord_arc[0][1]), n=nrD)
        r2 = Segment(p1=(coord_arc[-1][0], coord_arc[-1][1]), p2=(0, 0), n=nrD)
        
        coord_r1 = r1.coords()
        coord_r2 = r2.coords()
        
        coord = np.concatenate((coord_arc[:-1], coord_r2[:-1], coord_r1[:-1]), axis=0)
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []
    
    def __len__(self) -> int:
        return self.nD
        
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.aG, self.nD))


class CircularSegment(Geometry2D):
    @geminit({'radius':'r', 'angle':'a', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        a:float = pi,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        A region of two-dimensional space that is bounded by a circular arc 
        and by the circular chord connecting the endpoints of the arc.

        Args:
            r | radius (float): radius of the segment.
            a | angle (float): central angle (unit: radian) of the segment.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.rD, self.aG, self.nD = r, a, n

        if self.aG <= 0 or self.aG > 2*pi:
            raise ValueError(" \
                [ERROR] CircularSegment: The argument `angle` must be in range (0, 2π]. \
            ")

        if self.nD < 6 :
            raise ValueError(" \
                [Error] CircularSegment: The argument `num_dot` is too small. \
            ")

        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = self.rD*(2*sin(self.aG/2) + self.aG)
        _nD = self.nD + 2
        naD = int(_nD*self.rD*self.aG/_s)
        ncD = _nD - naD

        theta = np.linspace(0, min(2*pi, self.aG), naD)
        rad = self.rD*np.ones_like(theta)

        coord_arc = to_cartesian(rad, theta)

        c = Segment(p1=(coord_arc[-1][0], coord_arc[-1][1]), p2=(coord_arc[0][0], coord_arc[0][1]), n=ncD)
        
        coord_chord = c.coords()
        
        coord = np.concatenate((coord_arc, coord_chord[1:-1]), axis=0)
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
        
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.aG, self.nD))


class Wave(Geometry2D):
    @geminit({'radius':'r', 'angle':'a', 'num_dot':'n'})
    def __init__(
        self, 
        a:float = None,
        w:float = None,
        f:float = 1.0,
        p:float = 0.0,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        A periodic wave whose waveform is the trigonometric sine function.
        (also, denoted as a sine wave, sinusoidal wave, or sinusoid)
        
        Args:
            a | amplitude (float): the peak deviation of the function from zero.
            w | width (float): the horizontal length of the wave.
            f | frequency (float): the number of oscillations (cycles) that occur each second of time.
            p | phase (float): When `p` is non-zero, the entire waveform appears to be shifted 
                backwards in time by the amount `p/(2*pi*f)` seconds.
            n | num_dot (int): number of points consisting of the wave.
        """
        self.aP, self.w, self.fQ, self.pH, self.nD = a, w, f, p, n
        
        super().__init__(
            planar=False,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*pi, self.nD)
        x = np.linspace(-self.w/2, self.w/2, self.nD)
        rad = self.aP * np.sin(self.fQ*theta + self.pH)
        
        coord = np.stack((x, rad), axis=1)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_seq(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.aP, self.w, self.fQ, self.pH, self.nD))


class Helix(Geometry2D):
    @geminit({'radius':'r', 'angle':'a', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        a:float = 4*pi,
        n:int = 64,
        pitch:float = 1.0,
        **kwargs
    ) -> None:
        """
        Shape of a coiled tube, generated by sweeping a circle.

        Args:
            r | radius (float): radius of the spring.
                When a positive number is given, the point traces a right-handed helix.
                Otherwise, the geometry looks like a left-handed helix.
            a | angle (float): determines the range of theta in polar equation (r, θ) of
                the spiral (0 ≤ θ ≤ `a`, unit: radian).
            n | num_dot (int): number of dots consisting of the geometry.
            pitch (float): determines the width of the single rotation.
        """
        self.rD, self.aG, self.nD, self.pitch = r, a, n, pitch
        
        if self.aG <= 0:
            raise ValueError(" \
                [ERROR] Helix: Tried to assign non-positive value to the argument `angle`. \
            ")

        super().__init__(
            planar=False,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, self.aG, self.nD)
        height = self.pitch*np.linspace(-self.rD, self.rD, self.nD)
        rad = self.rD*np.ones_like(theta)
        coord = np.stack((rad*np.cos(theta), -rad*np.sin(theta) + height), axis=1)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_seq(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.aG, self.nD, self.pitch))
    

class Parabola(Geometry2D):
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
        A plane curve which is mirror-symmetrical and is approximately U-shaped.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the U-shaped curve.
            w | width (float): width of the U-shaped curve.
            n | num_dot (int): number of points consisting of the parabola.
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Parabola: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        super().__init__(
            planar=False,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        dx = np.linspace(-self.w/2, self.w/2, self.nD)
        dy = 4*self.h*np.power(dx, 2)/pow(self.w, 2) - self.h/2
        coord = np.stack((dx, dy), axis=1)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD))


class SymmetricSpiral(Geometry2D):
    @geminit({'radius':'r', 'num_vertex':'v', 'num_dot':'n'})
    def __init__(
        self, 
        r:float = None,
        v:int = 6,
        n:int = 16,
        **kwargs
    ) -> None:
        """
        Blades of N-way logarithmic spiral.

        Args:
            r | radius (float): radius of the spiral.
            v | num_vertex (int): number of blades.
            n | num_dot (int): number of dots consisting of each blade.
        """
        self.rD, self.nV, self.nD = r, v, n

        if self.nV < 3 :
            raise ValueError(" \
                [ERROR] SymmetricSpiral: Requires at least 3 blades \
            ")

        if self.nD < 2 :
            raise ValueError(" \
                [ERROR] SymmetricSpiral: Each blade must have at least 2 dots \
            ")
        
        super().__init__(
            planar=False,
            **kwargs
        )

    def _draw_blades(self, r, v):
        size = self.rD*r/self.nD
        e = exp(1)
        pitch = 90*(self.nV - 2)/self.nV * 2*pi/360
        
        a = 1
        b = 1/tan(pitch)
        s = self.rD - size
        t = log(b*s/(a*sqrt(1+b**2)))/b
        
        gr = a*pow(e, (b*t))
        
        x = gr*cos(t)
        y = gr*sin(t)

        aG = 2*pi*v/self.nV
        rx = cos(aG)*x - sin(aG)*y
        ry = sin(aG)*x + cos(aG)*y

        return rx, ry

    def _base_coords(self) -> np.ndarray:
        coord = np.array([[self._draw_blades(j, i) for j in range(self.nD)] for i in range(self.nV)])
        coord = coord.reshape(-1, coord.shape[-1])

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        eidx = [[i*self.nD + j for j in range(self.nD)] for i in range(self.nV)]

        return eidx, []
    
    def __len__(self) -> int:
        return self.nD*self.nV
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nV, self.nD))
    

class Star(Geometry2D):
    @geminit({'size':'s', 'num_vertex':'v', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        v:int = 5,
        n:int = 8,
        **kwargs
    ) -> None:
        """
        A regular star polygon that has `v` corner vertices and intersecting edge.
        
        Args:
            s | size (float): distance between centroid and sharp corner of the star.
            n | num_dot (int): number of dots consisting of a edge.
            v | num_vertex (int): number of vertex.
        """
        self.uS, self.nV, self.nD = s, v, n

        if self.nV < 3 :
            raise ValueError(" \
                [ERROR] Star: Requires at least 3 vertices. \
            ")

        if self.nD < 2 :
            raise ValueError(" \
                [ERROR] Star: Each side must have at least 2 dots. \
            ")

        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        ang = 2*pi/self.nV
        _s = sin(ang/2)
        _t = tan(ang)
        _c = cos(ang/2)
        irD = self.uS/(_s*_t + _c)
        
        coord = []
        
        for i in range(self.nV):
            left = Segment((irD*_s, irD*_c), (0, self.uS), self.nD)
            right = Segment((0, self.uS), (-irD*_s, irD*_c), self.nD)
            
            _coord = np.concatenate((left[1:], right[1:-1]), axis = 0)
            _coord = rotate_2D(_coord, i*ang)
            
            coord.append(_coord)
            
        _p = RegularPolygon(s = 2*irD*_s, v=self.nV, n = self.nD)
        _p.rotate(pi)
        
        coord.append(_p[:])
        coord = np.concatenate(tuple(coord), axis=0)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        eidx = []
        
        for i in range(self.nV):
            for j in range(2*self.nD-3):
                eidx.append(i*(2*self.nD-3) + j)
                
            eidx.append(self.nV*(2*self.nD-3) + (i+1)*(self.nD-1) - 1)
            
        eidx.append(0)

        iidx = linear_ring(self.nV*(2*self.nD-3), self.nV*(3*self.nD-4))

        return [eidx], [iidx]

    def __len__(self) -> int:
        return self.nV*(3*self.nD-4)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD, self.nV))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
#          The below geometries are not defined as mathematical term,         #
#                                                                             #      
#     But, they are all popular and symbolistic shape used in many cases.     #  
#                                                                             #        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class Heart(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:int = None,
        n:int = 128,
        **kwargs
    ) -> None:
        """
        Heart symbol.
        
        Args:
            s | size (float): scale of the geometry.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.uS, self.nD, = s, n

        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = (self.uS/2)*(2 - 2.3*np.sin(theta) + 0.4*np.cos(2*theta)
            + (1.3*np.sin(theta) * np.sqrt(np.power(np.abs(np.cos(theta)), 1.3)))/(np.sin(theta) + 1.7))/3

        coord = to_cartesian(rad, theta)
        coord[:, 1] += (self.uS/2)*(3.2 + 1.3/2.7 - 1.3/0.7)/3
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))


class ButterFly(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        n:int = 128,
        **kwargs
    ) -> None:
        """
        ButterFly shape.
        
        Args:
            s | size (float): scale of the geometry.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.uS, self.nD, = s, n

        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.uS*(1.35 - np.cos(theta - np.pi/3) * np.sin(3*(theta - np.pi/3)))/2

        leftside = np.where(
            (theta >= np.pi/2) &
            (theta <= 3*np.pi/2)
        )

        rad[leftside] = self.uS * (
            1.35 - np.cos(2*np.pi/3 - theta[leftside]) * np.sin(3*(2*np.pi/3 - theta[leftside]))
        )/2

        coord = to_cartesian(rad, theta)/1.35
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))
    

class CottonCandy(Geometry2D):
    @geminit({'size':'s', 'num_corner':'c', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        c:int = None, 
        n:int = 128,
        **kwargs
    ) -> None:
        """
        Puffy, cotton-like cloud shape.
        
        Args:
            s | size (float): scale of the geometry.
            c | num_corner (int): number of corners.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.uS, self.nC, self.nD = s, c, n

        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        fig = Epicycloid(p=self.nC, q=1, size=self.uS, num_dot=self.nD)

        return np.array(fig[:])
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nC, self.nD))


class Boomerang(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self, 
        s:float = None,
        n:int = 64, 
        **kwargs
    ) -> None:
        """
        Boomerang shape.

        Args:
            s | size (float): scale of the geometry.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.uS, self.nD = s, n

        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rx = (np.cos(theta) + np.cos(2*theta))/4
        ry = np.sin(theta)
        
        coord = np.stack((rx, ry), axis=1)*self.uS/2
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))
    
    
class Stellate(Geometry2D):
    @geminit({'size':'s', 'num_corner':'c', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        c:int = 6,
        n:int = 128,
        **kwargs
    ) -> None:
        """
        A star-like shaped curve.
        
        Args:
            s | size (float): scale of the geometry.
            c | num_corner (int): number of corners.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.uS, self.nC, self.nD = s, c, n
        
        if self.nC < 3:
            raise ValueError(" \
                [ERROR] Stellate: Requires at least 3 corners. \
            ")

        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rx = (9 + np.cos(self.nC*theta))*np.sin(theta)/10
        ry = (9 + np.cos(self.nC*theta))*np.cos(theta)/10
        
        coord = np.stack((rx, ry), axis=1)*self.uS/2
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nC, self.nD))
    
    
class Shuriken(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self, 
        s:float = None,
        border:float = 0.5,
        n:int = 10,
        **kwargs
    ) -> None:
        """
        A shuriken shape with 4 blades.

        Args:
            s | size (float): distance between centroid and the far corner.
            border (float): determines the distance from the center to the nearest (inward) corner.
                It ranges from 0 to 1; smaller value makes the geometry have more sharp blades.
            n | num_dot (int): number of points consisting of each side.
        """
        self.R = s/2
        self.r = border*self.R
        self.nD = n

        if border <= 0 or border >= 1:
            raise ValueError(" \
                [ERROR] Shuriken: The assigned value for argument `border` is out of range: (0 < b < 1). \
            ")

        if self.R <= 0:
            raise ValueError(" \
                [ERROR] Shuriken: Tried to assign a non-positive valut to the `size`. \
            ")
        
        if self.nD < 2 :
            raise ValueError(" \
                [ERROR] Shuriken: Each blade must have at least 2 dots. \
            ")
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _draw_edge(self) -> np.ndarray:
        i = np.arange(self.nD)
        lb = self.r *sqrt(2)/2
        
        x_a = self.R - (self.R - lb)*i/(self.nD - 1)
        y_a = lb * i/(self.nD - 1)
        coord_a = np.vstack((x_a, y_a)).T
        
        j = np.arange(1, self.nD-1)[::-1]
        x_b = lb * j/(self.nD - 1)
        y_b = self.R - (self.R - lb) * j/(self.nD - 1)
        coord_b = np.vstack((x_b, y_b)).T
        
        coord = np.concatenate((coord_a, coord_b), axis=0)
        
        return coord

    def _base_coords(self) -> np.ndarray:
        edge_right = self._draw_edge()
        
        edge_up = rotate_2D(edge_right, pi/2)
        edge_left = rotate_2D(edge_right, pi)
        edge_down = rotate_2D(edge_right, 3*pi/2)
        
        coord = np.concatenate((edge_right, edge_up, edge_left, edge_down), axis=0)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return 8*(self.nD - 1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.r, self.R, self.nD))
    

class _Flower(Geometry2D):
    def __init__(
        self,
        draw_func:Callable,
        gem_type:str,
        s:float = None,
        n:int = None,
        nL:int = None,
        planar:bool = True,
        **kwargs
    ) -> None:
        """
        A flower-shaped curve.
        """
        self.draw_func = draw_func
        self.gem_type = gem_type
        
        self.uS, self.nD, self.nL = s, n, nL
        
        if self.nL < 3:
            raise ValueError(" \
                [ERROR] %s: Requires at least 3 leaves. \
            "%(gem_type))

        super().__init__(
            planar=planar,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        return self.draw_func(self.uS/2, self.nD, self.nL)

    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD*self.nL if self.gem_type == 'Flower_D' else self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nL, self.nD))
    

def Flower_A(s:float = None, n:int = 128, nL:int = 6, **kwargs) -> _Flower:
    """
    Flower shape Type A (like Daisy).
    
    Args:
        s | size (float): scale of the geometry.
        n | num_dot (int): number of dots consisting of its circumference.
        nL | num_leaves (int): number of floral leaves.
    """
    def func(uS, nD, nL):
        nD_l = int(nD/nL)
        coord = []

        for i in range(nL):
            _nD = nD_l + 2 if i != nL -1 else nD + 2 - (nL-1)*nD_l

            theta = np.linspace(0, np.pi/nL, _nD)[1:-1]
            rad = uS*np.sin(nL*theta)
        
            _c = to_cartesian(rad, theta)
            _c = rotate_2D(_c, 2*i*pi/nL)

            coord.append(_c)

        return np.concatenate(coord, axis=0)
    
    return _Flower(func, 'Flower_A', s, n, nL, **kwargs)


@alias({'size':'s', 'num_dot':'n', 'num_leaves':'nL'})
def Flower_B(s:float = None, n:int = 128, nL:int = 6, **kwargs) -> _Flower:
    """
    Flower shape Type B (like Lily).
    
    Args:
        s | size (float): scale of the geometry.
        n | num_dot (int): number of dots consisting of its circumference.
        nL | num_leaves (int): number of floral leaves.
    """
    def func(uS, nD, nL):
        theta = np.linspace(0, 2*np.pi, nD+1)[:-1]
        rad = uS*(2 - np.power(np.sin(nL*theta), 3))/3
        coord = to_cartesian(rad, theta)
        
        return coord
    
    return _Flower(func, 'Flower_B', s, n, nL, **kwargs)

    
@alias({'size':'s', 'num_dot':'n', 'num_leaves':'nL'})
def Flower_C(s:float = None, n:int = 128, nL:int = 5, **kwargs) -> _Flower:
    """
    Flower shape Type C (like Camellia).
    
    Args:
        s | size (float): scale of the geometry.
        n | num_dot (int): number of dots consisting of its circumference.
        nL | num_leaves (int): (odd) number of floral leaves.
    """
    if nL%2 == 0:
        raise ValueError(" \
            [ERROR] Flower_C: The number of leaves should be odd. \
        ")
    
    def func(uS, nD, nL):
        theta = np.linspace(0, 4*np.pi, nD+1)[:-1]
        rad = uS * (2 + np.cos(nL*theta/2))/3
            
        coord = to_cartesian(rad, theta)

        return coord
    
    return _Flower(func, 'Flower_C', s, n, nL, **kwargs)


@alias({'size':'s', 'num_dot':'n', 'num_leaves':'nL'})
def Flower_D(s:float = None, n:int = 25, nL:int = 6, **kwargs) -> _Flower:
    """
    Flower shape Type D (like Saffron).
    
    Args:
        s | size (float): scale of the geometry.
        n | num_dot (int): number of dots consisting of one leaf.
        nL | num_leaves (int): number of floral leaves.
    """
    def func(uS, nD, nL):
        if nD%2 == 0 :
            theta = np.linspace(0, 4*np.pi, 12*(nD+1)+1)[:-1]
        else :
            theta = np.linspace(0, 4*np.pi, 24*(nD//2 + 1)+1)[:-1]
            
        rad = uS * np.cos(3*theta/2)
        coord = to_cartesian(rad, theta)
        one_leaf = sqrt(2)*np.concatenate((coord[nD+2:3*nD//2+2], coord[9*nD//2+5:5*nD+5]), axis=0)
            
        res = one_leaf.copy()
        
        for i in range(1, nL):
            tp = rotate_2D(one_leaf, 2*pi*i/nL)
            res = np.concatenate((res, tp), axis=0)

        return res
    
    return _Flower(func, 'Flower_D', s, n, nL, **kwargs)


@alias({'size':'s', 'num_dot':'n', 'num_leaves':'nL'})
def Flower_E(s:float = None, n:int = 128, nL:int = 6, **kwargs) -> _Flower:
    """
    Flower shape Type E (like Marigold).
    
    Args:
        s | size (float): scale of the geometry.
        n | num_dot (int): number of dots consisting of its circumference.
        nL | num_leaves (int): number of floral leaves.
    """
    def func(uS, nD, nL):
        theta = np.linspace(0, 2*np.pi, nD+1)[:-1]
        rx = 2*np.cos(2*theta) + np.cos((1 + nL)*theta)
        ry = 2*np.sin(2*theta) + np.sin((1 + nL)*theta)
        
        coord = np.stack((rx, ry), axis=1)*uS/3
        
        return coord
    
    return _Flower(func, 'Flower_E', s, n, nL, **kwargs)


@alias({'size':'s', 'num_dot':'n', 'num_leaves':'nL'})
def Flower_F(s:float = None, n:int = 128, nL:int = 6, **kwargs) -> _Flower:
    """
    Flower shape Type F (like Jasmine). 
    
    Args:
        s | size (float): scale of the geometry.
        n | num_dot (int): number of dots consisting of its circumference.
        nL | num_leaves (int): number of floral leaves.
    """
    def func(uS, nD, nL):
        theta = np.linspace(0, 2*np.pi, nD+1)[:-1]
        rad = uS*(1 + np.cos(nL*theta))/2
        
        coord = to_cartesian(rad, theta)
        
        return coord
    
    return _Flower(func, 'Flower_F', s, n, nL, **kwargs)
    
    
class Clover(Geometry2D):
    @geminit({'size':'s', 'num_leaves':'nL', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        nL:int = 4,
        n:int = 128,
        **kwargs
    ) -> None:
        """
        Clover leaf shape.

        Args:
            s | size (float): scale of the geometry.
            nL | num_leaves (int): number of floral leaves.
            n | num_dot (int): number of dots consisting of its circumference.
        """
        self.uS, self.nV, self.nD = s, nL, n
        
        if self.nV < 3 :
            raise ValueError(" \
                [ERROR] Clover: Requires at least 3 leaves. \
            ")
    
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = 1 + np.cos(self.nV*theta) + np.power(np.sin(self.nV*theta), 2)
        rad = (self.uS/2)*rad/3
        
        coord = to_cartesian(rad, theta)
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nV, self.nD))
    

class FattyStar(Geometry2D):
    @geminit({'size':'s', 'num_vertex':'v', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        v:int = 5,
        n:int = 128,
        **kwargs
    ) -> None:
        """
        A concave star drawn by a non-straight edge.

        Args:
            s | size (float): scale of the geometry.
            v | num_vertex (int): number of vertex.
            n | num_dot (int): number of dots consisting of the star.
        """
        self.uS, self.nV, self.nD = s, v, n
        
        if self.nV < 3 :
            raise ValueError(" \
                [ERROR] FattyStar: Requires at least 3 vertices. \
            ")
    
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = (self.uS/2)*(1.5 - np.power(np.sin(self.nV*theta/2)/2 + np.cos(self.nV*theta/2)/2, 2))
        
        coord = to_cartesian(rad, theta)
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nV, self.nD))


class Moon(Geometry2D):
    @geminit({'radius':'r', 'num_dot':'n'})
    def __init__(
        self, 
        r:float = None,
        n:int = 64,
        breadth:float = 0.5,
        **kwargs
    ) -> None:
        """
        A crescent shape used to represent the lunar phase.

        Args:
            r | radius (float): radius of the moon.
            n | num_dot (int): number of dots consisting of its circumference.
            breadth (float): represents ratio of largest width aspect to the diameter of the moon,
                using percentage values in range [0, 1].
        """
        self.rD, self.nD = r, n
        self.bR = breadth
        
        if breadth <= 0 or breadth >= 1:
            raise ValueError(" \
                [ERROR] Moon: The argument `breadth` should be in range of 0 < b < 1. \
            ")

        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*np.ones_like(theta)/2

        coord = to_cartesian(rad, theta)
        fliped_idx = np.where(coord[:, 0] <= -self.bR*self.rD/2)
        coord[fliped_idx, 0] = -self.bR*self.rD - coord[fliped_idx, 0]

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nD, self.bR))
    
    
class Yinyang(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self, 
        s:int = None,
        n:int = 128,
        **kwargs
    ) -> None:
        """
        Yin and Yang symbol
        
        Args:
            s | size (float): scale of the geometry
            n | num_dot (int): number of points
        """
        self.uS, self.nD, = s, n

        super().__init__(
            planar=False,
            **kwargs
        )
    
    def _base_coords(self) -> np.ndarray:
        _s = 5*pi*self.uS/4
        _nD = self.nD + 3
        self.nD_r = nD_r = int(_nD * (pi*self.uS/4)/_s)
        self.nD_R = nD_R = _nD - 2*nD_r
        
        a1 = Arc(r=self.uS/4, a=pi, n=nD_r)
        a2 = Arc(r=self.uS/4, a=pi, n=nD_r)
        a1.rotate(pi)
        a1.translateX(self.uS/4)
        a2.translateX(-self.uS/4)
        
        c = Circle(r=self.uS/2, n=nD_R)
        
        coord = np.concatenate((c[:], a2[:-1], a1[1:-1]), axis=0)
        coord = rotate_2D(coord, pi/2)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        eidx1 = linear_seq(self.nD_R//2)
        eidx1.extend(linear_seq(self.nD_R + self.nD_r - 2, self.nD_R - 1, -1))
        eidx1.extend(linear_seq(self.nD_R + self.nD_r-1, self.nD_R + 2*self.nD_r-3))
        eidx1.append(0)

        eidx2 = linear_seq(self.nD_R//2, self.nD_R)
        eidx2.extend(linear_seq(self.nD_R + 2*self.nD_r - 4, self.nD_R + self.nD_r - 2, -1))
        eidx2.extend(linear_seq(self.nD_R, self.nD_R + self.nD_r-1))
        eidx2.append(self.nD_R//2)

        return [eidx1, eidx2], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))
    

class Polygontile(Geometry2D):
    @geminit({'size':'s', 'num_vertex':'v', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        v:int = None,
        n:int = 10,
        **kwargs
    ) -> None:
        """
        A regular polygon surrounded by other regular polygons that have same number of vertices.

        Args:
            s | size (float): length of each side.
            n | num_dot (int): number of dots consisting of a edge.
            v | num_vertex (int): number of vertex.
        """
        self.uS, self.nV, self.nD = s, v, n

        if self.nV < 3 :
            raise ValueError(" \
                [ERROR] Polygontile: Requires at least 3 vertices. \
            ")

        if self.nD < 2 :
            raise ValueError(" \
                [ERROR] Polygontile: Each side must have at least 2 dots. \
            ")
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        irD = 2 * tan(pi/self.nV) * self.uS / (2 + 1/cos(pi/self.nV))
        _fo = RegularPolygon(size=irD, num_dot=self.nD, num_vertex=self.nV)
        coord = []
        
        for i in range(self.nV):
            mx, my = 0, irD/tan(pi/self.nV)
            dx, dy = rotate_2D((mx, my), 2*i*pi/self.nV)
            _ft = _fo.copy()
            _ft.rotate(2*pi*i/self.nV)
            _ft.translate(dx, dy)
            coord.append(_ft[:-1])

        return np.concatenate(tuple(coord), axis=0)
    
    def _linear_paths(self) -> Tuple[list, list]:
        eidx, iidx = [], []

        for i in range(self.nV):
            eidx.extend(
                linear_seq(
                    (i*self.nV + 1)*(self.nD - 1) - (1 + i),
                    (i+1)*self.nV*(self.nD-1) - (1 + i)
                )
            )

            iidx.extend(
                linear_seq(
                    (i*self.nV + 1)*(self.nD - 1) - i - 1,
                    (i*self.nV + 1)*(self.nD - 1) - (self.nD + i),
                    -1
                )
            )
            
        eidx.append(self.nD - 2)
        iidx.append(self.nD - 2)

        return [eidx], [iidx]
        
    def __len__(self) -> int:
        return self.nV*(self.nV*(self.nD-1)-1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nV, self.nD))

    
class Gear(Geometry2D):
    @geminit({'radius':'r', 'num_cog':'c', 'num_dot':'n'})
    def __init__(
        self,
        r:float = None,
        c:int = 8,
        n:int = 10,
        **kwargs
    ) -> None:
        """
        Gear shape, which depicts a rotating circular machine part.
        
        Args:
            r | radius (float): radius of the gear.
            c | num_cog (int): number of cogs (gear tooth).
            n | num_dot (int): number of dots consisting of a edge.
        """
        self.rD, self.nC, self.nD = r, c, n
        
        if self.nC < 3 :
            raise ValueError(" \
                [ERROR] Gear: Requires at least 3 cogs (gear tooth). \
            ")

        if self.nD < 2 :
            raise ValueError(" \
                [ERROR] Gear: Each side must have at least 2 dots. \
            ")
        
        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        irD = 2*self.rD/(2 + 1/tan(pi/self.nC))
        f = RegularPolygon(s = irD, n=self.nD, v=4)
        f.translateX(irD*(1 + 1/tan(pi/self.nC))/2)

        coord = []

        for i in range(self.nC):
            _f = f.copy()
            _f.rotate(2*i*pi/self.nC)

            coord.append(_f[:3*(self.nD-1)])
        
        coord = np.concatenate(tuple(coord), axis=0)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return 3*(self.nD-1)*self.nC
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.rD, self.nC, self.nD))
    
    
class SnippedRect(Geometry2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:int = 48,
        clip_size:Tuple[float, float, float, float] = (0.5, 0, 0, 0),
        **kwargs
    ) -> None:
        """
        A rectangle with a diagonal cut at the some corner.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the geometry.
            w | width (float): width of the geometry.
            n | num_dot (int): number of dots consisting of the geometry.
            clip_size (float): denote the relative size of the snipped edge
                for each corners (top_left, top_right, bottom_left, bottom_right),
                using percentage values in range [0, 1].
                ex) clip_size = (1, 0, 1, 0.5) results in a geometry looks like
                
                        ''''''''''\\
                        |          \\
                        |          //
                        \\........//
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] SnippedRect: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        self.bR = [clip_size[i] if len(clip_size) > i else 0 for i in range(4)]
        
        for i in range(4):
            if self.bR[i] < 0 or self.bR[i] > 1:
                raise ValueError(" \
                    [ERROR] SnippedRect: Elements of `clip_size` must be in (0 ~ 1). \
                ")
            
        super().__init__(
            planar=True,
            **kwargs
        )
    
    def _base_coords(self) -> np.ndarray:
        iS = [i * min(self.h, self.w)/2 for i in self.bR]
        _s = 2*(self.h + self.w) - (2 - sqrt(2))*sum(iS)
        _nD = self.nD + 4 
        
        for i, j in [(0, 1), (1, 3), (2, 3), (2, 0)]:
            if self.bR[i] == self.bR[j] == 0:
                continue
            
            if self.h == self.w and self.bR[i] == self.bR[j] == 1:
                continue
            
            _nD += 1
        
        num_dot = _nD
        edges = []
        
        if self.bR[0] > 0:
            nD_e = int(_nD * sqrt(2)*iS[0]/_s)
            num_dot -= nD_e
            edges.append(Segment((self.w/2, self.h/2 - iS[0]), (self.w/2 - iS[0], self.h/2), n=nD_e))
        
        if not (self.bR[0] == self.bR[1] == 1 and self.h == self.w):
            nD_e = int(_nD * (self.w - iS[0] - iS[1])/_s)
            num_dot -= nD_e
            edges.append(Segment((self.w/2 - iS[0], self.h/2), (-self.w/2 + iS[1], self.h/2), n=nD_e))
            
        if self.bR[1] > 0:
            nD_e = int(_nD * sqrt(2)*iS[1]/_s)
            num_dot -= nD_e
            edges.append(Segment((-self.w/2 + iS[1], self.h/2), (-self.w/2, self.h/2 - iS[1]), n=nD_e))
            
        if not (self.bR[1] == self.bR[3] == 1 and self.h == self.w):
            nD_e = int(_nD * (self.h - iS[1] - iS[3])/_s)
            num_dot -= nD_e
            edges.append(Segment((-self.w/2, self.h/2 - iS[1]), (-self.w/2, -self.h/2 + iS[3]), n=nD_e))
            
        if self.bR[3] > 0:
            nD_e = int(_nD * sqrt(2)*iS[3]/_s)
            num_dot -= nD_e
            edges.append(Segment((-self.w/2, -self.h/2 + iS[3]), (-self.w/2 + iS[3], -self.h/2), n=nD_e))
            
        if not (self.bR[2] == self.bR[3] == 1 and self.h == self.w):
            nD_e = int(_nD * (self.w - iS[2] - iS[3])/_s)
            num_dot -= nD_e
            edges.append(Segment((-self.w/2 + iS[3], -self.h/2), (self.w/2 - iS[2], -self.h/2), n=nD_e))
            
        if self.bR[2] > 0:
            nD_e = num_dot if (self.bR[2] == self.bR[0] == 1 and self.h == self.w) else int(_nD * sqrt(2)*iS[2]/_s)
            num_dot -= nD_e
            edges.append(Segment((self.w/2 - iS[2], -self.h/2), (self.w/2, -self.h/2 + iS[2]), n=nD_e))
            
        if not (self.bR[2] == self.bR[0] == 1 and self.h == self.w):
            edges.append(Segment((self.w/2, -self.h/2 + iS[2]), (self.w/2, self.h/2 - iS[0]), n=num_dot))
            
        return connect_edges(*edges)
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD, tuple(self.bR)))


class RoundedRect(Geometry2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:int = 48,
        border_radius:Tuple[float, float, float, float] = (0.5, 0, 0, 0),
        **kwargs
    ) -> None:
        """
        A rectangular shape with rounded corners.
        
        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the geometry.
            w | width (float): width of the geometry.
            n | num_dot (int): number of dots consisting of the geometry.
            border_radius (float): denote the relative size of the corners of border edge,
                for each corners (top_left, top_right, bottom_left, bottom_right),
                using percentage values in range [0, 1].
                ex) border_radius = (1, 0, 1, 0.5) results in a geometry looks like
                
                        ''''''''''\)
                        |          \)
                        |          /)
                        (\......../)               
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] RoundedRect: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        self.bR = [border_radius[i] if len(border_radius) > i else 0 for i in range(4)]
        
        for i in range(4):
            if self.bR[i] < 0 or self.bR[i] > 1:
                raise ValueError(" \
                    [ERROR] RoundedRect: `border_radius` must be in (0 ~ 1) \
                ")

        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        iS = [i * min(self.h, self.w)/2 for i in self.bR]
        _s = 2*(self.h + self.w) - (2 - pi/2)*sum(iS)
        _nD = self.nD + 4 
        
        for i, j in [(0, 1), (1, 3), (2, 3), (2, 0)]:
            if self.bR[i] == self.bR[j] == 0:
                continue
            
            if self.h == self.w and self.bR[i] == self.bR[j] == 1:
                continue
            
            _nD += 1
        
        num_dot = _nD
        
        edges = []
        
        if self.bR[0] > 0:
            nD_e = int(_nD * (pi/2)*iS[0]/_s)
            num_dot -= nD_e
            _f = Arc(r=iS[0], n=nD_e, a=pi/2)
            _f.translate(self.w/2-iS[0], self.h/2-iS[0])
            edges.append(_f)
        
        if not (self.bR[0] == self.bR[1] == 1 and self.h == self.w):
            nD_e = int(_nD * (self.w - iS[0] - iS[1])/_s)
            num_dot -= nD_e
            edges.append(Segment((self.w/2 - iS[0], self.h/2), (-self.w/2 + iS[1], self.h/2), n=nD_e))
            
        if self.bR[1] > 0:
            nD_e = int(_nD * (pi/2)*iS[1]/_s)
            num_dot -= nD_e
            _f = Arc(r=iS[1], n=nD_e, a=pi/2)
            _f.rotate(pi/2)
            _f.translate(-self.w/2+iS[1], self.h/2-iS[1])
            edges.append(_f)
            
        if not (self.bR[1] == self.bR[3] == 1 and self.h == self.w):
            nD_e = int(_nD * (self.h - iS[1] - iS[3])/_s)
            num_dot -= nD_e
            edges.append(Segment((-self.w/2, self.h/2 - iS[1]), (-self.w/2, -self.h/2 + iS[3]), n=nD_e))
            
        if self.bR[3] > 0:
            nD_e = int(_nD * (pi/2)*iS[3]/_s)
            num_dot -= nD_e
            _f = Arc(r=iS[3], n=nD_e, a=pi/2)
            _f.rotate(pi)
            _f.translate(-self.w/2+iS[3], -self.h/2+iS[3])
            edges.append(_f)
            
        if not (self.bR[2] == self.bR[3] == 1 and self.h == self.w):
            nD_e = int(_nD * (self.w - iS[2] - iS[3])/_s)
            num_dot -= nD_e
            edges.append(Segment((-self.w/2 + iS[3], -self.h/2), (self.w/2 - iS[2], -self.h/2), n=nD_e))
            
        if self.bR[2] > 0:
            nD_e = num_dot if (self.bR[2] == self.bR[0] == 1 and self.h == self.w) else int(_nD * (pi/2)*iS[2]/_s)
            num_dot -= nD_e
            _f = Arc(r=iS[2], n=nD_e, a=pi/2)
            _f.rotate(3*pi/2)
            _f.translate(self.w/2-iS[2], -self.h/2+iS[2])
            edges.append(_f)
            
        if not (self.bR[2] == self.bR[0] == 1 and self.h == self.w):
            edges.append(Segment((self.w/2, -self.h/2 + iS[2]), (self.w/2, self.h/2 - iS[0]), n=num_dot))
            
        return connect_edges(*edges)
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD, tuple(self.bR)))
    

class Plaque(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float,
        n:int=64,
        border_radius:float = 0.25,
        **kwargs
    ) -> None:
        """
        Plaque shape with four snipped corners.

        Args:
            s | size (float): length of each side.
            n | num_dot (int): number of dots consisting of the geometry.
            border_radius (float): denote the size of the corners of border edge,
                using percentage values in range [0, 1].
        """
        self.uS, self.nD = s, n
        self.bR = border_radius
        
        if self.bR < 0 or self.bR > 1:
            raise ValueError(" \
                [ERROR] Plaque: `border_radius` must be in (0 ~ 1). \
            ")

        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = 1/np.abs(np.sin(2*theta) + 1e-6)
        rad = np.power(rad, 0.5)
        rad = self.uS * np.minimum(rad/(2 - self.bR), np.ones_like(theta))/2
        
        coord = to_cartesian(rad, theta)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD, self.bR))
    
    
class Ring(Geometry2D):
    @geminit({'major_radius':'R', 'minor_radius':'r', 'num_dot':'n'})
    def __init__(
        self,
        R:float = None,
        r:float = None,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        A round band, which has a hollow hole in the center.
        
        Args:
            R | major_radius (float): radius of the major circle.
            r | minor_radius (float): radius of the minor circle.
            n | num_dot (int): number of dots consisting of the geometry.
        """
        self.R, self.r, self.nD = R, r, n
        
        if self.r <= 0 or self.R <= 0:
            raise ValueError(" \
                [ERROR] Ring: radius should be positive number \
            ")

        if self.R <= self.r :
            raise ValueError(" \
                [ERROR] Ring: minor circle can't have radius larger than radius of major circle \
            ")
        
        super().__init__(
            planar=False,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        nR = ceil((8*(self.R - self.r))/self.R)
        _s = (nR + 1)*(self.R + self.r)/2
        _c = self.nD
        
        coord = []
        
        for i in range(nR+1):
            c = int((self.nD * (i*(self.R - self.r)/nR + self.r))//_s)
            
            if i == nR :
                c = _c
            
            _c -= c
            _f = Circle(r = self.r + i*(self.R-self.r)/nR, nD = c)
            
            coord.append(_f[:])        

        coord = np.concatenate(tuple(coord), axis=0)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.R, self.r, self.nD))


class BlockArc(Geometry2D):
    @geminit({'major_radius':'R', 'minor_radius':'r', 'angle':'a', 'num_dot':'n'})
    def __init__(
        self,
        R:float = None,
        r:float = None,
        a:float = pi/2,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        Arc shape that has two polar handles.
        
        Args:
            R | major_radius (float): radius of the major circle.
            r | minor_radius (float): radius of the minor circle.
            a | angle (float) : interior angle (unit: radian) of an arc.
            n | num_dot (int): number of dots consisting of the geometry.
        """
        self.R, self.r, self.aG, self.nD = R, r, a, n
        
        if self.r <= 0 or self.R <= 0:
            raise ValueError(" \
                [ERROR] BlockArc: radius should be positive number. \
            ")

        if self.R <= self.r :
            raise ValueError(" \
                [ERROR] BlockArc: minor circle can't have radius larger than radius of major circle. \
            ")
            
        if self.aG <= 0 or self.aG >= 2*pi:
            raise ValueError(" \
                [ERROR] BlockArc: interior angle should be in range (0, 2π). \
            ")
        
        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        _s = self.aG*(self.R + self.r) + 2*(self.R - self.r)
        _c = self.nD
        
        nD_edge = int((_c * (self.R-self.r))//_s)
        nD_major = int((_c*self.aG*self.R)//_s)
        nD_minor = _c - 2*nD_edge - nD_major
        
        theta_major = np.linspace(0, self.aG, nD_major+2)[1:-1]
        theta_minor = np.linspace(0, self.aG, nD_minor+2)[1:-1]
        
        rad_major = self.R*np.ones_like(theta_major)
        rad_minor = self.r*np.ones_like(theta_minor)
        
        coord_R = to_cartesian(rad_major, theta_major)
        coord_r = to_cartesian(rad_minor, theta_minor)[::-1]
        coord_e1 = Segment(
            p1=(self.r, 0), 
            p2=(self.R, 0),
            n = nD_edge
        )
        coord_e2 = Segment(
            p1=(self.R*cos(self.aG), self.R*sin(self.aG)), 
            p2=(self.r*cos(self.aG), self.r*sin(self.aG)),
            n = nD_edge
        )
    
        coord = np.concatenate((coord_e1, coord_R, coord_e2, coord_r), axis=0)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.R, self.r, self.nD, self.aG))


class Cross_A(Geometry2D):
    @geminit({'size':'s', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        w:float = None,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        A 2D shape comprised of intersecting lines or bars that are perpendicular to one another.

        Args:
            s | size (float): scale of the cross.
            w | width (float): interior width of the geometry.
            n | num_dot (int): number of dots consisting of each corner.
        """
        self.uS, self.w, self.nD = s, w, n
        
        if self.uS <= self.w:
            raise ValueError(" \
                [ERROR] Cross_A: The argument `width` should be shorter than the `size`. \
            ")

        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = self.uS
        _nD = self.nD + 2
        nD_h = int(_nD * (self.uS/2-self.w/2)/_s)
        nD_v = _nD - 2*nD_h
        
        bottom = Segment( 
            p1 = (self.w/2, -self.w/2), 
            p2 = (self.uS/2, -self.w/2),
            num_dot=nD_h
        )
        right = Segment(
            p1 = (self.uS/2, -self.w/2), 
            p2 = (self.uS/2, self.w/2),
            num_dot=nD_v
        )
        top = Segment(
            p1 = (self.uS/2, self.w/2), 
            p2 = (self.w/2, self.w/2),
            num_dot=nD_h
        )
        
        coord = []
        
        for i in range(4):
            _c = connect_edges(bottom, right, top)
            coord.append(rotate_2D(_c, i*pi/2))
        
        return np.concatenate(tuple(coord), axis=0)
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return 4*(self.nD-1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.w, self.nD))
    
    
class Cross_B(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        n:int = 128,
        border_radius:float = 0.25,
        **kwargs
    ) -> None:
        """
        Templar Cross.

        Args:
            s | size (float): scale of the cross.
            n | num_dot (int): number of dots consisting of the cross.
            border_radius (float): denote the size of the corners of border edge,
                using percentage values in range [0, 1]
        """
        self.uS, self.nD = s, n
        self.bR = border_radius
        
        if self.bR < 0 or self.bR > 1:
            raise ValueError(" \
                [ERROR] Cross_B: The argument `border_radius` must be in (0 ~ 1). \
            ")
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = 1/np.abs(np.sin(2*theta) + 1e-6)
        rad = np.power(rad, 2.5)
        rad = self.uS * np.minimum(rad/(2 - self.bR), np.ones_like(theta))/2
        
        coord = to_cartesian(rad, theta)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD, self.bR))
    
    
class Cross_C(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        n:int = 10,
        **kwargs
    ) -> None:
        """
        Maltese cross, consisting of four "V" or arrowhead shaped concave quadrilaterals.

        Args:
            s | size (float): scale of the cross.
            n | num_dot (int): number of dots consisting of each side.
        """
        self.uS, self.nD = s, n
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        coord = []
        
        for i in range(4):
            _h = self.uS/2
            _w = self.uS/3
            f = ConcaveKite(s=(_h, _w), n=[self.nD//2, self.nD, self.nD, self.nD//2])
            f.translateY(2*_w*_h/(2*_h + _w))
            f.rotate(pi*i/2)
            coord.append(f[1:])

        return np.concatenate(tuple(coord), axis=0)
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return 4*(2*self.nD + 2*(self.nD//2) - 5)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))
    

class SunCross(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        n:int = 192,
        **kwargs
    ) -> None:
        """
        A cross symbol consisting of an equilateral cross inside a circle.

        Args:
            s | size (float): scale of the cross.
            n | num_dot (int): number of dots consisting of the cross.
        """
        self.uS, self.nD = s, n
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = self.uS*(4 + 3*pi)/2
        self.nD_ic = nD_ic = int(self.nD*self.uS*(pi/8 + 1/2)/_s)
        self.nD_oc = nD_oc = self.nD - 4*nD_ic

        f_oc = Circle(self.uS/2, nD_oc)
        coord = [f_oc[:]]

        for i, m in enumerate([[1, 1], [-1, 1], [-1, -1], [1, -1]]):
            f_ls = CircularSector(self.uS/4, pi/2, nD_ic)
            f_ls.rotate(i*pi/2)
            f_ls.translate(m[0]*self.uS/8, m[1]*self.uS/8)
            coord.append(f_ls[:])
            
        return np.concatenate(tuple(coord), axis=0)
    
    def _linear_paths(self) -> Tuple[list, list]:
        eidx = [linear_ring(self.nD_oc)]
        iidx = [linear_ring(self.nD_oc + i*self.nD_ic, self.nD_oc + (i+1)*self.nD_ic) for i in range(4)]

        return eidx, iidx

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))
    

class CelticCross(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        n:int = 192,
        **kwargs
    ) -> None:
        """
        A hooked cross with four comma-shaped heads.

        Args:
            s | size (float): scale of the cross.
            n | num_dot (int): number of dots consisting of each head.
        """
        self.uS, self.nD = s, n
        
        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        _s = self.uS * (20 + 6*pi)/7
        _nD = self.nD + 16
        self.nD_e = nD_e = int(_nD*self.uS*(1/7)/_s)
        self.nD_c = nD_c = int(_nD*self.uS*(pi/7)/_s)
        self.nD_i = nD_i = int((_nD - 12*nD_e - 4*nD_c)/4)

        coord = []

        for i in range(4):
            _iar = CircularSector(self.uS/7, pi/2, nD_i)
            _iar.translate(self.uS/14, self.uS/14)
            _iar.rotate(i*pi/2)
            coord.append(_iar[:])

        for i in range(4):
            _e1 = Segment((self.uS*5/14, -self.uS/14), (self.uS/2, -self.uS/14), n=nD_e)
            _e2 = Segment((self.uS/2, -self.uS/14), (self.uS/2, self.uS/14), n=nD_e)
            _e3 = Segment((self.uS/2, self.uS/14), (self.uS*5/14, self.uS/14), n=nD_e)
            _ar = Arc(self.uS*2/7, pi/2, nD_c + (0 if i < 3 else _nD - 12*nD_e - 4*(nD_c + nD_i)))
            _ar.translate(self.uS/14, self.uS/14)

            _c = connect_edges(_e1, _e2, _e3, _ar)
            _c = rotate_2D(_c, i*pi/2)

            coord.append(_c)
        
        return np.concatenate(tuple(coord), axis=0)
    
    def _linear_paths(self) -> Tuple[list, list]:
        eidx = [linear_ring(4*self.nD_i, self.nD)]
        iidx = [linear_ring(i*self.nD_i, (i+1)*self.nD_i) for i in range(4)]

        return eidx, iidx

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))


class BasqueCross(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        A hooked cross with four comma-shaped heads.

        Args:
            s | size (float): height/width of the cross.
            n | num_dot (int): number of dots consisting of each heads.
        """
        self.uS, self.nD = s, n
        
        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        _s = self.uS*pi
        _nD = self.nD + 3
        self.nD_r = nD_r = int(_nD*(pi*self.uS/4)/_s)
        self.nD_R = nD_R = _nD - 2*nD_r

        coord = []

        for i in range(4):
            _aR = Arc(r = self.uS/4, n = nD_R, a = pi)
            _ar_1 = Arc(r = self.uS/8, n = nD_r, a = pi)
            _ar_2 = Arc(r = self.uS/8, n = nD_r, a = pi)

            _aR.rotate(3*pi/2)
            _ar_1.rotate(pi/2)
            _ar_2.rotate(pi/2)
            _ar_2.flipY()

            _aR.translateY(self.uS/4)
            _ar_1.translateY(3*self.uS/8)
            _ar_2.translateY(self.uS/8)

            _c = connect_edges(_aR, _ar_1, _ar_2)
            _c = rotate_2D(_c, i*pi/2)
            coord.append(_c)
        
        return np.concatenate(tuple(coord), axis=0)
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return 4*self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))


class Lshape(Geometry2D):
    @geminit({'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        w:float = None,
        n:int = 10,
        **kwargs
    ) -> None:
        """
        Shape like the letter `L`, made of two perpendicular rectangles with equal width.

        Args:
            w | width (float): interior width of the geometry.
            n | num_dot (int): number of dots consisting of each edges.
        """
        self.uS, self.nD = w, n
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        top_1 = Segment(
            p1 = (self.uS, 0), 
            p2 = (0, 0),
            num_dot=self.nD
        )
        right_1 = Segment(
            p1 = (0, 0), 
            p2 = (0, self.uS),
            num_dot=self.nD
        )
        top_2 = Segment(
            p1 = (0, self.uS), 
            p2 = (-self.uS, self.uS),
            num_dot=self.nD
        )
        left = Segment( 
            p1 = (-self.uS, self.uS), 
            p2 = (-self.uS, -self.uS),
            num_dot=2*self.nD-1
        )
        bottom = Segment(
            p1 = (-self.uS, -self.uS), 
            p2 = (self.uS, -self.uS),
            num_dot=2*self.nD-1
        )
        right_2 = Segment(
            p1 = (self.uS, -self.uS), 
            p2 = (self.uS, 0),
            num_dot=self.nD
        )

        coord = connect_edges(top_1, right_1, top_2, left, bottom, right_2)
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return 8*self.nD - 8
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))


class HalfFrame(Geometry2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        breadth:float = None,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        Half frame shape.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the frame.
            w | width (float): width of the frame.
            breadth | (float): breadth of the frame.
            n | num_dot (int): number of dots consisting of the geometry.
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] HalfFrame: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        self.iw = breadth

        if self.iw >= min(self.h, self.w)/2:
            raise ValueError(" \
                [ERROR] HalfFrame: The breadth of the frame must be less than the half of height (or width). \
            ")
        
        super().__init__(
            planar=True,
            **kwargs
        )

    def _base_coords(self) -> np.ndarray:
        _s = 2*(self.h + self.w) + 2*(sqrt(2) - 2)*self.iw
        _nD = self.nD + 6
        self.nD_d = nD_d = int(_nD * (sqrt(2)*self.iw)/_s)
        self.nD_r = nD_r = int(_nD * (self.h - 2*self.iw)/_s)
        self.nD_b = nD_b = int(_nD * (self.w - 2*self.iw)/_s)
        self.nD_l = nD_l = int(_nD * (self.h)/_s)
        self.nD_t = nD_t = _nD - (2*nD_d + nD_r + nD_b + nD_l)

        top = Segment( 
            p1 = (self.w/2, self.h/2), 
            p2 = (-self.w/2, self.h/2),
            num_dot=nD_t
        )
        left = Segment( 
            p1 = (-self.w/2, self.h/2), 
            p2 = (-self.w/2, -self.h/2),
            num_dot=nD_l
        )
        diagonal_1 = Segment(
            p1 = (-self.w/2, -self.h/2), 
            p2 = (-self.w/2 + self.iw, -self.h/2 + self.iw),
            num_dot=nD_d
        )
        right = Segment(
            p1 = (-self.w/2 + self.iw, -self.h/2 + self.iw), 
            p2 = (-self.w/2 + self.iw, self.h/2 - self.iw),
            num_dot=nD_r
        )
        bottom = Segment( 
            p1 = (-self.w/2 + self.iw, self.h/2 - self.iw), 
            p2 = (self.w/2 - self.iw, self.h/2 - self.iw),
            num_dot=nD_b
        )
        diagonal_2 = Segment(
            p1 = (self.w/2 - self.iw, self.h/2 - self.iw),
            p2 = (self.w/2, self.h/2),
            num_dot=nD_d
        )

        coord = connect_edges(top, left, diagonal_1, right, bottom, diagonal_2)
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.iw, self.nD))


class Arrow(Geometry2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        A graphical symbol, such as ← or →, or a pictogram, used to point or indicate direction.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the arrow.
            W | width (float): width of the arrow.
            n | num_dot (int): number of dots consisting of the arrow.
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Arrow: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = (5 - sqrt(5))*self.h/2 + 2*self.w
        _nD = self.nD + 7
        self.nD_d = nD_d = int(_nD*(3*self.h/4)/_s)
        self.nD_r = nD_r = int(_nD*(self.h/4)/_s)
        self.nD_h = nD_h = int(_nD*(self.w - sqrt(5)*self.h/4)/_s)
        self.nD_l = nD_l = _nD - 2*(nD_d + nD_r + nD_h)
        
        diagonal_1 = Segment( 
            p1 = (self.w/2, 0), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, self.h/2),
            num_dot=nD_d
        )
        right_1 = Segment(
            p1 = (self.w/2 - sqrt(5)*self.h/4, self.h/2), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, self.h/4),
            num_dot=nD_r
        )
        top = Segment(
            p1 = (self.w/2 - sqrt(5)*self.h/4, self.h/4), 
            p2 = (-self.w/2, self.h/4),
            num_dot=nD_h
        )
        left = Segment(
            p1 = (-self.w/2, self.h/4), 
            p2 = (-self.w/2, -self.h/4),
            num_dot=nD_l
        )
        bottom = Segment(
            p1 = (-self.w/2, -self.h/4), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, -self.h/4),
            num_dot=nD_h
        )
        right_2 = Segment(
            p1 = (self.w/2 - sqrt(5)*self.h/4, -self.h/4), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, -self.h/2),
            num_dot=nD_r
        )
        diagonal_2 = Segment( 
            p1 = (self.w/2 - sqrt(5)*self.h/4, -self.h/2), 
            p2 = (self.w/2, 0),
            num_dot=nD_d
        )

        coord = connect_edges(diagonal_1, right_1, top, left, bottom, right_2, diagonal_2)
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD))


class DoubleArrow(Geometry2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        Left Right Arrow.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the arrow.
            W | width (float): width of the arrow.
            n | num_dot (int): number of dots consisting of the arrow.
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] DoubleArrow: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = (4 - sqrt(5))*self.h + 2*self.w
        _nD = self.nD + 10
        self.nD_d = nD_d = int(_nD*(3*self.h/4)/_s)
        self.nD_v = nD_v = int(_nD*(self.h/4)/_s)
        self.nD_h = nD_h = int((_nD - 4*(nD_d + nD_v))/2)
        _nD -= (4*(nD_d + nD_v) + 2*nD_h)
        
        diagonal_1 = Segment(
            p1 = (self.w/2, 0), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, self.h/2),
            num_dot=nD_d
        )
        vertical_1 = Segment( 
            p1 = (self.w/2 - sqrt(5)*self.h/4, self.h/2), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, self.h/4),
            num_dot=nD_v
        )
        top = Segment(
            p1 = (self.w/2 - sqrt(5)*self.h/4, self.h/4), 
            p2 = (-self.w/2 + sqrt(5)*self.h/4, self.h/4),
            num_dot=nD_h
        )
        vertical_2 = Segment(
            p1 = (-self.w/2 + sqrt(5)*self.h/4, self.h/4), 
            p2 = (-self.w/2 + sqrt(5)*self.h/4, self.h/2),
            num_dot=nD_v
        )
        diagonal_2 = Segment(
            p1 = (-self.w/2 + sqrt(5)*self.h/4, self.h/2), 
            p2 = (-self.w/2, 0),
            num_dot=nD_d
        )
        diagonal_3 = Segment(
            p1 = (-self.w/2, 0), 
            p2 = (-self.w/2 + sqrt(5)*self.h/4, -self.h/2),
            num_dot=nD_d
        )
        vertical_3 = Segment( 
            p1 = (-self.w/2 + sqrt(5)*self.h/4, -self.h/2), 
            p2 = (-self.w/2 + sqrt(5)*self.h/4, -self.h/4),
            num_dot=nD_v
        )
        bottom = Segment(
            p1 = (-self.w/2 + sqrt(5)*self.h/4, -self.h/4), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, -self.h/4),
            num_dot=nD_h + _nD
        )
        vertical_4 = Segment(
            p1 = (self.w/2 - sqrt(5)*self.h/4, -self.h/4), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, -self.h/2),
            num_dot=nD_v
        )
        diagonal_4 = Segment( 
            p1 = (self.w/2 - sqrt(5)*self.h/4, -self.h/2), 
            p2 = (self.w/2, 0),
            num_dot=nD_d
        )

        coord = connect_edges(
            diagonal_1, 
            vertical_1, 
            top, 
            vertical_2, 
            diagonal_2, 
            diagonal_3,
            vertical_3,
            bottom, 
            vertical_4,
            diagonal_4
        )
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD))
      

class ArrowPentagon(Geometry2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        Arrow (pentagon shape).

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the arrow.
            W | width (float): width of the arrow.
            n | num_dot (int): number of dots consisting of each edges.
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] ArrowPentagon: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = (5 - sqrt(5))*self.h/2 + 2*self.w
        _nD = self.nD + 5
        self.nD_d = nD_d = int(_nD*(3*self.h/4)/_s)
        self.nD_h = nD_h = int(_nD*(self.w - sqrt(5)*self.h/4)/_s)
        self.nD_v = nD_v = _nD - 2*(nD_d + nD_h)
        
        diagonal_1 = Segment(
            p1 = (self.w/2, 0), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, self.h/2),
            num_dot=nD_d
        )
        top = Segment(
            p1 = (self.w/2 - sqrt(5)*self.h/4, self.h/2), 
            p2 = (-self.w/2, self.h/2),
            num_dot=nD_h
        )
        left = Segment(
            p1 = (-self.w/2, self.h/2), 
            p2 = (-self.w/2, -self.h/2),
            num_dot=nD_v
        )
        bottom = Segment(
            p1 = (-self.w/2, -self.h/2), 
            p2 = (self.w/2 - sqrt(5)*self.h/4, -self.h/2),
            num_dot=nD_h
        )
        diagonal_2 = Segment(
            p1 = (self.w/2 - sqrt(5)*self.h/4, -self.h/2), 
            p2 = (self.w/2, 0),
            num_dot=nD_d
        )

        coord = connect_edges(diagonal_1, top, left, bottom, diagonal_2)
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD))
    

class ArrowChevron(Geometry2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        Arrow chevron symbol that has a sharp bend to the left or right.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the arrow.
            W | width (float): width of the arrow.
            n | num_dot (int): number of dots consisting of each edges.
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] ArrowChevron: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = self.w + 2*sqrt(self.h**2 + self.w**2)
        _nD = self.nD + 6
        self.nD_d = nD_d = int(_nD*(sqrt(self.h**2 + self.w**2)/2)/_s)
        self.nD_h = nD_h = int(_nD*(self.w/2)/_s)
        _nD -= (4*nD_d + 2*nD_h)
        
        diagonal_1 = Segment( 
            p1 = (self.w/2, 0), 
            p2 = (0, self.h/2),
            num_dot=nD_d
        )
        top = Segment(
            p1 = (0, self.h/2), 
            p2 = (-self.w/2, self.h/2),
            num_dot=nD_h
        )
        diagonal_2 = Segment(
            p1 = (-self.w/2, self.h/2), 
            p2 = (0, 0),
            num_dot=nD_d
        )
        diagonal_3 = Segment(
            p1 = (0, 0), 
            p2 = (-self.w/2, -self.h/2),
            num_dot=nD_d
        )
        bottom = Segment(
            p1 = (-self.w/2, -self.h/2), 
            p2 = (0, -self.h/2),
            num_dot=nD_h + _nD
        )
        diagonal_4 = Segment(
            p1 = (0, -self.h/2), 
            p2 = (self.w/2, 0),
            num_dot=nD_d
        )

        coord = connect_edges(diagonal_1, top, diagonal_2, diagonal_3, bottom, diagonal_4)
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD))
    
    
class Teardrop(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        n:int = 32,
        **kwargs
    ) -> None:
        """
        Teardrop 2D shape (bottom half circle, top-half kindof diamond shape).

        Args:
            s | size (float): scale of the geometry.
            n | num_dot (int): number of dots consisting of the geometry.
        """
        self.uS, self.nD = s, n
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = self.uS*(3*pi/2 + 2)/2
        _nD = self.nD + 3
        self.nD_e = nD_e = int(_nD*(self.uS/2)/_s)
        self.nD_a = nD_a = _nD - 2*nD_e
        
        right = Segment(
            p1 = (self.uS*cos(pi/4)/2, self.uS*sin(pi/4)/2), 
            p2 = (0, sqrt(2)*self.uS/2),
            num_dot=nD_e
        )
        left = Segment(
            p1 = (0, sqrt(2)*self.uS/2), 
            p2 = (-self.uS*cos(pi/4)/2, self.uS*sin(pi/4)/2),
            num_dot=nD_e
        )

        arc = Arc(r=self.uS/2, n=nD_a, a=3*pi/2)
        arc.rotate(3*pi/4)
        
        coord = connect_edges(right, left, arc)

        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))
    

class Nosign(Geometry2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        n:int = 64,
        **kwargs
    ) -> None:
        """
        `No` sign, circle-backslash symbol.

        Args:
            s | size (float): scale of the geometry.
            n | num_dot (int): number of dots consisting of the geometry.
        """
        self.uS, self.nD = s, n
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        _s = self.uS*(sqrt(3) + 8*pi/3)/2
        self.nD_ic = nD_ic = int(self.nD*(pi*self.uS/6 + sqrt(3)*self.uS/4)/_s)
        self.nD_oc = nD_oc = self.nD - 2*self.nD_ic

        f_oc = Circle(self.uS/2, nD_oc)
        f_ls = CircularSegment(self.uS/4, 2*pi/3, nD_ic)
        f_1 = f_ls.copy()
        f_1.rotate(23*pi/12)
        f_2 = f_ls.copy()
        f_2.rotate(11*pi/12)

        coord = np.concatenate((f_oc[:], f_1[:], f_2[:]), axis=0)
        
        return coord
    
    def _linear_paths(self) -> Tuple[list, list]:
        _e = [linear_ring(self.nD_oc)]
        _i = [
            linear_ring(self.nD_oc, self.nD_oc + self.nD_ic),
            linear_ring(self.nD_oc + self.nD_ic, self.nD_oc + 2*self.nD_ic)
        ]

        return _e, _i

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD))