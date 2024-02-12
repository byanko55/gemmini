from gemmini.misc import *

__all__ = [
    "dist",
    "_isNumber",
    "_isPoint"
]

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

def _isNumber(n):
    return isinstance(n, (int, float, np.number)) 

def _isPoint(p:Tuple[Any, ...], dim:int = None) -> bool:
    if not isinstance(p, (tuple, list, np.ndarray)):
        return False
    
    if len(p) < 2 or len(p) > 3:
        warnings.warn("We do not support dimensions except 2d or 3d")
        return False
    
    if dim != None and len(p) != dim:
        return False
    
    return all(_isNumber(i) for i in p)