from gemmini.misc import *
from gemmini.canvas import Canvas
from gemmini.d2.line2D import Line2D
from gemmini.d2.point2D import Point2D, Grid
from gemmini.d2.polar2D import Circle, Ellipse
from gemmini.d2.polygon2D import RegularPolygon

if __name__ == "__main__":
    canva = Canvas()
    
    a = Line2D((10,0), (0,15))
    b = Grid(10, 8, num_dot=(10, 8))
    c = Point2D(px=-6, py=9)
    
    canva.add(a)
    canva.add(b)
    canva.add(c)
    canva.plot()
    
    canva = Canvas(scale=2, minor_ticks=False)
    
    a = Line2D((10,0), (0,15))
    b = Line2D((-1,-1), (5,2))
    c = RegularPolygon(6, 10, nV=5)
    c.translate(4, 8)
    
    canva.add(a, marker_color='orange')
    canva.add(b, dot_style='--')
    canva.add(c, dot_style='*')
    canva.plot()
    
    canva.remove(a)
    canva.plot()
    
    canva = Canvas(draw_grid=False)
    
    a = Circle(r=3, nD=64)
    b = Ellipse(4, 8, 48)
    a.translate(-6, -4)
    
    canva.add(a)
    canva.add(b)
    canva.plot()