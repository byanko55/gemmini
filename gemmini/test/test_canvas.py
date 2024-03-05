from gemmini.misc import *
from gemmini.canvas import Canvas
from gemmini.d2.line2D import Line2D
from gemmini.d2.point2D import Point2D, Grid
from gemmini.d2.polar2D import Circle, Ellipse
from gemmini.d2.polygon2D import RegularPolygon

import pytest


def test_canvas_1():
    canva = Canvas()
    
    a = Line2D((10,0), (0,15))
    b = Grid(10, 8, num_dot=(10, 8))
    c = Point2D(px=-6, py=9)
    
    canva.add((a,b,c))
    canva.plot()

def test_canvas_2():
    canva = Canvas(scale=2, minor_ticks=False)
    
    a = Line2D((10,0), (0,15))
    b = Line2D((-1,-1), (5,2))
    c = RegularPolygon(6, 10, v=5)
    c.translate(4, 8)
    
    canva.add(a, color='skyblue')
    canva.add(b, draw_style='--')
    canva.add(c, draw_style='*')
    canva.plot()
    
    canva.remove(a)
    canva.plot()
    
def test_canvas_3():
    canva = Canvas(draw_grid=False)
    
    a = Circle(r=3, nD=64)
    b = Ellipse(4, 8, 48)
    a.translate(-6, -4)
    
    canva.add((a, b), show_radius=True)
    canva.plot()
    
def test_canvas_4():
    canva = Canvas()
    
    a = RegularPolygon(s=3, v=7, n=3)
    b = RegularPolygon(s=3, v=6)
    c = RegularPolygon(s=3, v=5)
    
    a.translate(0, 3)
    b.translate(-8, 6)
    c.translate(8, 0)
    
    canva.add(a, show_edges=True)
    canva.add(b, draw_interior=True)
    canva.add(c, show_size=True)
    canva.plot()


if __name__ == "__main__":
    test_canvas_1()
    test_canvas_2()
    test_canvas_3()
    test_canvas_4()