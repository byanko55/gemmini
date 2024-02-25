from gemmini.misc import *
from gemmini.d2._gem2D import Geometry2D
from gemmini.d2.line2D import Segment
from gemmini.calc.geometry import connect_edges
from gemmini.calc.coords import _isNumber, _isPoint, rotate_2D


class Polygon2D(Geometry2D):
    def __init__(
        self,
        v:Union[list, np.ndarray] = None,
        **kwargs
    ) -> None:
        """
        A 2D plane figure made up of line segments connected to form a closed polygonal chain.

        Args:
            vertices (Union[list, np.ndarray]): set of polygon's vertices (or corners).
        """
        gem_type = 'Polygon2D'
        
        if 'gem_type' in kwargs:
            gem_type = kwargs['gem_type']
            del kwargs['gem_type']
        
        self.v = assignArg(gem_type, [v], ['vertices'], kwargs)
        
        super().__init__(
            gem_type=gem_type,
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        return self.v

    def __len__(self) -> int:
        return NotImplementedError
    
    def __hash__(self) -> int:
        return super().__hash__()
    

def line_segment2D(p1:Tuple[float, float], p2:Tuple[float, float]):
    """
    A one-dimensional line segment joining two vertices
    
    Args:
        p1, p2 (float, float): coordinates of two vertices
    """
    if not _isPoint(p1, dim=2) or not _isPoint(p2, dim=2):
        raise ValueError(" \
            [ERROR] line_segment2D: check every points to conform the 2D format (x, y) \
        ")
    
    return Polygon2D(vertices=[p1, p2])


class RegularPolygon(Polygon2D):
    def __init__(
        self,
        s:float = None,
        nD:int = None,
        nV:int = None,
        **kwargs
    ):
        """
        A polygon whose angles are all equal, and all sides have the same length.

        Args:
            s | size (float): length of each side
            nD | num_dot (int): number of dots consisting of a edge
            nV | num_vertex (int): number of vertex
        """
        gem_type = self.__class__.__name__

        self.uS, self.nD, self.nV = assignArg(
            gem_type, 
            [s, nD, nV], 
            ['size', 'num_dot', 'num_vertex'], 
            kwargs
        )

        if self.nV < 3 :
            raise ValueError("[ERROR] %s should have at least 3 vertices"%(gem_type))

        if self.nD < 2 :
            raise ValueError("[ERROR] %s: each side must have at least 2 dots"%(gem_type))
        
        coord = np.array([
            [self._draw_edge(i, self.nD-j-1) for j in reversed(range(self.nD-1))] for i in range(self.nV)
        ])

        coord = coord.reshape(-1, coord.shape[-1])
        
        super().__init__(
            vertices=coord, 
            gem_type=gem_type, 
            **kwargs
        )
    
    def _draw_edge(self, v, e):
        dx = -self.uS/2 + self.uS*e/(self.nD-1)
        dy = -self.uS/(2*tan(pi/self.nV))
        
        rx, ry = rotate_2D((dx, dy), 2*v*pi/self.nV)
        
        return rx, ry

    def __len__(self) -> int:
        return self.nV*(self.nD-1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD, self.nV))
    
    
class IsoscelesTriangle(Polygon2D):
    def __init__(
        self,
        h:float = None,
        w:float = None,
        nD:int = None,
        **kwargs
    ):
        """
        A triangle that has two sides of equal length.

        Args:
            h | height (float): height of triangle
            w | width (float): base length of the triangle
            nD | num_dot (int): number of dots consisting of a edge
        """
        gem_type = self.__class__.__name__

        self.h, self.w, self.nD = assignArg(
            gem_type, 
            [h, w, nD], 
            ['height', 'width', 'num_dot'], 
            kwargs
        )
        
        right = Segment(
            num_dot=self.nD, 
            p1 = (self.w/2, -self.h/3), 
            p2 = (0, 2*self.h/3)
        )
        left = Segment(
            num_dot=self.nD, 
            p1 = (0, 2*self.h/3), 
            p2 = (-self.w/2, -self.h/3),
        )
        base = Segment(
            num_dot=self.nD, 
            p1 = (-self.w/2, -self.h/3), 
            p2 = (self.w/2, -self.h/3)
        )
        
        super().__init__(
            vertices=connect_edges(right, left, base), 
            gem_type=gem_type, 
            **kwargs
        )
        
    def __len__(self) -> int:
        return 3*(self.nD - 1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD))
        

