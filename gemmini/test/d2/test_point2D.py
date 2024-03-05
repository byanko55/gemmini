from gemmini.misc import *
from gemmini.d2.point2D import *
from gemmini.canvas import Canvas

import pytest

def test_point():
    canva = Canvas()
    p = Point2D(3,4)
    
    points = 5*np.random.rand(20, 2)
    pc = PointSet2D(points)

    print("bounding box: ", pc.bounding_box())
    print("centroid: ", pc.center())
    print("width x height:", pc.dim())
    print("radius: ", pc.rad())
    print("2~5th dots: ", pc[1:4])

    canva.add(p)
    canva.add(pc)
    canva.plot()

def test_grid():
    canva = Canvas()
    g = Grid((5, 4), num_dot=(10, 8))
    
    canva.add(g)
    canva.plot()

if __name__ == "__main__":
    test_point()
    test_grid()