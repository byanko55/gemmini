from gemmini.misc import *
from gemmini.d2._gem2D import Geometry2D
from gemmini.d2.line2D import Segment
from gemmini.calc.geometry import connect_edges
from gemmini.calc.coords import isNumber, isPoint, rotate_2D


class Polygon2D(Geometry2D):
    def __init__(
        self,
        vertices:Union[list, np.ndarray],
        **kwargs
    ) -> None:
        """
        A 2D plane figure made up of line segments connected to form a closed polygonal chain.

        Args:
            vertices (list | np.ndarray): set of polygon's vertices (or corners).
        """
        if not hasattr(self, 'gem_type'):
            self.gem_type = 'Polygon2D'
        
        self.v = vertices
        
        super().__init__(
            planar=True,
            **kwargs
        )
        
    def _base_coords(self) -> np.ndarray:
        return self.v
    
    def _linear_paths(self) -> Tuple[list, list]:
        return [linear_ring(len(self.v))], []

    def __len__(self) -> int:
        return NotImplementedError
    
    def __hash__(self) -> int:
        return super().__hash__()
    

def line_segment2D(p1:Tuple[float, float], p2:Tuple[float, float]) -> Polygon2D:
    """
    A one-dimensional line segment joining two vertices.
    
    Args:
        p1, p2 (float, float): coordinates of two vertices.
    """
    if not isPoint(p1, dim=2) or not isPoint(p2, dim=2):
        raise ValueError(" \
            [ERROR] line_segment2D: Input vector does not match the format of 2D point. \
        ")
    
    return Polygon2D(vertices=[p1, p2])