class RightTriangle(Polygon2D):
    def __init__(
        self,
        h:float = None,
        w:float = None,
        nD:int = None,
        **kwargs
    ):
        """
        A triangle that has one of its interior angles measuring 90°

        Args:
            h | height (float): height of triangle
            w | width (float): base length of the triangle
            nD | num_dot (int): number of dots consisting of a edge
        """
        gem_type = self.__class__.__name__

        self.h, self.w, self.nD = assignArg(
            gem_type, 
            [h, w, nD], 
            ['height', 'width', 'num_dot'], 
            kwargs
        )
        
        right = Segment(
            num_dot=self.nD, 
            p1 = (2*self.w/3, -self.h/3), 
            p2 = (-self.w/3, 2*self.h/3),
        )
        left = Segment(
            num_dot=self.nD, 
            p1 = (-self.w/3, 2*self.h/3), 
            p2 = (-self.w/3, -self.h/3)
        )
        base = Segment(
            num_dot=self.nD, 
            p1 = (-self.w/3, -self.h/3), 
            p2 = (2*self.w/3, -self.h/3)
        )
        
        super().__init__(
            vertices=connect_edges(right, left, base), 
            gem_type=gem_type, 
            **kwargs
        )
        
    def __len__(self) -> int:
        return 3*(self.nD - 1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD))


class Parallelogram(Polygon2D):
    def __init__(
        self,
        h:float = None,
        w:float = None,
        nY:int = None,
        nX:int = None,
        a:float = None,
        **kwargs
    ):
        """
        A quadrilateral which is made up of 2 pairs of parallel sides.

        Args:
            h | height (float): length of vertical edge
            w | width (float): length of horizontal edge
            nY | num_ydot (int): number of dots consisting of a vertical edge
            nX | num_xdot (int): number of dots consisting of a horizontal edge
            a | angle (float): interior angle (unit: radian)
        """
        gem_type = self.__class__.__name__

        self.h, self.w, self.nY, self.nX, self.aG = assignArg(
            gem_type, 
            [h, w, nY, nX, a], 
            ['height', 'width', 'num_ydot', 'num_xdot', 'angle'], 
            kwargs
        )

        if self.nX < 2 or self.nY < 2 :
            raise ValueError("[ERROR] %s: each side should consist of at least 2 dots"%(gem_type))
        
        top = Segment(
            num_dot=self.nX, 
            p1 = ((-self.w + self.h*cos(self.aG))/2, self.h*sin(self.aG)/2), 
            p2 = ((self.w + self.h*cos(self.aG))/2, self.h*sin(self.aG)/2)
        )
        right = Segment(
            num_dot=self.nY, 
            p1 = ((self.w + self.h*cos(self.aG))/2, self.h*sin(self.aG)/2), 
            p2 = ((self.w - self.h*cos(self.aG))/2, -self.h*sin(self.aG)/2)
        )
        bottom = Segment(
            num_dot=self.nX, 
            p1 = ((self.w - self.h*cos(self.aG))/2, -self.h*sin(self.aG)/2), 
            p2 = ((-self.w - self.h*cos(self.aG))/2, -self.h*sin(self.aG)/2)
        )
        left = Segment(
            num_dot=self.nY, 
            p1 = ((-self.w - self.h*cos(self.aG))/2, -self.h*sin(self.aG)/2), 
            p2 = ((-self.w + self.h*cos(self.aG))/2, self.h*sin(self.aG)/2)
        )
        
        super().__init__(
            vertices=connect_edges(top, right, bottom, left), 
            gem_type=gem_type, 
            **kwargs
        )
        
    def __len__(self) -> int:
        return 2*(self.nX + self.nY - 2)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nY, self.nX, self.aG))
    
    
