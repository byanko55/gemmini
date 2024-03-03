from gemmini.misc import *
from gemmini.canvas import Canvas
from gemmini.d2.line2D import *
from gemmini.d2.polygon2D import RegularPolygon

import pytest

def test_line2D_1():
    a = Line2D((1,0), slope=1.5)
    assert a.grad() == 1.5

    b = Line2D((-1,0), (0,2))
    assert b.grad() == 2

def test_line2D_2():
    a = Line2D((1,0), slope=1.5)
    b = Line2D((3, 3), slope=1.5)
    c = Line2D((-1,0), (0,2))
    d = Line2D((0, 0), slope=1.5)
    e = Line2D((0, 0), (-2, 1))

    assert a == b
    assert a != c
    assert a.parallel(d)
    assert not a.parallel(c)
    assert c.orthog(e)

def test_line2D_3():
    canva = Canvas(scale=1.5)

    a = Line2D((1,0), slope=1.5)
    b = Line2D((-1,0), (0,2))
    c = Line2D((0, 0), (-2, 1))

    x, y = b.intersect(c)
    assert (abs(x - (-0.8)) <= 1e-6 and abs(y-0.4) <= 1e-6)
    canva.add((x, y))

    x, y = a & c
    assert (abs(x - 3/4) <= 1e-6 and abs(y - (-3/8)) <= 1e-6)
    canva.add((x, y))

    canva.add([a, b, c])
    canva.plot()

def test_segment():
    canva = Canvas()

    a = Segment(p1=(8,8), p2=(10,10), n=6)
    b = Segment(size=10, slope=pi/3, n=6)
    c = Segment((5, 5), (5, -5), 9)

    canva.add(a)
    canva.add(b)
    canva.add(c)
    canva.plot()

    with pytest.raises(ValueError):
        a = Segment(p1=(7, 5), slope=pi/4, n=5)

    with pytest.raises(ValueError):
        a = Segment(size=10, p2=(10,10))

    with pytest.raises(ValueError):
        a = Segment(p1=(7, 5), p2=[[10]])

def test_line_with_point():
    a = Line2D((0, 0), slope=1.5)

    assert a.on((2, 3)) == True
    assert a.on((3, 2)) == False

def test_line_with_gem():
    canva = Canvas()
    a = Line2D((0, 0), slope=1.5)

    ga = RegularPolygon(s=10, n=6, v=6)
    gb = RegularPolygon(s=10, n=6, v=4)
    gb.translate(-8, 4)

    assert len(a.intersect(ga)) == 2
    assert len(a.intersect(gb)) == 0

    assert a.on(ga) == True
    assert a.on(gb) == False

    canva.add(a)
    canva.add(ga)
    canva.add(gb)
    canva.plot()

def test_line_with_segment():
    canva = Canvas()
    a = Line2D((1, 0), slope=1/2)
    sa = Segment(p1=(0,3), p2=(3,2), n=10)
    sb = Segment(size=5, slope=pi/4, n=10)

    assert a.on(sa) == False
    assert a.on(sb) == True

    canva.add(a)
    canva.add(sa)
    canva.add(sb)
    canva.plot()

if __name__ == '__main__': 
    test_line2D_1()
    test_line2D_2()
    test_line2D_3()
    test_line_with_gem()
    test_segment()
    test_line_with_segment()