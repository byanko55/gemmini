from gemmini.misc import *
from gemmini.calc.coords import _isNumber, _isPoint

def to_ndarray(coord:COORDINATES) -> np.ndarray:
    """
    Return the coordinate lists as a numpy array with dimension: (N, 2).
    
    Args:
        coord (tuple | list | np.ndarray): a series of (x, y) coordinates
    """
    res = np.copy(coord)
    
    if _isNumber(res[0]):
        if len(res) != 2:
            raise ValueError("[ERROR] to_ndarray: you should give (x, y) position/positions")
        
        return res.reshape(-1, 2)
    
    if not _isPoint(res[0], dim=2):
        raise ValueError("[ERROR] to_ndarray: you should give (x, y) position/positions")
    
    return res
    
def scale(coord:COORDINATES, sx:float, sy:float = None) -> np.ndarray:
    """
    Resizes a point set on 2D plane.

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        sx (float): the scaling factor to apply on the x-coordinate
        sy (float): the scaling factor to apply on the y-coordinate
    """
    if sy == None:
        sy = sx

    res = to_ndarray(coord)
    res[:, 0] *= sx
    res[:, 1] *= sy
    
    return res

def scaleX(coord:COORDINATES, s:float = None, **kwargs) -> np.ndarray:
    """
    Resizes a point set along the x-axis (horizontally)

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        s | scale (float): the scaling factor to apply on the x-coordinate
    """
    s = assignArg("scaleX", [s], ['scale'], kwargs)

    res = to_ndarray(coord)
    res[:, 0] *= s

    return res

def scaleY(coord:COORDINATES, s:float = None, **kwargs) -> np.ndarray:
    """
    Resizes a point set along the y-axis (vertically)

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        s | scale (float): the scaling factor to apply on the y-coordinate
    """
    s = assignArg("scaleY", [s], ['scale'], kwargs)

    res = to_ndarray(coord)
    res[:, 1] *= s
    
    return res

def translate(coord:COORDINATES, mx:float, my:float) -> np.ndarray:
    """
    Repositions a point set on the 2D plane

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        mx (float): represents shift along x-axis
        my (float): represents shift along y-axis
    """
    res = to_ndarray(coord)
    res[:, 0] += mx
    res[:, 1] += my

    return res
    
def translateX(coord:COORDINATES, mx:float) -> np.ndarray:
    """
    Repositions a point set horizontally on the 2D plane

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        mx (float): represents shift along x-axis
    """
    res = to_ndarray(coord)
    res[:, 0] += mx

    return res

def translateY(coord:COORDINATES, my:float) -> np.ndarray:
    """
    Repositions a point set vertically on the 2D plane

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        my (float): represents shift along y-axis
    """
    res = to_ndarray(coord)
    res[:, 1] += my

    return res

def rotate(coord:COORDINATES, a:float = None, **kwargs) -> np.ndarray:
    """
    Rotate points by `a` radian in the xy-plane (= z-axis).

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        a | angle (float): angle (in radian) of rotation
    """
    a = assignArg("rotate", [a], ['angle'], kwargs)
    
    return rotateZ(coord, a)

def rotateX(coord:COORDINATES, a:float = None, **kwargs) -> np.ndarray:
    """
    Rotate points by `a` radian in the yz-plane (= x-axis).

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        a | angle (float): angle (in radian) of rotation
    """
    a = assignArg("rotateX", [a], ['angle'], kwargs)

    _c = to_ndarray(coord)
    
    x = _c[:, 0]
    y = _c[:, 1]

    rx = x
    ry = y*cos(a)

    return np.stack((rx, ry), axis=1)

def rotateY(coord:COORDINATES, a:float = None, **kwargs) -> np.ndarray:
    """
    Rotate points by `a` radian in the xz-plane (= y-axis).

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        a | angle (float): angle (in radian) of rotation
    """
    a = assignArg("rotateY", [a], ['angle'], kwargs)

    _c = to_ndarray(coord)
    
    x = _c[:, 0]
    y = _c[:, 1]

    rx = x*cos(a)
    ry = y

    return np.stack((rx, ry), axis=1)

def rotateZ(coord:COORDINATES, a:float = None, **kwargs) -> np.ndarray:
    """
    Rotate points by `a` radian in the xy-plane (= z-axis).

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        a | angle (float): angle (in radian) of rotation
    """
    a = assignArg("rotateZ", [a], ['angle'], kwargs)

    _c = to_ndarray(coord)
    
    x = _c[:, 0]
    y = _c[:, 1]

    rx = x*cos(a) - y*sin(a)
    ry = x*sin(a) + y*cos(a)

    return np.stack((rx, ry), axis=1)