class Rhombus(Polygon2D):
    def __init__(
        self,
        h:float = None,
        w:float = None,
        nD:int = None,
        **kwargs
    ):
        """
        A quadrilateral whose four sides all have the same length.

        Args:
            h | height (float): length of vertical diagonals
            w | width (float): length of horizontal diagonals
            nD | num_dot (int): number of dots consisting of a edge
        """
        gem_type = self.__class__.__name__

        self.h, self.w, self.nD = assignArg(
            gem_type, 
            [h, w, nD], 
            ['height', 'width', 'num_dot'], 
            kwargs
        )

        if self.nD < 2 :
            raise ValueError("[ERROR] %s: each side must have at least 2 dots"%(gem_type))
        
        top = Segment(
            num_dot=self.nD, 
            p1 = (0, self.h/2), 
            p2 = (self.w/2, 0)
        )
        right = Segment(
            num_dot=self.nD, 
            p1 = (self.w/2, 0), 
            p2 = (0, -self.h/2)
        )
        bottom = Segment(
            num_dot=self.nD, 
            p1 = (0, -self.h/2), 
            p2 = (-self.w/2, 0)
        )
        left = Segment(
            num_dot=self.nD, 
            p1 = (-self.w/2, 0), 
            p2 = (0, self.h/2)
        )

        super().__init__(
            vertices=connect_edges(top, right, bottom, left),
            gem_type=gem_type, 
            **kwargs
        )

    def __len__(self) -> int:
        return 4*(self.nD - 1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nD))
    

class Trapezoid(Polygon2D):
    def __init__(
        self,
        h:float = None,
        wt:float = None,
        wb:float = None,
        nD:Union[int, Tuple[int, int, int]] = None,
        opt:float = 0,
        **kwargs
    ):
        """
        A quadrilateral that has at least one pair of parallel sides.
        
        Args:
            h | height (float): height of the trapezoid
            wt | width_top (float): width of the top side
            wb | width_bottom (float): width of the bottom side
            nD | num_dot (int | (int, int, int)): number of dots consisting of top/bottom/vertical side
                If a single numeric value is given, then every edge have the same number of dots.
                Or, you can determine the number of dots in each sides differently by giving a tuple for the `num_dot` argument. 
                ex) num_dot = (2,4,5): top=2, bottom=4, vertical edge=5
            opt (float, optional): determine the position in x-aixs of the top side
                `opt=k` will translate the top side to the left as much as `k`.
        """
        gem_type = self.__class__.__name__

        self.h, self.wt, self.wb, nD = assignArg(
            gem_type, 
            [h, wt, wb, nD], 
            ['height', 'width_top', 'width_bottom', 'num_dot'], 
            kwargs
        )

        self.translate_top = opt

        if _isNumber(nD):
            self.ntD, self.nbD, self.nsD = map(int, [nD]*3)
        else :
            self.ntD, self.nbD, self.nsD = nD

        if self.nbD < 2 or self.ntD < 2 or self.nsD < 2 :
            raise ValueError("[ERROR] %s: each side should consist of at least 2 dots"%(gem_type))
        
        top = Segment(
            num_dot=self.ntD, 
            p1 = (-self.wt/2 + self.translate_top, self.h/2), 
            p2 = (self.wt/2 + self.translate_top, self.h/2)
        )
        right = Segment(
            num_dot=self.nsD, 
            p1 = (self.wt/2 + self.translate_top, self.h/2), 
            p2 = (self.wb/2, -self.h/2)
        )
        bottom = Segment(
            num_dot=self.nbD, 
            p1 = (self.wb/2, -self.h/2), 
            p2 = (-self.wb/2, -self.h/2)
        )
        left = Segment(
            num_dot=self.nsD, 
            p1 = (-self.wb/2, -self.h/2), 
            p2 = (-self.wt/2 + self.translate_top, self.h/2)
        )

        super().__init__(
            vertices=connect_edges(top, right, bottom, left),
            gem_type=gem_type, 
            **kwargs
        )

    def __len__(self) -> int:
        return self.nbD + self.ntD + 2*self.nsD - 4
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.wt, self.wb, self.ntD, self.nbD, self.nsD))
    

