from gemmini.misc import *
from gemmini.d2._gem2D import *
from gemmini.calc.coords import _isNumber, _isPoint, rotate_2D

class Polygon2D(Geometry2D):
    def __init__(
        self,
        vertices:Union[list, np.ndarray],
        **kwargs
    ) -> None:
        """
        A 2D plane figure made up of line segments connected to form a closed polygonal chain.

        Args:
            vertices (Union[list, np.ndarray]): set of polygon's vertices (or corners).
        """
        self.vertices = np.array(vertices)
        
        if len(self.vertices.shape) != 2 or self.vertices.shape[1] != 2 :
            raise ValueError(" \
                [ERROR] Polygon2D: check every vertices to conform the 2D format (x, y) \
            ")
        
        super().__init__(gem_type="Polygon2D", **kwargs)
        
    def _base_coords(self) -> np.ndarray:
        return self.vertices

    def __len__(self) -> int:
        return len(self.vertices)
    
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
                ex) Segment(3, size=128, slope=75)
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

            coord[:, 0] = d * cos(pi*self.aG/180)
            coord[:, 1] = d * sin(pi*self.aG/180)

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
        dy = self.uS/(2*tan(pi/self.nV))
        
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
            a | angle (float): interior angle (unit: degrees, °)
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
    
        if self.aG <= 0 or self.aG >= 180:
            raise ValueError("[ERROR] %s: interior angle should be in range (0, 180)"%(gem_type))
        
        super().__init__(gem_type=gem_type, **kwargs)
        
    def _base_coords(self) -> np.ndarray:
        coord = []
        
        for i in range(self.nX):
            fig = Segment(
                num_dot=self.nY, 
                size=self.h/sin(self.aG), 
                slope=180*self.aG/pi
            )

            fig.translate(mx = int(-self.w/2 + i*self.w/(self.nX-1)))
            
            if 0 < i and i < self.nX - 1:
                idx = [0, self.nY-1]
                coord += fig[idx]
            else :
                coord += fig[:]
        
        coord = np.array(coord)

        return coord
        
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
        coord = []
        
        for i in range(2*self.nD - 1):
            x = -self.w/2 + i*self.w/(2*self.nD-2)
            y = (self.nD - 1 - abs(self.nD-1-i))/(self.nD-1) * self.h/2
            
            if i == 0:
                coord.insert(0, [x, 0])
            elif i == 2*(self.nD-1):
                coord.insert(-1, [x, 0])
            else :
                coord.insert(0, [x, y])
                coord.insert(-1, [x, -y])
        
        return np.array(coord)

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
            p1 = (-self.wt/2 + self.translate_top, -self.h/2), 
            p2 = (self.wt/2 + self.translate_top, -self.h/2)
        )
        bottom = Segment(
            num_dot=self.nbD, 
            p1 = (self.wb/2, self.h/2), 
            p2 = (-self.wb/2, self.h/2)
        )
        left = Segment(
            num_dot=self.nsD, 
            p1 = (-self.wb/2, self.h/2), 
            p2 = (-self.wt/2 + self.translate_top, -self.h/2)
        )
        right = Segment(
            num_dot=self.nsD, 
            p1 = (self.wt/2 + self.translate_top, -self.h/2), 
            p2 = (self.wb/2, self.h/2)
        )

        coord_top = top[:]
        coord_bottom = bottom[:]
        coord_left = left[:]
        coord_right = right[:]

        coord = np.concatenate(
            (
                coord_top[:-1], 
                coord_right[:-1], 
                coord_bottom[:-1], 
                coord_left[:-1]
            ),
            axis=0
        )
        
        coord, idxs = np.unique(coord, axis=0, return_index=True)
        coord = coord[idxs.argsort()]

        return coord

    def __len__(self) -> int:
        return self.nbD + self.ntD + 2*self.nsD - 4
    
def RightTrapezoid(
    h:float = None,
    wt:float = None,
    wb:float = None,
    nD:Union[int, Tuple[int, int, int]] = None,
    **kwargs
):
    return Trapezoid(h, wt, wb, nD, (wt-wb)/2, kwargs)
    
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
        x = np.linspace(-self.w/2, self.w/2, self.nwD)
        y = np.linspace(-self.h/2, self.h/2, self.nhD)
        xv, yv = np.meshgrid(x, y)

        coord = np.array((xv, yv))
        coord = np.transpose(coord.reshape(2, -1))

        border = np.where(
            (coord[:, 0] == np.min(xv)) |
            (coord[:, 0] == np.max(xv)) | 
            (coord[:, 1] == np.min(yv)) | 
            (coord[:, 1] == np.max(yv))
        )

        coord = coord[border]

        return coord

    def __len__(self) -> int:
        return 2*(self.nwD + self.nhD - 2)

class Kite(Geometry2D):
    def __init__(
        self,
        h:float = None,
        w:float = None,
        nY:int = None,
        nX:int = None,
        **kwargs
    ):
        """
        A quadrilateral with reflection symmetry across a diagonal.

        Args:
            h | height (float): length of vertical diagonals
            w | width (float): length of horizontal diagonals
            nD | num_dot (int): number of dots consisting of a edge
        """
        
        gem_type = self.__class__.__name__

        self.h, self.w, self.nY, self.nX = assignArg(
            gem_type, 
            [h, w, nY, nX], 
            ['height', 'width', 'num_ydot', 'num_xdot'], 
            kwargs
        )

        if self.nX < 2 or self.nY < 2 :
            raise ValueError("[ERROR] %s: each side should consist of at least 2 dots"%(gem_type))

        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
        pass

    def __len__(self) -> int:
        return 2*(self.nX + self.nY - 1)
    
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

        coord_ss = self._draw_substar(orD)
        coord_ip = self._draw_polygon(irD, 2)

        coord = np.concatenate((coord_ss, coord_ip), axis=0)

        return coord
    
    def _draw_substar(self, orD):
        coord = []

        for v in range(self.nV):
            for e in reversed(range(self.nD-1)):
                dx = self.uS - orD*sin(2*pi/self.nV)*e/(self.nD-1)
                dy = -orD*cos(2*pi/self.nV)*e/(self.nD-1)
                
                rx, ry = rotate_2D(dx, dy, v*2*pi/self.nV)
                coord.append([rx, ry])
            for e in range(1, self.nD-1):
                dx = self.uS - orD*sin(2*pi/self.nV)*e/(self.nD-1)
                dy = orD*cos(2*pi/self.nV)*e/(self.nD-1)
                
                rx, ry = rotate_2D(dx, dy, v*2*pi/self.nV)
                coord.append([rx, ry])

        coord = np.array(coord)

        return coord

    def _draw_polygon(self, irD, inD):
        fig = RegularPolygon(size=irD, num_vertex=self.nV, num_dot=inD)
        fig.rotate(180/self.nV)

        return fig.get_subcoord()

    def __len__(self) -> int:
        return self.nV*(2*self.nD-2)