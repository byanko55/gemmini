from gemmini.misc import *

import matplotlib.path as pth


def to_ndarray(xy:COORDINATES) -> np.ndarray:
    """
    Return the coordinate lists as a numpy array with dimension: (N, 2).
    
    Args:
        xy (tuple | list | np.ndarray): a series of (x, y) coordinates.
    """
    res = np.copy(xy)
    
    if isNumber(res[0]):
        if len(res) != 2:
            raise ValueError(" \
                [ERROR] to_ndarray: Given matrix is not convertible to a numpy array with shape (N, 2). \
            ")
        
        return res.reshape(-1, 2)
    
    if not isPoint(res[0], dim=2):
        raise ValueError(" \
            [ERROR] to_ndarray: Given matrix is not convertible to a numpy array with shape (N, 2). \
        ")
    
    return res


def dist(p:Tuple[Any, ...], q:Tuple[Any, ...]) -> float:
    """
    Returns the Euclidean distance between two points.

    Args:
        p, q (tuple): the coordinates of that point.

    Returns:
        A float value, representing the Euclidean distance between p and q.
    """
    if not (isPoint(p) and isPoint(q)):
        raise ValueError(" \
            [ERROR] dist: Tried to give input that can't be represented as a cartesian point. \
        ")
    
    return np.linalg.norm(np.array(p) - np.array(q))


def mesh_dist(a:np.ndarray, b:np.ndarray) -> np.ndarray:
    """
    Calculate pairwise distances between two different sets of points.
     
    Args:
        a, b (np.ndarray): two coordinate lists.

    Returns:
        res (np.ndarray): pairs of distance.
            res[i][j] = Euclidean distance between the `i`-th point of `a` and `j`-th point of `b`.
    """
    if not isPointSet(a) or not isPointSet(b):
        raise ValueError(" \
            [ERROR] mesh_dist: The dimension of input arrays should be (N, 2). \
        ")
    
    return np.sqrt(((a[:, None] - b[:, :, None]) ** 2).sum(0))


def outer_product(p:Tuple[float, float], q:Tuple[float, float], r:Tuple[float, float] = None) -> float:
    """
    Compute the outer product of given vectors.

    Args:
        p, q (tuple): two cartesian coordinates.
        r (tuple, Optional): If a 3rd coordinates `r` is provided, 
            then it will return the outer product of two vectors: `p -> q` and `p -> r`.
    """
    if type(r) == type(None):
        return p[0]*q[1] - q[0]*p[1]

    return (q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1])


def to_cartesian(r:Union[float, np.ndarray], theta:Union[float, np.ndarray]) -> np.ndarray:
    """
    Transforms polar coordinates (r, θ) into cartesian coordinates (x, y).
    
    Args:
        r (float | np.ndarray): radius.
        theta (float | np.ndarray): angle (in radian).

    Returns:
        xy (np.ndarray): coordinates on cartesian system.
    """
    
    if isNumber(theta):
        xy = np.array([[r*cos(theta), r*sin(theta)]])
    elif isNumberArray(theta) :
        xy = np.stack((r*np.cos(theta), r*np.sin(theta)), axis=1)
    else :
        raise ValueError(" \
            [ERROR] to_cartesian: Both `radius` and `theta` should be a floating value, \
            or list of numbers. \
        ")
    
    return xy


def centroid(xy:COORDINATES) -> Tuple[float, float]:
    """
    Returns The centroid of a given points.

    Args:
        xy (tuple | list | np.ndarray): a series of (x, y) coordinates.
    """
    if not isPointSet(xy):
        raise ValueError(" \
            [ERROR] centroid: Input array should be 2D or 3D point sets. \
        ")
    
    _xm = np.mean([p[0] for p in xy])
    _ym = np.mean([p[1] for p in xy])
    
    return _xm, _ym    


def bounding_box(xy:COORDINATES) -> Tuple[float, float, float, float]:
    """
    Border's coordinates on the X and Y axes that enclose a geometric object.
    
    Args:
        xy (tuple | list | np.ndarray): a series of (x, y) coordinates.

    Returns:
        (x_min, y_min, x_max, y_max): the minimum/maximum position of x, y axes.
    """
    if not isPointSet(xy):
        raise ValueError(" \
            [ERROR] bounding_box: Input array should be 2D or 3D point sets. \
        ")
    
    if isinstance(xy, list):
        lb, bb, rb, tb = inf, inf, -inf, -inf
        
        for p in xy:
            lb = min(lb, p[0])
            bb = min(bb, p[1])
            rb = max(rb, p[0])
            tb = max(tb, p[1])
            
        return lb, bb, rb, tb
    else :
        xs, ys = xy[:, 0], xy[:, 1]

        return min(xs), min(ys), max(xs), max(ys)


def interior_pixels(xy:COORDINATES, density:float = 16) -> np.ndarray:
    """
    Get a grid of pixels located inside of the geometric object.
    
    Args:
        xy (COORDINATES): a matrix of 2D coordinates.
        density (float): dot density of a result geometry.
    """
    border = to_ndarray(xy)
    lb, bb, rb, tb = bounding_box(border)
    
    x, y = np.meshgrid(
        np.linspace(lb, rb, int((rb-lb)*density/min(rb-lb, tb-bb))), 
        np.linspace(bb, tb, int((tb-bb)*density/min(rb-lb, tb-bb)))
    )
    
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x, y)).T
    
    p = pth.Path(border)
    grid = p.contains_points(points)
    idxs = np.where(grid == True)
    inner_xy = points[idxs]
    
    res = np.concatenate((inner_xy, border), axis=0)
    
    return res


def rotate_2D(xy:COORDINATES, theta:float) -> COORDINATES:
    """
    Rotate points in the xy plane anti-clockwise through an angle `theta`.

    Args:
        xy (tuple | np.ndarray): collection of coordinates on 2D space.
        theta (float): rotation angle (in radian).
    """
    if isPoint(xy):
        x, y = xy
        xx = x * cos(theta) - y * sin(theta)
        yy = x * sin(theta) + y * cos(theta)

        return xx, yy
    
    if isinstance(xy, list):
        xy = np.array(xy)
    
    c, s = np.cos(theta), np.sin(theta)
    r = np.array([[c, s], [-s, c]])
    m = np.dot(xy, r)

    return m


def gradient(p:Tuple[float, float], q:Tuple[float, float], radian:bool = False) -> float:
    """
    Returns the gradient of a line connecting given two points.

    Args:
        p, q (tuple): the coordinates of that point.
        radian (bool): if True, the gradient is measured in radian.
    """
    if not (isPoint(p) and isPoint(q)):
        raise ValueError(" \
            [ERROR] gradient: Tried to give input that can't be represented as a cartesian point. \
        ")
    
    if p[0] == q[0]:
        if radian:
            return pi/2 if q[1] > p[1] else 3*pi/2
        
        return inf
    
    g = (q[1]-p[1])/(p[1]-p[0])
    
    return atan(g) if radian else g