def rotate3D(coord:COORDINATES, a1:float = None, a2:float = None, a3:float = None, **kwargs) -> np.ndarray:
    """
    3D rotation

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        a1 | yaw (float): counterclockwise rotation about the z-axis
        a2 | pitch (float): counterclockwise rotation about the y-axis
        a3 | roll (float): counterclockwise rotation about the x-axis
    """
    a1, a2, a3 = assignArg(
        "rotate3D", 
        [a1, a2, a3], 
        ['yaw', 'pitch', 'roll'], 
        kwargs
    )

    _c = to_ndarray(coord)
    
    x = _c[:, 0]
    y = _c[:, 1]

    rx = x*cos(a1)*cos(a2) + y*(cos(a1)*sin(a2)*sin(a3) - sin(a1)*cos(a3))
    ry = x*sin(a1)*cos(a2) + y*(sin(a1)*sin(a2)*sin(a3) + cos(a1)*cos(a3))

    return np.stack((rx, ry), axis=1)

def skew(coord:COORDINATES, a:float = None, ax:float=None, ay:float=None, **kwargs) -> np.ndarray:
    """
    Skews coordinates on the 2D plane.

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        a | angle (float): angle to use to distort the coordinates on the 2D plane 
            same with skew(coord, ax=`a`, ay=`a`)
        ax (float, optional): angle to use to distort the coordinates along the x-axis.
        ay (float, optional): angle to use to distort the coordinates along the y-axis
    """
    if 'angle' in kwargs:
        a = kwargs['angle']
        
    if a == None and ax == None and ay == None:
        raise ValueError("[Error] skew: missing argument `a` (angle)")
    
    if a != None:
        ax = a
        ay = a
        
    if ax == None:
        return skewY(coord, ay)
        
    if ay == None:
        return skewX(coord, ax)
    
    _c = to_ndarray(coord)
    
    x = _c[:, 0]
    y = _c[:, 1]

    rx = x + y*tan(ax)
    ry = x*tan(ay) + y

    return np.stack((rx, ry), axis=1)

def skewX(coord:COORDINATES, a:float = None, **kwargs) -> np.ndarray:
    """
    Skews coordinates in the horizontal direction on the 2D plane

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        a | angle (float): angle (in radian) to use to distort the coordinates along the x-axis
    """
    a = assignArg("skewX", [a], ['angle'], kwargs)

    _c = to_ndarray(coord)
    
    x = _c[:, 0]
    y = _c[:, 1]

    rx = x + y*tan(a)

    return np.stack((rx, y), axis=1)

def skewY(coord:COORDINATES, a:float = None, **kwargs) -> np.ndarray:
    """
    Skews coordinates in the vertical direction on the 2D plane

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        a | angle (float): angle (in radian) to use to distort the coordinates along the y-axis
    """
    a = assignArg("skewY", [a], ['angle'], kwargs)

    _c = to_ndarray(coord)
    
    x = _c[:, 0]
    y = _c[:, 1]

    ry = x*tan(a) + y

    return np.stack((x, ry), axis=1)

def reflect(coord:COORDINATES, p:Tuple[float, float]) -> np.ndarray:
    """
    Flip the given point set about the specific point (x, y),
    and merge it with the original coordinates

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        p (tuple): a point along which to flip over
    """
    original = to_ndarray(coord)
    reflected = flip(np.copy(original), p)

    res = np.concatenate((original, reflected), axis=0)

    return np.unique(res, axis=0)

def reflectX(coord:COORDINATES) -> np.ndarray:
    """
    Flip the given point set about the x-axis,
    and merge it with the original coordinates

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
    """
    original = to_ndarray(coord)
    reflected = flipX(np.copy(original))

    res = np.concatenate((original, reflected), axis=0)

    return np.unique(res, axis=0)

def reflectY(coord:COORDINATES) -> np.ndarray:
    """
    Flip the given point set about the y-axis,
    and merge it with the original coordinates

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
    """
    original = to_ndarray(coord)
    reflected = flipY(np.copy(original))

    res = np.concatenate((original, reflected), axis=0)

    return np.unique(res, axis=0)

def reflectXY(coord:COORDINATES) -> np.ndarray:
    """
    Flip the given point set about the origin (0, 0),
    and merge it with the original coordinates

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
    """
    original = to_ndarray(coord)
    reflected = flipXY(np.copy(original))

    res = np.concatenate((original, reflected), axis=0)

    return np.unique(res, axis=0)

def reflectDiagonal(coord:COORDINATES) -> np.ndarray:
    """
    Flip the given point set about the line: y = x,
    and merge it with the original coordinates

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
    """
    original = to_ndarray(coord)
    reflected = flipDiagonal(np.copy(original))

    res = np.concatenate((original, reflected), axis=0)

    return np.unique(res, axis=0)

