from gemmini.misc import *
from gemmini.d2._gem2D import *
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
        gem_type = self.__class__.__name__
        
        self.v = assignArg(gem_type, [v], ['vertices'], kwargs)
        self.v = np.array(self.v)
        
        if len(self.v.shape) != 2 or self.v.shape[1] != 2 :
            raise ValueError(" \
                [ERROR] Polygon2D: check every vertices to conform the 2D format (x, y) \
            ")
        
        super().__init__(gem_type=gem_type, **kwargs)
        
    def _base_coords(self) -> np.ndarray:
        return self.v

    def __len__(self) -> int:
        return len(self.v)
    
def line_segment2D(p1:Tuple[float, float], p2:Tuple[float, float]):
    if not _isPoint(p1, dim=2) or not _isPoint(p2, dim=2):
        raise ValueError(" \
            [ERROR] line_segment2D: check every points to conform the 2D format (x, y) \
        ")
    
    return Polygon2D(vertices=[p1, p2])

class Segment(Geometry2D):
    def __init__(
        self,
        nD:int = None,
        arg1:Union[float, Tuple[int, int]] = None,
        arg2:Union[float, Tuple[int, int]] = None,
        **kwargs
    ):
        """
        A part of a straight line that is bounded by two distinct end points.
        You can draw it in 2 ways:

            1) by specifying the `length` and `slope` of the line segment
                ex) Segment(3, size=128, slope=pi/3)
            2) by specifying the `coordinates` of two end-points: 'p1', 'p2'
                ex) Segment(3, p1 = (8,8), p2 = (10,10))

        Args:
            nD | num_dot (int): number of dots consisting of the line segment
            s | size (int): length of segment
            slope (float): slope or gradient of a line
            p1, p2 (float, float): End-points of the line segment.
        """

        gem_type = self.__class__.__name__

        self.nD, arg1, arg2 = assignArg(
            gem_type, 
            [nD, arg1, arg2], 
            ['num_dot', ['s', 'size', 'p1'], ['slope', 'p2']], 
            kwargs
        )

        if _isNumber(arg1) and _isNumber(arg2):
            self.line_type = 0
            self.uS = arg1
            self.aG = arg2
        elif _isPoint(arg1) and _isPoint(arg2):
            self.line_type = 1
            self.p1 = arg1
            self.p2 = arg2
        else :
            raise ValueError(" \
                [ERROR] %s: You can draw it in 2 ways \
                \
                1) by specifying the `length` and `slope` of the line segment \
                    ex) Segment(3, size=128, slope=75) \
                2) by specifying the `coordinates` of two end-points: 'p1', 'p2' \
                    ex) Segment(3, p1 = (8,8), p2 = (10,10)) \
            "%(gem_type))

        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
        if self.line_type == 0 :
            coord = np.zeros((self.nD, 2))

            d = -self.uS/2 + self.uS*np.arange(self.nD)/(self.nD-1)

            coord[:, 0] = d * cos(self.aG)
            coord[:, 1] = d * sin(self.aG)

            return coord
        else :
            d = np.arange(self.nD)
            coord = np.zeros((self.nD, 2))
            coord[:, 0] = (d * self.p2[0] + (self.nD - d - 1) * self.p1[0])/(self.nD-1)
            coord[:, 1] = (d * self.p2[1] + (self.nD - d - 1) * self.p1[1])/(self.nD-1)

            return coord

    def __len__(self) -> int:
        return self.nD

class RegularPolygon(Geometry2D):
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
        
        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
        coord = np.array([[self._draw_edge(i, self.nD-j-1) for j in range(self.nD-1)] for i in range(self.nV)])
        coord = coord.reshape(-1, coord.shape[-1])

        return coord
    
    def _draw_edge(self, v, e):
        dx = -self.uS/2 + self.uS*e/(self.nD-1)
        dy = -self.uS/(2*tan(pi/self.nV))
        
        rx, ry = rotate_2D((dx, dy), 2*v*pi/self.nV)
        
        return rx, ry

    def __len__(self) -> int:
        return self.nV*(self.nD-1)
    
class Parallelogram(Geometry2D):
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
        
        super().__init__(gem_type=gem_type, **kwargs)
        
    def _base_coords(self) -> np.ndarray:
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
        
        return connect_edges(top, right, bottom, left)
        
    def __len__(self) -> int:
        return 2*(self.nX + self.nY - 2)
    
class Rhombus(Geometry2D):
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

        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
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
        
        return connect_edges(top, right, bottom, left)

    def __len__(self) -> int:
        return 4*(self.nD - 1)

class Trapezoid(Geometry2D):
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

        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
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
        
        return connect_edges(top, right, bottom, left)

    def __len__(self) -> int:
        return self.nbD + self.ntD + 2*self.nsD - 4
    
def RightTrapezoid(
    h:float = None,
    wt:float = None,
    wb:float = None,
    nD:Union[int, Tuple[int, int, int]] = None,
    **kwargs
):
    return Trapezoid(h, wt, wb, nD, (wt-wb)/2, **kwargs)
    
class Rectangle(Geometry2D):
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
            h | height (float): length of vertical diagonals
            w | width (float): length of horizontal diagonals
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

        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
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
        
        return connect_edges(top, right, bottom, left)

    def __len__(self) -> int:
        return 2*(self.nwD + self.nhD - 2)

class Kite(Geometry2D):
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
        
        self.a = a
        self.b = b

        self.nD = assignArg(gem_type, [nD], ['num_dot'], kwargs)

        if self.nD < 2 :
            raise ValueError("[ERROR] %s: each side should consist of at least 2 dots"%(gem_type))

        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
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
        
        return connect_edges(top, right, bottom, left)

    def __len__(self) -> int:
        return 4*(self.nD - 1)
    
class ConcaveStar(Geometry2D):
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

        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
        ang = pi/self.nV
        orD = self.uS * sin(ang) / (cos(2*ang)*cos(ang) + sin(2*ang)*sin(ang))
        irD = self.uS / (cos(ang) + sin(ang)*tan(2*ang))

        coord = self._draw_substar(orD)

        return coord
    
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
    
def connect_edges(*args:Segment) -> np.ndarray:
    coord = args[0][:-1]
    
    for seg in args[1:]:
        coord = np.concatenate((coord, seg[:-1]), axis=0)
    
    return coord