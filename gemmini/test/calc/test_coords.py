from gemmini.misc import *
from gemmini.calc.coords import _isNumber, _isPoint, dist, polar_pixels, rotate_2D

if __name__ == "__main__":
    assert _isNumber(3) == True
    assert _isNumber(3.33) == True
    assert _isNumber(3/7) == True
    assert _isNumber(np.float32(1.0)) == True
    assert _isNumber(np.int32(1)) == True
    assert _isNumber('3.33') == False
    
    assert _isPoint([3,4]) == True
    assert _isPoint((3,4)) == True
    assert _isPoint([3,4.5]) == True
    assert _isPoint([4]) == False
    assert _isPoint([3,4,5]) == True
    assert _isPoint([3,4,5,6]) == False
    assert _isPoint(np.array([3,4])) == True
    
    assert dist(p=[0,0], q=[3,0]) == 3
    assert dist(p=[0,0], q=[3,4]) == 5
    assert dist(p=[0,1,2], q=[1,3,4]) == 3

    _o = polar_pixels(r=2, theta=pi/4)
    assert _o[0][0] == 2*cos(pi/4)
    assert _o[0][1] == 2*sin(pi/4)

    theta = np.linspace(0, np.pi/2, 4)
    _o = polar_pixels(10, theta)
    assert _o[1][0] == 10*cos(pi/6)
    assert _o[1][1] == 10*sin(pi/6)
    assert _o[2][0] == 10*cos(pi/3)
    assert _o[2][1] == 10*sin(pi/3)

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
