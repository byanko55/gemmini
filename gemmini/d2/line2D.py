from gemmini.misc import *
from gemmini.d2._gem2D import Geometry2D


class Line2D:
    def __init__(
        self,
        p1:Tuple[float, float], 
        p2:Tuple[float, float] = None,
        slope:float = None,
    ) -> None:
        """
        Infinite long straight line.
        Either p2 or slope has to be given.

        Args:
            p1, p2 (tuple): Points for the line to pass through.
            slope (float): The slope of the line.
        """
        if (type(p2) == type(None) and slope == None) or (type(p2) != type(None) and slope != None):
            raise ValueError(" \
                [ERROR] Line2D: Either p2 or slope has to be given. \
            ")
        
        if not isPoint(p1, dim=2) or (type(p2) != type(None) and not isPoint(p2, dim=2)):
            raise ValueError(" \
                [ERROR] Line2D: Input vector does not match the format of 2D point. \
            ")
        
        if slope != None and not isNumber(slope):
            raise ValueError(" \
                [ERROR] Line2D: Tried to assign non-numetic value to `slope`. \
            ")
        
        self.p1 = p1
        self.p2 = p2
        self.slope = slope

    def grad(self) -> float:
        """
        Return the gradient of the line.
        """
        if self.slope != None:
            return self.slope

        if self.p1[0] == self.p2[0]:
            return inf

        return (self.p2[1]-self.p1[1])/(self.p2[0]-self.p1[0])
    
    def parallel(self, other:Any) -> bool:
        """
        True, if two line are parallel.
        """
        if type(other) != Line2D:
            raise ValueError(" \
                [ERROR] parallel: the input is not a `Line2D` object. \
            ")

        return self.grad() == other.grad()
    
    def orthog(self, other:Any) -> bool:
        """
        True, if two line are orthogonal.
        """
        if type(other) != Line2D:
            raise ValueError(" \
                [ERROR] orthognal: the input is not a `Line2D` object. \
            ")

        ga = self.grad()
        gb = other.grad()

        if (ga == inf and gb == 0) or (ga == 0 and gb == inf):
            return True
        
        if ga*gb == -1:
            return True
 
        return False
    
    def orthog_point(self, p:Tuple[float, float]) -> Tuple[float, float]:
        """
        Return 'Foot of a perpendicular', the point where it intersects with 
        a line through the given point `p`, that forms a right angle.

        Args:
            p (tuple): a (x, y) coordinates.
        """
        g = self.grad()

        if g == 0 :
            return p[0], self.p1[1]
        
        if g == inf:
            return self.p1[0], p[1]
        
        x = (p[0]/g + g*self.p1[0] + p[1] - self.p1[1])*g/(g**2 + 1)
        y = g*(x - self.p1[0]) + self.p1[1]

        return x, y
    
    def _intersect_line(self, other:Any) -> Tuple[float, float]:
        if self.parallel(other):
            warnings.warn(" \
                [WARN] intersect: Two line are parallel. \
            ")
            
            return None, None
        
        ga = self.grad()
        gb = other.grad()

        if ga == inf:
            rx = self.p1[0]
            ry = gb*(rx - other.p1[0]) + other.p1[1]
        elif gb == inf:
            rx = other.p1[0]
            ry = ga*(rx - self.p1[0]) + self.p1[1]
        else :
            rx = (ga*self.p1[0] - gb*other.p1[0] - self.p1[1] + other.p1[1])/(ga-gb)
            ry = ga*(rx - self.p1[0]) + self.p1[1]

        return rx, ry
    
    def _intersect_segment(self, other:Any) -> Tuple[float, float]:
        coord = other.coords()
        _l = Line2D(coord[0], coord[-1])

        _x, _y = self._intersect_line(_l)

        if _x == None:
            return None, None
        
        if min(coord[0][0], coord[-1][0]) <= _x \
        and max(coord[0][0], coord[-1][0]) >= _x \
        and min(coord[0][1], coord[-1][1]) <= _y \
        and max(coord[0][1], coord[-1][1]) >= _y:
            return _x, _y

        return None, None
    
    def _intersect_gem(self, other:Any) -> List[Tuple]:
        res = []

        coord = other.coords()
        idx = list(range(len(coord))) + [0]

        for i in range(len(coord)):
            _s = Segment(nD=2, p1=coord[idx[i]], p2=coord[idx[i+1]])
            _x, _y = self._intersect_segment(_s)

            if _x == None:
                continue

            res.append([_x, _y])

        return np.array(res)
    
    def intersect(self, other:Any) -> Tuple[float, float]:
        """
        Return the coordinates of intersection point with another line/geometry.
        """
        if type(self) == type(other):
            return self._intersect_line(other)
        
        if isinstance(other, Geometry2D):
            return self._intersect_gem(other)
        
        raise ValueError(" \
            [ERROR] intersect: the class of input is neither Line2D nor Geometry2D. \
        ")
    
    def on(self, other:Union[Tuple[float, float], Geometry2D]) -> bool:
        """
        Check whether a point or geometry is on the line.

        Args:
            other ((float, float) | Geometry2D]): can be either a (x, y) coordinates or geometric object.
        """
        if isPoint(other):
            return other[1] == self.grad()*(other[0] - self.p1[0]) + self.p1[1]
        
        if not isinstance(other, Geometry2D):
            raise ValueError(" \
                [ERROR] on: Input should be a 2D point or geometric object. \
            ")

        coord = other.coords()
        idx = list(range(len(coord))) + [0]

        for i in range(len(coord)):
            _l = Line2D(coord[idx[i]], coord[idx[i+1]])

            if self.parallel(_l):
                return True

            _x, _y = self._intersect_line(_l)

            if _x == None:
                continue

            if min(coord[idx[i]][0], coord[idx[i+1]][0]) > _x :
                continue

            if max(coord[idx[i]][0], coord[idx[i+1]][0]) < _x:
                continue

            if min(coord[idx[i]][1], coord[idx[i+1]][1]) > _y :
                continue

            if max(coord[idx[i]][1], coord[idx[i+1]][1]) < _y:
                continue

            return True

        return False        

    def __and__(self, other:Any) -> Tuple[float, float]:
        return self.intersect(other)
    
    def __str__(self) -> str:
        return 'Line2D'
    
    def __eq__(self, other:Any) -> bool:
        if not isinstance(other, Line2D):
            return False

        return (self.grad() == other.grad() and other.on(self.p1))

    def __ne__(self, other:Any) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        return hash((self.p1, self.grad()))
    

