from gemmini.misc import *
from gemmini.d2.shape2D import *
from gemmini.canvas import Canvas

import pytest

def test_shape_1():
    canva = Canvas()

    fa = CircularSector(r=5, a=4*pi/3)
    fb = CircularSegment(r=5, a=2*pi/3)
    fc = CircularSegment(r=5, a=pi)
    fd = CircularSegment(r=5, a=3*pi/2)

    for i, f in enumerate([fa, fb, fc, fd]):
        f.translateX(12*i)
        canva.add(f)

    canva.plot()

def test_shape_2():
    canva = Canvas()

    fa = Wave(a=2, w=8)
    fb = Wave(a=2, w=8, f=2)
    fc = Wave(a=2, w=8, p=pi/2)

    for i, f in enumerate([fa, fb, fc]):
        f.translateX(10*i)
        canva.add(f)

    fd = Helix(r=3)
    fe = Helix(r=3, pitch=3)
    ff = Helix(r=3, a=8*pi, n=128, pitch=3)

    for i, f in enumerate([fd, fe, ff]):
        f.translate(10*i, 20)
        canva.add(f)

    canva.plot()
    
def test_shape_3():
    canva = Canvas()

    fa = Parabola(s=5)
    fb = Parabola(h=8, w=4)
    fc = Parabola(h=4, w=8)

    for i, f in enumerate([fa, fb, fc]):
        f.translateX(10*i)
        canva.add(f)
        
    canva.plot()

def test_shape_4():
    canva = Canvas()

    fa = SymmetricSpiral(r=8)
    canva.add(fa)
        
    canva.plot()
    
def test_shape_5():
    canva = Canvas()

    fa = Star(s=5)
    fb = Star(s=5, v=6)
    fc = Star(s=5, v=8)

    for i, f in enumerate([fa, fb, fc]):
        f.translateX(10*i)
        canva.add(f)
        
    canva.plot()


def test_shape_6():
    canva = Canvas()

    fa = Heart(s=8)
    fb = ButterFly(s=8)
    fc = CottonCandy(s=8, c=6)
    
    for i, f in enumerate([fa, fb, fc]):
        f.translate(10*i, -10)
        canva.add(f)
        
    fd = Boomerang(s=8)
    fe = Stellate(s=8)
    ff = Stellate(s=8, c=8)
        
    for i, f in enumerate([fd, fe, ff]):
        f.translate(10*i, 0)
        canva.add(f)
        
    fg = Shuriken(s=8)
    fh = Shuriken(s=8, border=0.2)
    fi = Shuriken(s=8, border=2/3)
        
    for i, f in enumerate([fg, fh, fi]):
        f.translate(10*i, 10)
        canva.add(f)

    canva.plot()
    
def test_flower():
    canva = Canvas()

    fa = Flower_A(s=8)
    fb = Flower_B(s=8)
    fc = Flower_C(s=8)
    
    for i, f in enumerate([fa, fb, fc]):
        f.translate(9*i, -9)
        canva.add(f)
        
    fd = Flower_D(s=8)
    fe = Flower_E(s=8)
    ff = Flower_F(s=8)
        
    for i, f in enumerate([fd, fe, ff]):
        f.translate(9*i, 0)
        canva.add(f)
        
    canva.plot()
    
def test_shape_7():
    canva = Canvas()

    fa = FattyStar(s=6)
    fb = FattyStar(s=6, v=6)
    fc = Yinyang(s=8)
    
    for i, f in enumerate([fa, fb, fc]):
        f.translate(9*i, -9)
        canva.add(f)
        
    fd = Moon(r=8)
    fe = Moon(r=8, breadth=0.25)
    ff = Moon(r=8, breadth=0.6)
    
    for i, f in enumerate([fd, fe, ff]):
        f.translate(9*i, 0)
        canva.add(f)
        
    canva.plot()
    
def test_polygon_tile():
    canva = Canvas()

    fa = Polygontile(s=4, v=4)
    fb = Polygontile(s=4, v=5)
    fc = Polygontile(s=4, v=6)
    
    for i, f in enumerate([fa, fb, fc]):
        f.translate(9*i, -9)
        canva.add(f)
        
    canva.plot()

def test_shape_8():
    canva = Canvas()

    fa = Gear(r=4)
    fb = Gear(r=4, c=12)
    fc = Gear(r=4, c=16)
    
    for i, f in enumerate([fa, fb, fc]):
        f.translate(9*i, -9)
        canva.add(f)
        
    canva.plot()