class RegularPolygon(Polygon2D):
    @geminit({'size':'s', 'num_vertex':'v', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        v:int = None,
        n:int = 8,
        **kwargs
    ) -> None:
        """
        A polygon whose angles are all equal, and all sides have the same length.

        Args:
            s | size (float): side length of the polygon.
            v | num_vertex (int): number of vertex.
            n | num_dot (int): number of dots consisting of a edge.
        """
        self.uS, self.nV, self.nD = s, v, n

        if self.nV < 3 :
            raise ValueError(" \
                [ERROR] RegularPolygon: Requires at least 3 vertices. \
            ")

        if self.nD < 2 :
            raise ValueError(" \
                [ERROR] RegularPolygon: Each side must have at least 2 dots. \
            ")
        
        coord = np.array([
            [self._draw_edge(i, self.nD-j-1) for j in reversed(range(self.nD-1))] for i in range(self.nV)
        ])

        coord = coord.reshape(-1, coord.shape[-1])
        
        super().__init__(
            vertices=coord,
            **kwargs
        )
    
    def _draw_edge(self, v, e) -> Tuple[float, float]:
        dx = -self.uS/2 + self.uS*e/(self.nD-1)
        dy = -self.uS/(2*tan(pi/self.nV))
        
        rx, ry = rotate_2D((dx, dy), 2*v*pi/self.nV)
        
        return rx, ry

    def __len__(self) -> int:
        return self.nV*(self.nD-1)
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.uS, self.nV, self.nD))
    
    
class IsoscelesTriangle(Polygon2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:Union[int, Tuple[int, int, int]] = 27,
        **kwargs
    ) -> None:
        """
        A triangle that has two sides of equal length.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of triangle.
            w | width (float): base length of the triangle.
            n | num_dot (int | tuple): number of dots consisting of each edge.
                If a numeric value is given, then the triangle includes `n` dots on its circumference.
                Or, you can determine the number of dots on each sides respectively,
                by giving a tuple for the `num_dot` argument. 
                ex) num_dot = (8,9,12): #dots on left leg=8, #dots on right leg=9, #dots on base=12
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] IsoscelesTriangle: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        if isNumber(n):
            _s = self.w + 2*sqrt(self.h**2 + (self.w/2)**2)
            _nD = n + 3
            nD_l = int(_nD * sqrt(self.h**2 + (self.w/2)**2)/_s)
            self.nD = [nD_l, nD_l, _nD - 2*nD_l]
            
        if not isNumberArray(self.nD) or len(self.nD) != 3:
            raise ValueError(" \
                [ERROR] IsoscelesTriangle: Invalid data type for the argument `num_dot`. \
                Make sure it is either an integer or a tuple with 3 numeric elements. \
            ")
            
        if min(self.nD) < 2:
            raise ValueError(" \
                [ERROR] IsoscelesTriangle: Each side should consist of at least 2 dots. \
            ")
        
        right = Segment(
            num_dot=self.nD[1], 
            p1 = (self.w/2, -self.h/3), 
            p2 = (0, 2*self.h/3)
        )
        left = Segment(
            num_dot=self.nD[0], 
            p1 = (0, 2*self.h/3), 
            p2 = (-self.w/2, -self.h/3),
        )
        base = Segment(
            num_dot=self.nD[2], 
            p1 = (-self.w/2, -self.h/3), 
            p2 = (self.w/2, -self.h/3)
        )
        
        super().__init__(
            vertices=connect_edges(right, left, base),
            **kwargs
        )
        
    def __len__(self) -> int:
        return sum(self.nD) - 3
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, tuple(self.nD)))
        

class RightTriangle(Polygon2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:Union[int, Tuple[int, int, int]] = 27,
        **kwargs
    ) -> None:
        """
        A triangle that has one of its interior angles measuring 90°.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of triangle.
            w | width (float): base length of the triangle.
            n | num_dot (int | tuple): number of dots consisting of each edge.
                If a numeric value is given, then the triangle includes `n` dots on its circumference.
                Or, you can determine the number of dots on each sides respectively,
                by giving a tuple for the `num_dot` argument. 
                ex) num_dot = (8,9,12): #dots on vertical leg=8, #dots on hypotenuse=9, #dots on base=12
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] RightTriangle: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        if isNumber(n):
            _s = self.w + self.h + sqrt(self.h**2 + self.w**2)
            _nD = n + 3
            nD_v = int(_nD * self.h/_s)
            nD_h = int(_nD * self.w/_s)
            self.nD = [nD_v, _nD - nD_v - nD_h, nD_h]
            
        if not isNumberArray(self.nD) or len(self.nD) != 3:
            raise(" \
                [ERROR] RightTriangle: Invalid data type for the argument `num_dot`. \
                Make sure it is either an integer or a tuple with 3 numeric elements. \
            ")
            
        if min(self.nD) < 2:
            raise ValueError(" \
                [ERROR] RightTriangle: Each side should consist of at least 2 dots. \
            ")
        
        right = Segment(
            num_dot=self.nD[1], 
            p1 = (2*self.w/3, -self.h/3), 
            p2 = (-self.w/3, 2*self.h/3),
        )
        left = Segment(
            num_dot=self.nD[0], 
            p1 = (-self.w/3, 2*self.h/3), 
            p2 = (-self.w/3, -self.h/3)
        )
        base = Segment(
            num_dot=self.nD[2], 
            p1 = (-self.w/3, -self.h/3), 
            p2 = (2*self.w/3, -self.h/3)
        )
        
        super().__init__(
            vertices=connect_edges(right, left, base),
            **kwargs
        )
        
    def __len__(self) -> int:
        return sum(self.nD) - 3
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, tuple(self.nD)))


