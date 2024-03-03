from gemmini.misc import *
from gemmini.d2.polar2D import *
from gemmini.canvas import Canvas

import pytest

def test_circle():
    fa = Circle(r=5)
    fb = Arc(r=4, angle=3*pi/4, n=16)
    fc = Ellipse(size=(4, 8), n=48)
    fd = Ellipse(height=8, width=4, n=48)

    fa.translate(0, -8)
    fb.translate(8, 0)
    fc.translate(-8, 0)
    fd.translate(0, 8)

    canva = Canvas()
    canva.add((fa, fb, fc, fd))
    canva.plot()

def test_spiral_1():
    fa = Spiral(10, 6*pi, 150)
    fb = ParabolicSpiral(10, 8*pi, 99)
    fc = ParabolicSpiral(10, 8*pi, 100)
    fd = LituusSpiral(10, 5*pi, 150)

    canva = Canvas()
    canva.add(fa)

    for i, f in enumerate([fb, fc, fd]):
        f.translate(25*cos(i*2*pi/3), 25*sin(i*2*pi/3))
        canva.add(f)

    canva.plot()

def test_spiral_2():
    fa = HyperbolicSpiral(10, 4*pi, n=64)

    canva = Canvas()
    canva.add(fa)
    canva.plot()  
    
def test_spiral_3():
    fa = LogarithmicSpiral(10, 2*pi)

    canva = Canvas()
    canva.add(fa)
    canva.plot()  

def test_spiral_4():
    f = BoundedSpiral(10, 8*pi, 256)

    canva = Canvas()
    canva.add(f)
    canva.plot()

def test_cycloid_1():
    f = Cycloid(5, 6*pi, n=128)

    canva = Canvas()
    canva.add(f)
    canva.plot()

def test_cycloid_2():
    fa = Epicycloid(p=5, q=3, size=16)
    fb = Epicycloid(p=2, q=1, size=16)
    fc = Hypocycloid(p=5, q=3, size=16)
    fd = Hypocycloid(p=7, q=4, size=16)

    canva = Canvas()

    for i, f in enumerate([fa, fb, fc, fd]):
        f.translate(12*cos(i*pi/2), 12*sin(i*pi/2))
        canva.add(f)

    canva.plot()

def test_others():
    fa = CurvedPolygon(size=10, num_vertex=5)
    fb = Lissajous(a=3, b=2, size=10)
    fc = Folium(r=10)
    fd = Bifolium(r=10)

    canva = Canvas()
    fb.translateY(12)
    fc.translateX(12)
    fd.translate(12, 12)
    canva.add((fa, fb, fc, fd))
    canva.plot()

if __name__ == "__main__":
    test_circle()
    test_spiral_1()
    test_spiral_2()
    test_spiral_3()
    test_spiral_4()
    test_cycloid_1()
    test_cycloid_2()
    test_others()