def test_snipped_rect():
    canva = Canvas()
    
    fa = SnippedRect(h=5, w=8, nD=100)
    fb = SnippedRect(h=5, w=8, nD=100, clip_size=(1.0, 0, 0, 0))
    fc = SnippedRect(h=5, w=8, nD=100, clip_size=(0.5, 0.4, 0.8))
    fd = SnippedRect(h=5, w=5, nD=100, clip_size=(0, 1.0, 1.0, 1.0))
    fe = SnippedRect(h=5, w=5, nD=100, clip_size=(1.0, 1.0, 1.0, 1.0))
    fb.translate(6, 6)
    fc.translate(-6, 6)
    fd.translate(-6, -6)
    fe.translate(6, -6)
    
    canva.add((fa, fb, fc, fd, fe))
    canva.plot()
    
def test_rounded_rect():
    canva = Canvas()
    
    fa = RoundedRect(h=5, w=8, nD=100)
    fb = RoundedRect(h=5, w=8, nD=100, border_radius=(1.0, 0, 0, 0))
    fc = RoundedRect(h=5, w=8, nD=100, border_radius=(0.5, 0.4, 0.8))
    fd = RoundedRect(h=5, w=5, nD=100, border_radius=(0, 1.0, 1.0, 1.0))
    fe = RoundedRect(h=5, w=5, nD=100, border_radius=(1.0, 1.0, 1.0, 1.0))
    fb.translate(6, 6)
    fc.translate(-6, 6)
    fd.translate(-6, -6)
    fe.translate(6, -6)
    
    canva.add((fa, fb, fc, fd, fe))
    canva.plot()
    
def test_shape_8():
    canva = Canvas()
    
    fa = Plaque(s=8, nD=200)
    fb = Plaque(s=8, nD=200, border_radius=0.99)
    fc = Plaque(s=8, nD=200, border_radius=0.1)
    
    for i, f in enumerate([fa, fb, fc]):
        f.translate(9*i, -9)
        canva.add(f)
        
    fd = Ring(R=4, r=3)
    fe = BlockArc(R=4, r=2, a=pi)
    ff = BlockArc(R=4, r=2, a=3*pi/2, n=100)
    
    for i, f in enumerate([fd, fe, ff]):
        f.translate(9*i, 0)
        canva.add(f)
        
    canva.plot()
    
def test_cross_1():
    canva = Canvas()
    
    fa = Cross_A(s=8, w=2)
    fb = Cross_A(s=8, w=1)
    fc = Cross_A(s=8, w=6)
    
    for i, f in enumerate([fa, fb, fc]):
        f.translate(9*i, -9)
        canva.add(f)
        
    fd = Cross_B(s=8)
    fe = Cross_B(s=8, border_radius=0.75)
    ff = Cross_C(s=8)
    
    for i, f in enumerate([fd, fe, ff]):
        f.translate(9*i, 0)
        canva.add(f)
        
    canva.plot()
    
def test_cross_2():
    canva = Canvas()
    
    fa = SunCross(s=8)
    fb = BasqueCross(s=8)
    fc = CelticCross(s=8)
    
    for i, f in enumerate([fa, fb, fc]):
        f.translate(9*i, 0)
        canva.add(f)
        
    canva.plot()
    
def test_shape_9():
    canva = Canvas()
    
    fa = Lshape(w=3)
    fb = HalfFrame(h=5, w=8, breadth=1.5)
    
    for i, f in enumerate([fa, fb]):
        f.translate(12*i, -5)
        canva.add(f)
    
    fc = Teardrop(s=6, n=100)
    fd = Nosign(s=8, n=100)
    
    for i, f in enumerate([fc, fd]):
        f.translate(12*i, 5)
        canva.add(f)
        
    canva.plot()
        
def test_arrow():
    canva = Canvas()
    
    fa = Arrow(h=3, w=10)
    fb = DoubleArrow(h=3, w=10)
    
    for i, f in enumerate([fa, fb]):
        f.translate(12*i, -3)
        canva.add(f)
    
    fc = ArrowPentagon(h=3, w=10)
    fd = ArrowChevron((5, 5))
    
    for i, f in enumerate([fc, fd]):
        f.translate(12*i, 3)
        canva.add(f)
        
    canva.plot()
    
def test_shape_10():
    canva = Canvas()
    
    fg = Clover(s=8, num_leaves=3)
    
    for i, f in enumerate([fg]):
        f.translate(9*i, 0)
        canva.add(f)
        
    canva.plot()
    

if __name__ == "__main__":
    test_shape_1()
    test_shape_2()
    test_shape_3()
    test_shape_4()
    test_shape_5()
    test_shape_6()
    test_flower()
    test_shape_7()
    test_polygon_tile()
    test_snipped_rect()
    test_rounded_rect()
    test_shape_8()
    test_cross_1()
    test_cross_2()
    test_shape_9()
    test_arrow()
    test_shape_10()