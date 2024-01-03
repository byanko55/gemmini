from gemplib.misc import *
from gemplib.shape.coords import *

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
    assert _isPoint([3,4,5]) == False
    assert _isPoint(np.array([3,4])) == True
    
    assert dist(p=[0,0], q=[3,0]) == 3
    assert dist(p=[0,0], q=[3,4]) == 5
    