class Parallelogram(Polygon2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n', 'angle':'a'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:Union[int, Tuple[int, int, int, int]] = 32,
        a:float = pi/3,
        **kwargs
    ) -> None:
        """
        A quadrilateral which is made up of 2 pairs of parallel sides.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): height of the geometry.
            w | width (float): length of base (horizontal edge).
            n | num_dot (int | tuple): number of dots consisting of each side.
                If a numeric value is given, then the geometry includes `n` dots on its circumference.
                Or, you can determine the number of dots on each sides respectively,
                by giving a tuple for the `num_dot` argument.
                ex) num_dot = (7,8,9,10): #dots on top/right/bottom/left side = 7/8/9/10
            a | angle (float): one of the adjacent angle (unit: radian) of the parallelogram.
        """
        self.h, self.w, self.nD, self.aG = h, w, n, a
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Parallelogram: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        if self.aG <= 0 or self.aG >= pi:
            raise ValueError(" \
                [ERROR] Parallelogram: The argument `angle` must be in range (0, π). \
            ")
        
        if isNumber(n):
            _s = 2*self.w + 2*self.h/sin(a)
            _nD = n + 4
            nD_tb = int(_nD * self.w/_s)
            nD_lr = int(_nD * (self.h/sin(self.aG))/_s)
            self.nD = [nD_tb, nD_lr, nD_tb, _nD - 2*nD_tb - nD_lr]
            
        if not isNumberArray(self.nD) or len(self.nD) != 4:
            raise ValueError(" \
                [ERROR] Parallelogram: Invalid data type for the argument `num_dot`. \
                Make sure it is either an integer or a tuple with 4 numeric elements. \
            ")
        
        if min(self.nD) < 2:
            raise ValueError(" \
                [ERROR] Parallelogram: Each side should consist of at least 2 dots. \
            ")
        
        top = Segment(
            num_dot=self.nD[0], 
            p1 = ((-self.w + self.h*cos(self.aG))/2, self.h*sin(self.aG)/2), 
            p2 = ((self.w + self.h*cos(self.aG))/2, self.h*sin(self.aG)/2)
        )
        right = Segment(
            num_dot=self.nD[1],
            p1 = ((self.w + self.h*cos(self.aG))/2, self.h*sin(self.aG)/2), 
            p2 = ((self.w - self.h*cos(self.aG))/2, -self.h*sin(self.aG)/2)
        )
        bottom = Segment(
            num_dot=self.nD[2],
            p1 = ((self.w - self.h*cos(self.aG))/2, -self.h*sin(self.aG)/2), 
            p2 = ((-self.w - self.h*cos(self.aG))/2, -self.h*sin(self.aG)/2)
        )
        left = Segment(
            num_dot=self.nD[3],
            p1 = ((-self.w - self.h*cos(self.aG))/2, -self.h*sin(self.aG)/2), 
            p2 = ((-self.w + self.h*cos(self.aG))/2, self.h*sin(self.aG)/2)
        )
        
        super().__init__(
            vertices=connect_edges(top, right, bottom, left),
            **kwargs
        )
        
    def __len__(self) -> int:
        return sum(self.nD)-4
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, tuple(self.nD), self.aG))
    
    
class Rhombus(Polygon2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:Union[int, Tuple[int, int, int, int]] = 32,
        **kwargs
    ) -> None:
        """
        A quadrilateral whose four sides all have the same length.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): length of vertical diagonals.
            w | width (float): length of horizontal diagonals.
            n | num_dot (int | tuple): number of dots consisting of each side.
                If a numeric value is given, then the geometry includes `n` dots on its circumference.
                Or, you can determine the number of dots on each sides respectively,
                by giving a tuple for the `num_dot` argument.
                ex) num_dot = (7,8,9,10): (top_right=7, bottom_right=8, bottom_left=9, top_left=10)
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Rhombus: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]

        if isNumber(n):
            _nD = n + 4
            nD_e = int(_nD/4)
            self.nD = [nD_e, nD_e, nD_e, _nD - 3*nD_e]
            
        if not isNumberArray(self.nD) or len(self.nD) != 4:
            raise ValueError(" \
                [ERROR] Rhombus: Invalid data type for the argument `num_dot`. \
                Make sure it is either an integer or a tuple with 4 numeric elements. \
            ")
        
        if min(self.nD) < 2:
            raise ValueError(" \
                [ERROR] Rhombus: Each side should consist of at least 2 dots. \
            ")
        
        top = Segment(
            num_dot=self.nD[0], 
            p1 = (0, self.h/2), 
            p2 = (self.w/2, 0)
        )
        right = Segment(
            num_dot=self.nD[1], 
            p1 = (self.w/2, 0), 
            p2 = (0, -self.h/2)
        )
        bottom = Segment(
            num_dot=self.nD[2], 
            p1 = (0, -self.h/2), 
            p2 = (-self.w/2, 0)
        )
        left = Segment(
            num_dot=self.nD[3], 
            p1 = (-self.w/2, 0), 
            p2 = (0, self.h/2)
        )

        super().__init__(
            vertices=connect_edges(top, right, bottom, left),
            **kwargs
        )

    def __len__(self) -> int:
        return sum(self.nD)-4
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, tuple(self.nD)))
    

class Trapezoid(Polygon2D):
    @geminit({'size':'s', 'num_dot':'n'})
    def __init__(
        self,
        s:List[float] = None,
        n:Union[int, Tuple[int, int, int, int]] = 32,
        **kwargs
    ) -> None:
        """
        A quadrilateral that has at least one pair of parallel sides.
        
        Args:
            s | size (list | tuple): specify the length of each side.
                ex) size = (8, 6): height=8, width=6 (Indeed, the result is `Rectangle`)
                ex) size = (8, 6, 10): height=8, length of top side=6, length of bottom side=10
                ex) size = (5, 6, 7, 8): length of top=5, right=6, bottom=7, left=8, respectively 
            n | num_dot (int | tuple): number of dots consisting of each side.
                If a numeric value is given, then the geometry includes `n` dots on its circumference.
                Or, you can determine the number of dots on each sides respectively,
                by giving a tuple for the `num_dot` argument.
                ex) num_dot = (7,8,9,10): #dots on top/right/bottom/left side = 7/8/9/10
        """
        self.s, self.nD = s, n

        if not isNumberArray(s) or len(s) < 2 or len(s) > 4:
            raise(" \
                [ERROR] Trapezoid: Invaild input type is given for the argument `size`. \
            ")
        
        if len(s) == 2:
            self.s = [s[1], s[0], s[1], s[0]]
        
        if len(s) == 3:
            l_v = sqrt(((s[2]-s[1])/2)**2 + s[0]**2)
            self.s = [s[1], l_v, s[2], l_v]

        if abs(self.s[1] - self.s[3]) > abs(self.s[0] - self.s[2]) \
        or abs(self.s[0] - self.s[2]) >= self.s[1] + self.s[3] :
            raise(" \
                [ERROR] Trapezoid: Given four lengths can't constitute \
                the consecutive sides of trapezoid. \
            ")

        if isNumber(n):
            _s = sum(self.s)
            _nD = n + 4
            nD_t = int(_nD*self.s[0]/_s)
            nD_r = int(_nD*self.s[1]/_s)
            nD_b = int(_nD*self.s[2]/_s)
            self.nD = [nD_t, nD_r, nD_b, _nD - (nD_t + nD_r + nD_b)]
            
        if not isNumberArray(self.nD) or len(self.nD) != 4:
            raise ValueError(" \
                [ERROR] Trapezoid: Invalid data type for the argument `num_dot`. \
                Make sure it is either an integer or a tuple with 4 numeric elements. \
            ")
        
        if min(self.nD) < 2:
            raise ValueError(" \
                [ERROR] Trapezoid: Each side should consist of at least 2 dots. \
            ")

        l = (self.s[1])**2 - (self.s[3])**2 + (self.s[2])**2 - (self.s[0])**2
        x = abs(l/(2*(self.s[0] + self.s[2])))

        y = sqrt((self.s[1])**2 - x**2)

        top = Segment(
            num_dot=self.nD[0], 
            p1 = (-self.s[0], 0), 
            p2 = (0, 0)
        )
        right = Segment(
            num_dot=self.nD[1], 
            p1 = (0, 0), 
            p2 = (x, -y)
        )
        bottom = Segment(
            num_dot=self.nD[2], 
            p1 = (x, -y), 
            p2 = (x-self.s[2], -y)
        )
        left = Segment(
            num_dot=self.nD[3], 
            p1 = (x-self.s[2], -y), 
            p2 = (-self.s[0], 0)
        )

        coord = connect_edges(top, right, bottom, left)
        coord[:, 0] -= (2*x - self.s[0] - self.s[2])/4
        coord[:, 1] -= (-y/2)

        super().__init__(
            vertices=coord,
            **kwargs
        )

    def __len__(self) -> int:
        return sum(self.nD) - 4
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, tuple(self.s), tuple(self.nD)))
    

@alias({'size':'s', 'num_dot':'n'})
def RightTrapezoid(
    s:Tuple[float, float, float] = None,
    n:Union[int, Tuple[int, int, int, int]] = 32,
    **kwargs
) -> Trapezoid:
    """
    A right trapezoid has two adjacent right angles.

    Args:
        s | size (tuple): specify the length of each side.
            ex) size = (8, 6, 10): height=8, length of top side=6, length of bottom side=10
        n | num_dot (int | tuple): number of dots consisting of each side.
            If a numeric value is given, then the geometry includes `n` dots on its circumference.
            Or, you can determine the number of dots on each sides respectively,
            by giving a tuple for the `num_dot` argument.
            ex) num_dot = (7,8,9,10): #dots on top/right/bottom/left side = 7/8/9/10
    """
    if not isNumberArray(s) or len(s) != 3:
        raise(" \
            [ERROR] RightTrapezoid: Invaild input type is given for the argument `size`. \
        ")
    
    s = [s[1], sqrt(abs(s[1]-s[2])**2 + s[0]**2), s[2], s[0]]

    return Trapezoid(s, n, **kwargs)
    

class Rectangle(Polygon2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:Union[int, Tuple[int, int, int, int]] = 32,
        **kwargs
    ) -> None:
        """
        A four-sided polygon with four right angles.
        
        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): length of vertical sides.
            w | width (float): length of horizontal sides.
            n | num_dot (int | tuple): number of dots consisting of each side.
                If a numeric value is given, then the geometry includes `n` dots on its circumference.
                Or, you can determine the number of dots on each sides respectively,
                by giving a tuple for the `num_dot` argument.
                ex) num_dot = (7,8,9,10): #dots on top/right/bottom/left side = 7/8/9/10
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Rectangle: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]

        if isNumber(n):
            _s = 2*self.w + 2*self.h
            _nD = n + 4
            nD_tb = int(_nD * self.w/_s)
            nD_lr = int(_nD * self.h/_s)
            self.nD = [nD_tb, nD_lr, nD_tb, _nD - 2*nD_tb - nD_lr]
            
        if not isNumberArray(self.nD) or len(self.nD) != 4:
            raise ValueError(" \
                [ERROR] Rectangle: Invalid data type for the argument `num_dot`. \
                Make sure it is either an integer or a tuple with 4 numeric elements. \
            ")
        
        if min(self.nD) < 2:
            raise ValueError(" \
                [ERROR] Rectangle: Each side should consist of at least 2 dots. \
            ")

        top = Segment(
            num_dot=self.nD[0], 
            p1 = (-self.w/2, self.h/2), 
            p2 = (self.w/2, self.h/2)
        )
        right = Segment(
            num_dot=self.nD[1], 
            p1 = (self.w/2, self.h/2), 
            p2 = (self.w/2, -self.h/2)
        )
        bottom = Segment(
            num_dot=self.nD[2], 
            p1 = (self.w/2, -self.h/2), 
            p2 = (-self.w/2, -self.h/2)
        )
        left = Segment(
            num_dot=self.nD[3], 
            p1 = (-self.w/2, -self.h/2), 
            p2 = (-self.w/2, self.h/2)
        )

        super().__init__(
            vertices=connect_edges(top, right, bottom, left),
            **kwargs
        )

    def __len__(self) -> int:
        return sum(self.nD) - 4
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.h, self.w, tuple(self.nD)))


