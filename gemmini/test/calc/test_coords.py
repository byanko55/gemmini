from gemmini.misc import *
from gemmini.calc.coords import (
    _isNumber, 
    _isNumberArray,
    _isPoint,
    _isPointSet,
    to_ndarray,
    dist, 
    mesh_dist,
    outer_product,
    polar_pixels,
    concave_hull,
    bounding_box,
    interior_pixels,
    rotate_2D
)
from gemmini.d2.point2D import Grid
from gemmini.d2.polygon2D import RegularPolygon

import pytest

def test_to_ndarray():
    a = to_ndarray([0, 2])
    assert type(a) == np.ndarray
    assert a.shape == (1, 2)
    
    with pytest.raises(ValueError):
        a = to_ndarray([0, 2, 3])
        
    a = to_ndarray([[0, 2], [3, 4]])
    assert type(a) == np.ndarray
    assert a.shape == (2, 2)
        
    with pytest.raises(ValueError):
        a = to_ndarray([[0, 2, 3], [3, 4, 5]])

def test_number():
    assert _isNumber(3) == True
    assert _isNumber(3.33) == True
    assert _isNumber(3/7) == True
    assert _isNumber(np.float32(1.0)) == True
    assert _isNumber(np.int32(1)) == True
    assert _isNumber('3.33') == False
    
def test_number_array():
    assert _isNumberArray(3) == False
    assert _isNumberArray(np.array([3])) == True
    assert _isNumberArray(np.array([3, 4, 5])) == True
    assert _isNumberArray(np.array([[3, 4], [5, 6]])) == False
    assert _isNumberArray([3, 8]) == True
    assert _isNumberArray([[3, 4], [5, 6]]) == False
    
def test_point():
    assert _isPoint([3,4]) == True
    assert _isPoint((3,4)) == True
    assert _isPoint([3,4.5]) == True
    assert _isPoint([4]) == False
    assert _isPoint([3,4,5]) == True
    assert _isPoint([3,4,5,6]) == False
    assert _isPoint(np.array([3,4])) == True
    
def test_point_set():
    assert _isPointSet(3) == False
    assert _isPointSet((3, 4)) == False
    assert _isPointSet([3, 4]) == False
    assert _isPointSet([[3, 4]]) == True
    assert _isPointSet([[3]]) == False
    assert _isPointSet([[3, 4]], dim=3) == False
    assert _isPointSet(np.array([[3, 5], [1, 2]])) == True
    assert _isPointSet(np.array([1, 2, 5])) == False
    
def test_dist():
    assert dist(p=[0,0], q=[3,0]) == 3
    assert dist(p=[0,0], q=[3,4]) == 5
    assert dist(p=[0,1,2], q=[1,3,4]) == 3
    
def test_mesh_dist():
    a = np.array([[1,0,0],[0,1,0],[0,0,1]])
    b = np.array([[1,1,0],[0,1,1],[1,0,1]])
    c = mesh_dist(a, b)
    
    ans = np.array([[1, sqrt(3), 1], [1, 1, sqrt(3)], [sqrt(3), 1, 1]])
    assert np.mean(c - ans) <= 1e-6
    assert c.shape == (3, 3)
    
def test_outer_product():
    a = np.array([3, 6])
    b = np.array([9, 10])
    assert outer_product(a, b) == -24
    
    a = np.array([1, 2])
    b = np.array([3, 7])
    c = np.array([-1, 4])
    assert outer_product(a, b, c) == 14
    
def test_polar_pixels():
    _o = polar_pixels(r=2, theta=pi/4)
    assert _o[0][0] == 2*cos(pi/4)
    assert _o[0][1] == 2*sin(pi/4)

    theta = np.linspace(0, np.pi/2, 4)
    _o = polar_pixels(10, theta)
    assert _o[1][0] == 10*cos(pi/6)
    assert _o[1][1] == 10*sin(pi/6)
    assert _o[2][0] == 10*cos(pi/3)
    assert _o[2][1] == 10*sin(pi/3)
    
def test_concave_hull():
    points = np.random.rand(25, 2)
    xs, ys = points[:, 0], points[:, 1]
    plt.scatter(xs, ys)
    
    exterior_edges = concave_hull(points)
    
    for i, j in exterior_edges:
        pa = points[i]
        pb = points[j]

        _x = [pa[0], pb[0]]
        _y = [pa[1], pb[1]]
        plt.plot(_x, _y, 'bo', linestyle="--", zorder=1)

    plt.show()
    
def test_bounding_box():
    with pytest.raises(ValueError):
        bounding_box([3, 4, 5])
        
    f = Grid(h=10, w=6, nD=12)
    f.translate(3, -7)
    
    assert bounding_box(f.coords()) == (0, -12, 6, -2)
    
def test_interior_pixels():
    f = RegularPolygon(s=5, nD=10, nV=5)
    points = f.coords()
    _c = interior_pixels(points)
    
    _x, _y = _c[:, 0], _c[:, 1]
    plt.scatter(_x, _y, c='orange')
    
    xs, ys = points[:, 0], points[:, 1]
    plt.scatter(xs, ys, c='blue', zorder=10)
    
    plt.show()
    
def test_rotate_2D():
    _x, _y = rotate_2D((2, 0), np.pi/2)
    assert (_x - 0.0) < 1e-6
    assert (_y - 2.0) < 1e-6

    _x, _y = rotate_2D(np.array([1, 1]), np.pi/2)
    assert (_x - (-1.0)) < 1e-6
    assert (_y - 1.0) < 1e-6

    _x, _y = rotate_2D([2, 1], np.pi)
    assert (_x - (-2.0)) < 1e-6
    assert (_y - (-1.0)) < 1e-6

    _o = rotate_2D(np.array([[1, 1], [3, 0]]), np.pi/3)
    assert _o[1][0] - 3*cos(np.pi/3) < 1e-6
    assert _o[1][1] - 3*sin(np.pi/3) < 1e-6

if __name__ == "__main__":
    test_to_ndarray()
    test_number()
    test_number_array()
    test_point()
    test_point_set()
    test_dist()
    test_mesh_dist()
    test_outer_product()
    test_polar_pixels()
    test_concave_hull()
    test_bounding_box()
    test_interior_pixels()
    test_rotate_2D()