def RightTrapezoid(
    h:float = None,
    wt:float = None,
    wb:float = None,
    nD:Union[int, Tuple[int, int, int]] = None,
    **kwargs
):
    """
    A right trapezoid has two adjacent right angles.

    Args:
        h | height (float): height of the trapezoid
        wt | width_top (float): width of the top side
        wb | width_bottom (float): width of the bottom side
        nD | num_dot (int | (int, int, int)): number of dots consisting of top/bottom/vertical side
            If a single numeric value is given, then every edge have the same number of dots.
            Or, you can determine the number of dots in each sides differently by giving a tuple for the `num_dot` argument. 
            ex) num_dot = (2,4,5): top=2, bottom=4, vertical edge=5
    """
    return Trapezoid(h, wt, wb, nD, (wt-wb)/2, **kwargs)
    

class Rectangle(Polygon2D):
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
            nD | num_dot (int | (int, int)): number of dots consisting of horizontal/vertical side
                If a single numeric value is given, then every edge have the same number of dots.
                Or, you can determine the number of dots in each sides differently by giving a tuple for the `num_dot` argument. 
                ex) num_dot = (2,4): horizontal edge=2, vertical edge=4
        """
        gem_type = self.__class__.__name__

        self.h, self.w, nD = assignArg(
            gem_type, 
            [h, w, nD], 
            ['height', 'width', 'num_dot'], 
            kwargs
        )

        if _isNumber(nD):
            self.nwD, self.nhD = map(int, [nD]*2)
        else :
            self.nwD, self.nhD = nD

        if self.nwD < 2 or self.nhD < 2 :
            raise ValueError("[ERROR] %s: each side should consist of at least 2 dots"%(gem_type))

        top = Segment(
            num_dot=self.nwD, 
            p1 = (-self.w/2, self.h/2), 
            p2 = (self.w/2, self.h/2)
        )
        right = Segment(
            num_dot=self.nhD, 
            p1 = (self.w/2, self.h/2), 
            p2 = (self.w/2, -self.h/2)
        )
        bottom = Segment(
            num_dot=self.nwD, 
            p1 = (self.w/2, -self.h/2), 
            p2 = (-self.w/2, -self.h/2)
        )
        left = Segment(
            num_dot=self.nhD, 
            p1 = (-self.w/2, -self.h/2), 
            p2 = (-self.w/2, self.h/2)
        )

        super().__init__(
            vertices=connect_edges(top, right, bottom, left),
            gem_type=gem_type, 
            **kwargs
        )

    def __len__(self) -> int:
        return 2*(self.nwD + self.nhD - 2)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, self.nwD, self.nhD))


class Kite(Polygon2D):
    def __init__(
        self,
        a:float,
        b:float,
        nD:int = None,
        **kwargs
    ):
        """
        A quadrilateral with reflection symmetry across a diagonal.

        Args:
            a, b (float, float): length of each side
            nD | num_dot (int): number of dots consisting of a edge
        """
        gem_type = self.__class__.__name__
        
        self.a = min(a, b)
        self.b = max(a, b)

        self.nD = assignArg(gem_type, [nD], ['num_dot'], kwargs)

        if self.nD < 2 :
            raise ValueError("[ERROR] %s: each side should consist of at least 2 dots"%(gem_type))

        _a = self.a/sqrt(self.a*self.a + self.b*self.b)
        _b = self.b/sqrt(self.a*self.a + self.b*self.b)
        
        top = Segment(
            num_dot=self.nD, 
            p1 = (0, self.a*_a), 
            p2 = (self.a*_b, 0)
        )
        right = Segment(
            num_dot=self.nD, 
            p1 = (self.a*_b, 0), 
            p2 = (0, -self.b*_b)
        )
        bottom = Segment(
            num_dot=self.nD, 
            p1 = (0, -self.b*_b), 
            p2 = (-self.a*_b, 0)
        )
        left = Segment(
            num_dot=self.nD, 
            p1 = (-self.a*_b, 0), 
            p2 = (0, self.a*_a)
        )

        super().__init__(
            vertices=connect_edges(bottom, left, top, right),
            gem_type=gem_type, 
            **kwargs
        )

    def __len__(self) -> int:
        return 4*(self.nD - 1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.a, self.b, self.nD))
    
    
class ConcaveKite(Polygon2D):
    def __init__(
        self,
        a:float,
        b:float,
        nD:int = None,
        **kwargs
    ):
        """
        A Kite shape, but the line through one of the diagonals bisects the other.

        Args:
            a, b (float, float): length of each side
            nD | num_dot (int): number of dots consisting of a edge
        """
        gem_type = self.__class__.__name__
        
        self.a = min(a, b)
        self.b = max(a, b)

        self.nD = assignArg(gem_type, [nD], ['num_dot'], kwargs)

        if self.nD < 2 :
            raise ValueError("[ERROR] %s: each side should consist of at least 2 dots"%(gem_type))

        _s = self.a/sqrt(self.a*self.a + self.b*self.b)
        _c = self.b/sqrt(self.a*self.a + self.b*self.b)
        _t2 = 2*self.a*self.b/(self.b**2 - self.a**2)
        
        top = Segment(
            num_dot=self.nD, 
            p1 = (0, self.a*_s), 
            p2 = ((self.b + self.a*_t2)*_s, (self.b + self.a*_t2)*_c - self.b*_c)
        )
        right = Segment(
            num_dot=self.nD, 
            p1 = ((self.b + self.a*_t2)*_s, (self.b + self.a*_t2)*_c - self.b*_c), 
            p2 = (0, -self.b*_c)
        )
        bottom = Segment(
            num_dot=self.nD, 
            p1 = (0, -self.b*_c), 
            p2 = (-(self.b + self.a*_t2)*_s, (self.b + self.a*_t2)*_c - self.b*_c)
        )
        left = Segment(
            num_dot=self.nD, 
            p1 = (-(self.b + self.a*_t2)*_s, (self.b + self.a*_t2)*_c - self.b*_c), 
            p2 = (0, self.a*_s)
        )

        super().__init__(
            vertices=connect_edges(bottom, left, top, right),
            gem_type=gem_type, 
            **kwargs
        )

    def __len__(self) -> int:
        return 4*(self.nD - 1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.a, self.b, self.nD))
    

class ConcaveStar(Polygon2D):
    def __init__(
        self,
        s:float = None,
        nD:int = None,
        nV:int = None, 
        **kwargs
    ):
        """
        A star polygon without intersecting edges.
        
        Args:
            s | size (float): distance between centroid and sharp corner of the star
            nD | num_dot (int): number of dots consisting of a edge
            nV | num_vertex (int): number of vertex
        """
        gem_type = self.__class__.__name__

        self.uS, self.nD, self.nV = assignArg(
            gem_type, 
            [s, nD, nV], 
            ['size', 'num_dot', 'num_vertex'], 
            kwargs
        )

        if self.nV < 3 :
            raise ValueError("[ERROR] %s should have at least 3 vertices"%(gem_type))

        if self.nD < 2 :
            raise ValueError("[ERROR] %s: each side must have at least 2 dots"%(gem_type))
        
        ang = pi/self.nV
        orD = self.uS * sin(ang) / (cos(2*ang)*cos(ang) + sin(2*ang)*sin(ang))

        coord = self._draw_substar(orD)

        super().__init__(
            vertices=coord,
            gem_type=gem_type, 
            **kwargs
        )
    
    def _draw_substar(self, orD):
        coord = []

        for v in range(self.nV):
            for e in reversed(range(self.nD-1)):
                dx = self.uS - orD*sin(2*pi/self.nV)*e/(self.nD-1)
                dy = -orD*cos(2*pi/self.nV)*e/(self.nD-1)
                
                rx, ry = rotate_2D((dx, dy), v*2*pi/self.nV)
                coord.append([rx, ry])
            for e in range(1, self.nD):
                dx = self.uS - orD*sin(2*pi/self.nV)*e/(self.nD-1)
                dy = orD*cos(2*pi/self.nV)*e/(self.nD-1)
                
                rx, ry = rotate_2D((dx, dy), v*2*pi/self.nV)
                coord.append([rx, ry])

        coord = np.array(coord)

        return coord

    def __len__(self) -> int:
        return self.nV*(2*self.nD-2)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nD, self.nV))