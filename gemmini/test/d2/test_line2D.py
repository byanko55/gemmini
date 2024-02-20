from gemmini.misc import *
from gemmini.plot import *
from gemmini.canvas import Canvas
from gemmini.d2.line2D import Line2D
from gemmini.d2.polygon2D import RegularPolygon

if __name__ == '__main__': 
    canva = Canvas()
    a = Line2D((1,0), slope=1.5)
    assert a.grad() == 1.5

    b = Line2D((-1,0), (0,2))
    assert b.grad() == 2

    aa = Line2D((3, 3), slope=1.5)
    c = Line2D((0, 0), slope=1.5)
    d = Line2D((0, 0), (-2, 1))

    assert a == aa
    assert a != b
    assert a.parallel(c)
    assert not a.parallel(b)
    assert b.orthog(d)

    x, y = b.intersect(d)
    assert (abs(x - (-0.8)) <= 1e-6 and abs(y-0.4) <= 1e-6)
    x, y = a & d
    assert (abs(x - 3/4) <= 1e-6 and abs(y - (-3/8)) <= 1e-6)

    canva.add(a)
    canva.add(b)
    canva.add(c)
    canva.add(d)
    canva.plot()

    canva = Canvas()

    ga = RegularPolygon(s=10, nD=6, nV=6)
    gb = RegularPolygon(s=10, nD=6, nV=4)
    gb.translate(-8, 4)

    assert len(c.intersect(ga)) == 2
    assert len(c.intersect(gb)) == 0

    assert c.on(ga) == True
    assert c.on(gb) == False

    canva.add(c)
    canva.add(ga)
    canva.add(gb)
    canva.plot()