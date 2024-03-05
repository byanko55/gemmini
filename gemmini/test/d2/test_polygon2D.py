from gemmini.misc import *
from gemmini.d2.polygon2D import *
from gemmini.canvas import Canvas

import pytest

def test_polygon():
    f = Polygon2D([[0,0], [3,0], [3,3], [2,1.5]])

    assert f.area() == 3.75

    canva = Canvas()
    canva.add(f, show_area=True)
    canva.plot()

def test_basic_polygon():
    fa = RegularPolygon(6, num_vertex=5)
    fb = Parallelogram(h=5, w=8, n=24)
    fc = Parallelogram(size=(9, 6), n=[5, 10, 5, 10], angle=pi/4)
    fd = Rhombus(h=6, w=10)
    fe = Rhombus(s=8, num_dot=[6,12,12,6])

    canva = Canvas()
    canva.add(fa)

    for i, f in enumerate([fb, fc, fd, fe]):
        f.translate(12*cos(i*pi/2), 12*sin(i*pi/2))
        canva.add(f)

    canva.plot()

def test_triangle():
    fa = RegularPolygon(6, num_vertex=3)
    fb = IsoscelesTriangle(size=(7, 5))
    fc = RightTriangle(size=(5, 9))

    canva = Canvas()

    for i, f in enumerate([fa, fb, fc]):
        f.translate(10*cos(i*2*pi/3), 10*sin(i*2*pi/3))
        canva.add(f)

    canva.plot()

def test_trapezoid():
    fa = Trapezoid(s=(8, 6))
    fb = Trapezoid(s=(8, 6, 10))
    fc = Trapezoid(s=(6, 8, 10, 12))
    fd = RightTrapezoid(s=(8, 6, 10))
    
    canva = Canvas()

    for i, f in enumerate([fa, fb, fc, fd]):
        f.translate(10*cos(i*pi/2), 10*sin(i*pi/2))
        canva.add(f)

    canva.plot()

def test_rectangle():
    fa = Rectangle(h=8, w=6, n=40)
    fb = Rectangle(s=(8,6), n=[10, 8, 12, 6])

    canva = Canvas()
    fb.translateY(10)
    canva.add((fa, fb))
    canva.plot()

def test_other_polygon():
    fa = Kite(s=(10, 8))
    fb = ConcaveKite(h=10, w=8)
    fc = ConcaveStar(s=9, num_vertex=5, num_dot=7)

    canva = Canvas()

    for i, f in enumerate([fa, fb, fc]):
        f.translate(10*cos(i*2*pi/3), 10*sin(i*2*pi/3))
        canva.add(f)

    canva.plot()

if __name__ == "__main__":
    test_polygon()
    test_basic_polygon()
    test_triangle()
    test_trapezoid()
    test_rectangle()
    test_other_polygon()