class Kite(Polygon2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:Union[int, Tuple[int, int, int, int]] = 32,
        **kwargs
    ) -> None:
        """
        A quadrilateral with reflection symmetry across a diagonal.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): length of vertical sides.
            w | width (float): length of horizontal sides.
            n | num_dot (int | tuple): number of dots consisting of each side.
                If a numeric value is given, then the geometry includes `n` dots on its circumference.
                Or, you can determine the number of dots on each sides respectively,
                by giving a tuple for the `num_dot` argument.
                ex) num_dot = (7,8,9,10): (top_right=7, bottom_right=8, bottom_left=9, top_left=10)
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] Kite: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
            
        if self.h <= self.w :
            raise ValueError(" \
                [ERROR] Kite: The width of Kite can't be larger than its height. \
            ")
            
        _c = sqrt(1 - (self.w**2)/(self.h**2))
        self.a = self.h * sqrt(2*(1 - _c))/2
        self.b = self.w/(sqrt(2 * (1 - _c)))

        if isNumber(n):
            _s = 2*(self.a+self.b)
            _nD = n + 4
            nD_t = int(_nD*self.a/_s)
            nD_b = int(_nD*self.b/_s)
            self.nD = [nD_t, nD_b, nD_b, _nD - 2*nD_b - nD_t]
            
        if not isNumberArray(self.nD) or len(self.nD) != 4:
            raise ValueError(" \
                [ERROR] Kite: Invalid data type for the argument `num_dot`. \
                Make sure it is either an integer or a tuple with 4 numeric elements. \
            ")
        
        if min(self.nD) < 2:
            raise ValueError(" \
                [ERROR] Kite: Each side should consist of at least 2 dots. \
            ")
        
        _a = self.a/sqrt(self.a*self.a + self.b*self.b) # sin θ
        _b = self.b/sqrt(self.a*self.a + self.b*self.b) # cos θ
        _r = self.a*self.b/(self.a + self.b) # radius of inner circle

        top = Segment(
            num_dot=self.nD[0], 
            p1 = (0, self.a*_a + self.b*_b), 
            p2 = (self.a*_b, self.b*_b)
        )
        right = Segment(
            num_dot=self.nD[1], 
            p1 = (self.a*_b, self.b*_b), 
            p2 = (0, 0)
        )
        bottom = Segment(
            num_dot=self.nD[2], 
            p1 = (0, 0), 
            p2 = (-self.a*_b, self.b*_b)
        )
        left = Segment(
            num_dot=self.nD[3], 
            p1 = (-self.a*_b, self.b*_b), 
            p2 = (0, self.a*_a + self.b*_b)
        )

        coord = connect_edges(bottom, left, top, right)
        coord[:, 1] -= _r/_a

        super().__init__(
            vertices=coord,
            **kwargs
        )

    def __len__(self) -> int:
        return sum(self.nD) - 4
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.a, self.b, tuple(self.nD)))
    
    
class ConcaveKite(Polygon2D):
    @geminit({'size':'s', 'height':'h', 'width':'w', 'num_dot':'n'})
    def __init__(
        self,
        s:Union[float, Tuple[float, float]] = -1,
        h:float = -1,
        w:float = -1,
        n:Union[int, Tuple[int, int, int, int]] = 32,
        **kwargs
    ) -> None:
        """
        A Kite shape, but the line through one of the diagonals bisects the other.

        Args:
            s | size (float | tuple): scale of the geometry.
                Passing a single number makes both the height/width be fixed as `s`,
                while an input like a pair (h, w) generates a geometry with height=`h` and width=`w`. 
                Alternatively, you can utilize keyword `h` and `w`, to specify the height/width.
            h | height (float): length of vertical sides.
            w | width (float): length of horizontal sides.
            n | num_dot (int | tuple): number of dots consisting of each side.
                If a numeric value is given, then the geometry includes `n` dots on its circumference.
                Or, you can determine the number of dots on each sides respectively,
                by giving a tuple for the `num_dot` argument.
                ex) num_dot = (7,8,9,10): (top_right=7, bottom_right=8, bottom_left=9, top_left=10)
        """
        self.h, self.w, self.nD = h, w, n
        
        if isNumber(s) and s != -1:
            self.h, self.w = map(int, [s]*2)
            
        if isNumberArray(s):
            if len(s) != 2:
                raise(" \
                    [ERROR] ConcaveKite: Argument `size` must be either a single number \
                    or a pair of numbers. \
                ")
                
            self.h, self.w = s[0], s[1]
        
        if self.h <= self.w :
            raise ValueError(" \
                [ERROR] ConcaveKite: The width of Kite can't be larger than its height. \
            ")
            
        _c = 2*self.h/sqrt(self.w**2 + 4*self.h**2)
        _s = sqrt(1 - _c**2)
        self.a = self.h*_s/(_c**2)
        self.b = self.h/_c

        if isNumber(n):
            _s = 2*(self.a+self.b)
            _nD = n + 4
            nD_t = int(_nD*self.a/_s)
            nD_b = int(_nD*self.b/_s)
            self.nD = [nD_t, nD_b, nD_b, _nD - 2*nD_b - nD_t]
            
        if not isNumberArray(self.nD) or len(self.nD) != 4:
            raise ValueError(" \
                [ERROR] Kite: Invalid data type for the argument `num_dot`. \
                Make sure it is either an integer or a tuple with 4 numeric elements. \
            ")
        
        if min(self.nD) < 2:
            raise ValueError(" \
                [ERROR] Kite: Each side should consist of at least 2 dots. \
            ")
        
        _a = self.a/sqrt(self.a*self.a + self.b*self.b) # sin θ
        _b = self.b/sqrt(self.a*self.a + self.b*self.b) # cos θ
        _r = self.a*self.b/(self.a + self.b) # radius of inner circle

        top = Segment(
            num_dot=self.nD[0], 
            p1 = (0, -self.a*_a + self.b*_b), 
            p2 = (self.a*_b, self.b*_b)
        )
        right = Segment(
            num_dot=self.nD[1], 
            p1 = (self.a*_b, self.b*_b), 
            p2 = (0, 0)
        )
        bottom = Segment(
            num_dot=self.nD[2], 
            p1 = (0, 0), 
            p2 = (-self.a*_b, self.b*_b)
        )
        left = Segment(
            num_dot=self.nD[3], 
            p1 = (-self.a*_b, self.b*_b), 
            p2 = (0, -self.a*_a + self.b*_b)
        )

        coord = connect_edges(bottom, left, top, right)
        coord[:, 1] -= 2*_r*_b

        super().__init__(
            vertices=coord,
            **kwargs
        )

    def __len__(self) -> int:
        return sum(self.nD) - 4
    
    def __hash__(self) -> int:
        return super().__hash__() + hash((self.gem_type, self.a, self.b, tuple(self.nD)))
    

class ConcaveStar(Polygon2D):
    @geminit({'size':'s', 'num_vertex':'v', 'num_dot':'n'})
    def __init__(
        self,
        s:float = None,
        v:int = 5, 
        n:int = 8,
        **kwargs
    ) -> None:
        """
        A star polygon without intersecting edges.
        
        Args:
            s | size (float): distance between centroid and sharp corner of the star.
            v | num_vertex (int): number of vertex.
            n | num_dot (int): number of dots consisting of a edge.
        """
        self.uS, self.nV, self.nD = s, v, n

        if self.nV < 3 :
            raise ValueError(" \
                [ERROR] ConcaveStar: Requires at least 3 vertices. \
            ")

        if self.nD < 2 :
            raise ValueError(" \
                [ERROR] ConcaveStar: Each side must have at least 2 dots. \
            ")

        ang = 2*pi/self.nV
        _s = sin(ang/2)
        _t = tan(ang)
        _c = cos(ang/2)
        irD = self.uS/(_s*_t + _c)
        
        coord = []
        
        for i in range(self.nV):
            left = Segment((irD*_s, irD*_c), (0, self.uS), self.nD)
            right = Segment((0, self.uS), (-irD*_s, irD*_c), self.nD)
            
            _coord = np.concatenate((left[:-1], right[:-1]), axis = 0)
            _coord = rotate_2D(_coord, i*ang)
            
            coord.append(_coord)

        coord = np.concatenate(tuple(coord), axis=0)

        super().__init__(
            vertices=coord,
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