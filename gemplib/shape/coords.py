from gemplib.misc import *

__all__ = [
    "dist",
    "_isNumber",
    "_isPoint"
]

def dist(p:Tuple[int, int], q:Tuple[int, int]) -> float:
    """
    Returns the Euclidean distance between two points (p and q), where p and q are the coordinates of that point.

    Args:
        p, q (Tuple[int, int]): the coordinates of that point.

    Returns:
        A float value, representing the Euclidean distance between p and q
    """
    if not (_isPoint(p) and _isPoint(q)):
        raise ValueError(" \
            [ERROR] dist: require (x, y) coordinates of two points \
        ")
    
    return sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)

def _isNumber(n):
    return isinstance(n, (int, float, np.number)) 

def _isPoint(p:Tuple[float, float]) -> bool:
    if isinstance(p, (tuple, list, np.ndarray)) \
    and len(p) == 2 \
    and _isNumber(p[0]) \
    and _isNumber(p[1]):
        return True
    
    return False
    
    