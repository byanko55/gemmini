from gemmini.misc import *

import pytest

def test_number():
    assert isNumber(3) == True
    assert isNumber(3.33) == True
    assert isNumber(3/7) == True
    assert isNumber(np.float32(1.0)) == True
    assert isNumber(np.int32(1)) == True
    assert isNumber('3.33') == False
    
def test_number_array():
    assert isNumberArray(3) == False
    assert isNumberArray(np.array([3])) == True
    assert isNumberArray(np.array([3, 4, 5])) == True
    assert isNumberArray(np.array([[3, 4], [5, 6]])) == False
    assert isNumberArray([3, 8]) == True
    assert isNumberArray([[3, 4], [5, 6]]) == False
    
def test_point():
    assert isPoint([3,4]) == True
    assert isPoint((3,4)) == True
    assert isPoint([3,4.5]) == True
    assert isPoint([4]) == False
    assert isPoint([3,4,5]) == True
    assert isPoint([3,4,5,6]) == False
    assert isPoint(np.array([3,4])) == True
    
def test_point_set():
    assert isPointSet(3) == False
    assert isPointSet((3, 4)) == False
    assert isPointSet([3, 4]) == False
    assert isPointSet([[3, 4]]) == True
    assert isPointSet([[3]]) == False
    assert isPointSet([[3, 4]], dim=3) == False
    assert isPointSet(np.array([[3, 5], [1, 2]])) == True
    assert isPointSet(np.array([1, 2, 5])) == False

def test_is_same():
    assert isSame(1, 1.0) == True
    assert isSame(1, -1) == False
    assert isSame((1, 2), [1, 2]) == True
    assert isSame((1, 2, 3), [1, 2]) == False
    assert isSame((1, 2, 3, 4, 5), np.array([1,2,3,4,5])) == True
    assert isSame((1, 2, 3, 4, 5), np.array([1,2,3,0,5])) == False
    
    a = np.array([[0, 0], [1, 2]])
    b = np.array([[1, 1], [2, 3]])

    assert isSame(a, b) == False
    assert isSame(a+1, b) == True

def test_alias():
    @alias({'arg_a':'a', 'arg_b':'b', 'arg_d':'d'})
    def foo(
        a=None,
        b=2,
        c='a',
        d='%',
        **kwargs
    ):
        return a, b, c, d
    
    assert foo(1, 2) == (1, 2, 'a', '%')
    assert foo(a=0, b=3, c='b') == (0, 3, 'b', '%')
    assert foo(1, b=3, c='c') == (1, 3, 'c', '%')
    assert foo(0, arg_b=4, c='d') == (0, 4, 'd', '%')
    assert foo(arg_a=-1, arg_b=5, d='&') == (-1, 5, 'a', '&')
    assert foo(-2, 2, arg_c='f', d='&') == (-2, 2, 'a', '&')
    assert foo(0) == (0, 2, 'a', '%')
                  
    with pytest.raises(ValueError):
        a, b, c, d = foo()

if __name__ == "__main__":
    test_number()
    test_number_array()
    test_point()
    test_point_set()
    test_is_same()
    test_alias()