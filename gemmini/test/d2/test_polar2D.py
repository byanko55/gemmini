from gemmini.misc import *
from gemmini.plot import *
from gemmini.d2.polar2D import *

if __name__ == "__main__":
    f = Circle(r=3, nD=64)
    print("Figure: Circle")
    plot(f)
    
    f = Arc(r=4, nD=36, angle=135)
    print("Figure: Arc")
    plot(f)

    f = Ellipse(4, 8, 48)
    print("Figure: Ellipse")
    plot(f)

    f = Spiral(9, 100, 6*pi)
    print("Figure: Spiral")
    plot(f)

    f = HyperbolicSpiral(10, 100, 5*pi)
    print("Figure: HyperbolicSpiral")
    plot(f)

    f = ParabolicSpiral(10, 99, 8*pi)
    print("Figure: ParabolicSpiral", len(f))
    plot(f)

    f = ParabolicSpiral(10, 100, 8*pi)
    print("Figure: ParabolicSpiral", len(f))
    plot(f)

    f = LituusSpiral(8, 150, 5*pi)
    print("Figure: LituusSpiral")
    plot(f)

    f = LogarithmicSpiral(22, 100, 5*pi)
    print("Figure: LogarithmicSpiral")
    plot(f)

    f = Cycloid(5, 40, 6*pi)
    print("Figure: Cycloid")
    plot(f)

    f = Epicycloid(p=5, q=3, radius=30, nD=300)
    print("Figure: Epicycloid")
    plot(f)

    f = Hypocycloid(p=5, q=3, radius=20, nD=300)
    print("Figure: Hypocycloid")
    plot(f)

    f = CurvedPolygon(size=15, nD=100, nV=5)
    print("Figure: CurvedPolygon")
    plot(f)

    f = Lissajous(a=3, b=2, radius=10, nD=300)
    print("Figure: Lissajous")
    plot(f)