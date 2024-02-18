from gemmini.misc import *

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

def mesh_dist(a:np.ndarray, b:np.ndarray) -> np.ndarray:
    """
    Return 2D matrix where each element represents the Euclidean distance,
    between two points chosen from two different coordinate lists, respectively.
     
    Args:
        a, b (np.ndarray): two coordinate lists

    Returns:
        res (np.ndarray): pairs of distance
            res[i][j] = Euclidean distance between the `i`-th point of `a` and `j`-th point of `b`.
    """
    res = np.zeros((len(a), len(b)))
    
    for i, aa in enumerate(a):
        for j, bb in enumerate(b):
            res[i][j] = np.linalg.norm(aa-bb)
            
    return res

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

def bounding_box(coord:COORDINATES) -> Tuple[float, float, float, float]:
    """
    border's coordinates on the X and Y axes that enclose a geometric object

    Returns:
        (x_min, y_min, x_max, y_max): the minimum/maximum position of x, y axes
    """
    if not _isPointSet(coord):
        raise ValueError("[Error] bounding_box: input array is not a form of 2D/3D cooridinate matrix")
    
    if isinstance(coord, list):
        lb, bb, rb, tb = inf, inf, -inf, -inf
        for p in coord:
            lb = min(lb, p[0])
            bb = min(bb, p[1])
            rb = max(rb, p[0])
            tb = max(tb, p[1])
            
        return lb, bb, rb, tb
    else :
        xs, ys = coord[:, 0], coord[:, 1]

        return min(xs), min(ys), max(xs), max(ys)

def interior_pixels(coord:COORDINATES, density:int = 16) -> np.ndarray:
    """
    Get pixels inside of the border of geometric object
    
    Args:
        coord (COORDINATES): a matrix of 2D coordinates
        density (int): density of points inside a result geometry
    """
    border = to_ndarray(coord)
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
    inner_coord = points[idxs]
    
    res = np.concatenate((inner_coord, border), axis=0)
    
    return res

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

def _isNumber(n:Any) -> bool:
    return isinstance(n, (int, float, np.number))

def _isNumberArray(a:Any) -> bool:
    if isinstance(a, np.ndarray) and len(a.shape) == 1 and _isNumber(a[0]):
        return True
    
    if isinstance(a, list) and not isinstance(a[0], list) and _isNumber(a[0]):
        return True
    
    return False

def _isPoint(p:Any, dim:int = None) -> bool:
    if not isinstance(p, (tuple, list, np.ndarray)):
        return False
    
    if len(p) < 2 or len(p) > 3:
        warnings.warn("We do not support dimensions except 2d or 3d")
        return False
    
    if dim != None and len(p) != dim:
        return False
    
    return all(_isNumber(i) for i in p)

def _isPointSet(p:Any, dim:int = None) -> bool:
    if not isinstance(p, (list, np.ndarray)):
        return False
    
    if isinstance(p, list) and not isinstance(p[0], list):
        return False
    
    if isinstance(p[0], list) and (len(p[0]) < 2 or len(p[0]) > 3):
        return False
    
    if dim != None and len(p[0]) != dim:
        return False
    
    if isinstance(p, np.ndarray) and (p.shape[1] < 2 or p.shape[1] > 3):
        return False
    
    return True