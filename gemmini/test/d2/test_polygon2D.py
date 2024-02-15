from gemmini.misc import *
from gemmini.plot import *
from gemmini.d2.polygon2D import *

if __name__ == "__main__":
    f = Polygon2D([[0,0], [3,0], [3,3], [2,1]])
    print("Figure: Polygon2D")
    plot(f)
    
    f = line_segment2D(p1=[-1,2], p2=[3,4])
    print("Figure: Line Segment2D")
    plot(f)

    f = Segment(25, 6, pi/3)
    print("Figure: Segment")
    plot(f)

    f = Segment(25, [1,4], [7,3])
    print("Figure: Segment")
    plot(f)

    f = RegularPolygon(6, 10, nV=5)
    print("Figure: RegularPolygon")
    plot(f)

    f = Parallelogram(h=5, w=8, nY=10, nX=16, a=pi/3)
    print("Figure: Parallelogram")
    plot(f)

    f = Rhombus(h=12, w=20, nD=16)
    print("Figure: Rhombus", len(f))
    plot(f)

    f = Trapezoid(h=12, wt=15, wb=25, nD=8)
    print("Figure: Trapezoid")
    plot(f)

    f = Trapezoid(h=12, wt=15, wb=25, nD=[15, 25, 12], opt=3)
    print("Figure: Trapezoid")
    plot(f)

    f = RightTrapezoid(h=12, wt=15, wb=25, nD=[15, 25, 12])
    print("Figure: RightTrapezoid")
    plot(f)

    f = Rectangle(h=8, w=6, nD=16)
    print("Figure: Rectangle")
    plot(f)

    f = Rectangle(h=8, w=6, nD=[16, 12])
    print("Figure: Rectangle")
    plot(f)

    f = Kite(10, 20, 15)
    print("Figure: Kite")
    plot(f)

    f = ConcaveStar(s=25, nD=7, nV=5)
    print("Figure: ConcaveStar")
    plot(f)