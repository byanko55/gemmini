from gemmini.misc import *
from gemmini.calc.geometry import (
    connect_edges,
    convex_hull,
    concave_hull
)
from gemmini.d2.line2D import Segment

import matplotlib.pyplot as plt

def test_connect_edges():
    a = Segment(7, (0, 0), (3, 4))
    b = Segment(5, (3, 4), (4, -2))
    c = Segment(6, (4, -2), (-3, -1))

    points = connect_edges(a, b, c)
    xs, ys = points[:, 0], points[:, 1]
    plt.scatter(xs, ys)

    plt.show()

def test_convex_hull():
    points = np.random.rand(25, 2)
    xs, ys = points[:, 0], points[:, 1]
    plt.scatter(xs, ys)
    
    _, exterior_edges = convex_hull(points)
    
    for i, j in exterior_edges:
        pa = points[i]
        pb = points[j]

        _x = [pa[0], pb[0]]
        _y = [pa[1], pb[1]]
        plt.plot(_x, _y, 'bo', linestyle="--", zorder=1)

    plt.show()

def test_concave_hull():
    points = np.random.rand(25, 2)
    xs, ys = points[:, 0], points[:, 1]
    plt.scatter(xs, ys)
    
    _, exterior_edges = concave_hull(points)
    
    for i, j in exterior_edges:
        pa = points[i]
        pb = points[j]

        _x = [pa[0], pb[0]]
        _y = [pa[1], pb[1]]
        plt.plot(_x, _y, 'bo', linestyle="--", zorder=1)

    plt.show()

if __name__ == "__main__":
    test_connect_edges()
    test_convex_hull()
    test_concave_hull()