class Segment(Geometry2D):
    @geminit({'size':'arg1', 's':'arg1', 'p1':'arg1', 'slope':'arg2', 'p2':'arg2', 'num_dot':'n'})
    def __init__(
        self,
        arg1:Union[float, Tuple[int, int]] = None,
        arg2:Union[float, Tuple[int, int]] = None,
        n:int = 16,
        **kwargs
    ) -> None:
        """
        A part of a straight line that is bounded by two distinct end points.
        You can draw it in 2 ways:

            1) by specifying the `length` and `slope` of the line segment.
                ex) Segment(3, size=128, slope=pi/3)
            2) by specifying the `coordinates` of two end-points: 'p1', 'p2'.
                ex) Segment(3, p1 = (8,8), p2 = (10,10))

        Args:
            s | size (int): length of segment.
            slope (float): slope or gradient of a line.
            p1, p2 (float, float): End-points of the line segment.
            n | num_dot (int): number of dots consisting of the line segment.
        """
        self.nD = n

        if isNumber(arg1) and isNumber(arg2):
            self.line_type = 0
            self.uS = arg1
            self.aG = arg2
        elif isPoint(arg1) and isPoint(arg2):
            self.line_type = 1
            self.p1 = arg1
            self.p2 = arg2
        else :
            raise ValueError(" \
                [ERROR] Segment: You can draw it in 2 ways: \
                \
                1) by specifying the `length` and `slope` of the line segment. \
                    ex) Segment(3, size=128, slope=75) \
                2) by specifying the `coordinates` of two end-points: 'p1', 'p2'. \
                    ex) Segment(3, p1 = (8,8), p2 = (10,10)) \
            ")

        super().__init__(
            gem_type=self.gem_type,
            planar=False,
            **kwargs
        )

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
        
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_seq(len(self))], []

    def __len__(self) -> int:
        return self.nD
    
    def __hash__(self) -> int:
        if self.line_type == 0:
            return super().__hash__() + hash((self.gem_type, self.nD, self.aG))
        else :
            return super().__hash__() + hash((self.gem_type, self.p1, self.p2))