def flip(coord:COORDINATES, p:Tuple[float, float]) -> np.ndarray:
    """
    Creates a new point set being the result of the original coordinates flipped about the given point (x, y)

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        p (tuple): a point along which to flip over
    """
    res = to_ndarray(coord)
    res[:, 0] = 2*p[0] - res[:, 0]
    res[:, 1] = 2*p[1] - res[:, 1]

    return res

def flipX(coord:COORDINATES) -> np.ndarray:
    """
    Creates a new point set being the result of the original coordinates flipped about the x-axis

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
    """
    res = to_ndarray(coord)
    res[:, 1] *= -1

    return res

def flipY(coord:COORDINATES) -> np.ndarray:
    """
    Creates a new point set being the result of the original coordinates flipped about the y-axis

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
    """
    res = to_ndarray(coord)
    res[:, 0] *= -1
    
    return res

def flipXY(coord:COORDINATES) -> np.ndarray:
    """
    Creates a new point set being the result of the original coordinates flipped about the origin (0, 0)

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
    """
    res = to_ndarray(coord)
    res[:, 0] *= -1
    res[:, 1] *= -1
    
    return res

def flipDiagonal(coord:COORDINATES) -> np.ndarray:
    """
    Creates a new point set being the result of the original coordinates flipped about the line: y = x 

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
    """
    res = to_ndarray(coord)
    temp = res[:, 0].copy()
    res[:, 0] = res[:, 1].copy()
    res[:, 1] = temp
    
    return res

def dot(coord:COORDINATES, m:np.ndarray) -> np.ndarray:
    """
    Dot product of a given coordinates and a matrix with dimension: (2, 2)

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        m (np.ndarray): 2 x 2 matrix for the matrix multiplication
    """
    if m.shape != (2, 2):
        raise ValueError("[ERROR] dot: you should give (x, y) position/positions")

    _c = to_ndarray(coord)

    return _c @ m

def distort(coord:COORDINATES, method='barrel', rate:float = 0.5):
    """
    Distorts a point set using various distorting methods.

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        method (string): it can be either `barrel` or `pincushion`.
            - barrel: magnification decreases with distance from the optical axis.
            - pincushion: magnification increases with the distance from the optical axis.
        rate (float) : distortion coefficients
    """

    if method not in ['barrel', 'pincushion']:
        raise ValueError("[Error] distort: `method` argument should be either `barrel` or `pincushion`")

    if method == 'pincushion' and rate >= 1:
        raise ValueError("[Error] distort: pincushion distortion coefficients should be larger than `1`")
    
    if method == 'pincushion':
        rate *= -1
    
    _c = to_ndarray(coord)
    x = _c[:, 0]
    y = _c[:, 1]

    cx, cy = np.mean(x), np.mean(y)
    
    r = np.sqrt(np.power(x-cx, 2) + np.power(y-cy, 2))
    R = np.max(r)
    r = r/R

    d = np.sqrt(1 + rate*np.power(r, 2))
    
    rx = cx + (x-cx)/d
    ry = cy + (y-cy)/d

    return np.stack((rx, ry), axis=1)

def focus(coord:COORDINATES, p:Tuple[float, float], rate:float = 0.5):
    """
    Pull the coordinates into a given pivot point

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        p (float, float): (x, y) positions of pivot point
        rate (float) : distortion factor to apply
    """
    
    _c = to_ndarray(coord)
    x = _c[:, 0]
    y = _c[:, 1]

    cx, cy = p
    
    r = np.sqrt(np.power(x-cx, 2) + np.power(y-cy, 2))
    R = np.max(r)
    r = r/R

    d = np.sqrt(1 + rate*np.power(r, 2))
    
    rx = cx + (x-cx)/d
    ry = cy + (y-cy)/d

    return np.stack((rx, ry), axis=1)

def shatter(coord:COORDINATES, p:Tuple[float, float], rate:float = 0.5):
    """
    Repel the coordinates away from a given pivot point

    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        p (float, float): (x, y) positions of pivot point
        rate (float) : distortion factor to apply
    """
    _c = to_ndarray(coord)
    x = _c[:, 0]
    y = _c[:, 1]
    
    cx, cy = p
    
    r = np.sqrt(np.power(x-cx, 2) + np.power(y-cy, 2))
    R = np.max(r)
    r = (R-r)/R

    d = np.sqrt(1 + rate*np.power(r, 2))
    
    rx = -cx + (x+cx)/d
    ry = -cy + (y+cy)/d

    return np.stack((rx, ry), axis=1)