from gemmini.misc import *

def dist(p:Tuple[Any, ...], q:Tuple[Any, ...]) -> float:
    """
    Returns the Euclidean distance between two points (p and q), where p and q are the coordinates of that point.

    Args:
        p, q (Tuple[Any, ...]): the coordinates of that point.

    Returns:
        A float value, representing the Euclidean distance between p and q
    """
    if not (_isPoint(p) and _isPoint(q)):
        raise ValueError(" \
            [ERROR] dist: require (x, y) coordinates of two points \
        ")
    
    return np.linalg.norm(np.array(p) - np.array(q))

def polar_pixels(r:Union[float, np.ndarray], theta:Union[float, np.ndarray]) -> np.ndarray:
    """
    Transforms polar coordinates (r, θ) into cartesian coordinates (x, y).
    
    Args:
        r (float | np.ndarray): radius
        theta (float | np.ndarray): angle (in radian)

    Returns:
        coord (np.ndarray): coordinates on cartesian system.
    """
    
    if _isNumber(theta):
        coord = np.array([[r*cos(theta), r*sin(theta)]])
    elif _isNumberArray(theta) :
        coord = np.stack((r*np.cos(theta), r*np.sin(theta)), axis=1)
    else :
        raise ValueError(" \
            [ERROR] polar_pixels: radius/theta should be a floating value or list of numbers, \
        ")
    
    return coord

def rotate_2D(xy:Union[Tuple, List, np.ndarray], theta:float) -> Union[Tuple, np.ndarray]:
    """
    Rotate points in the xy plane anti-clockwise through an angle `theta`

    Args:
        xy (tuple | np.ndarray): collection of coordinates on 2D space.
        theta (float): rotation angle (in radian)
    """
    if _isPoint(xy):
        x, y = xy
        xx = x * cos(theta) - y * sin(theta)
        yy = x * sin(theta) + y * cos(theta)

        return xx, yy
    
    if isinstance(xy, list):
        xy = np.array(xy)
    
    c, s = np.cos(theta), np.sin(theta)
    r = np.array([[c, -s], [s, c]])
    m = np.dot(xy, r)

    return m

def _isNumber(n) -> bool:
    return isinstance(n, (int, float, np.number))

def _isNumberArray(a) -> bool:
    if isinstance(a, np.ndarray) and len(a.shape) == 1 and _isNumber(a[0]):
        return True
    
    if isinstance(a, list) and not isinstance(a[0], list) and _isNumber(a[0]):
        return True
    
    return False

def _isPoint(p:Tuple[Any, ...], dim:int = None) -> bool:
    if not isinstance(p, (tuple, list, np.ndarray)):
        return False
    
    if len(p) < 2 or len(p) > 3:
        warnings.warn("We do not support dimensions except 2d or 3d")
        return False
    
    if dim != None and len(p) != dim:
        return False
    
    return all(_isNumber(i) for i in p)