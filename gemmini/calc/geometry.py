from gemmini.misc import *
from gemmini.calc.coords import dist, bounding_box

from scipy.spatial import ConvexHull, Delaunay


def connect_edges(*args:object) -> np.ndarray:
    """
    Connect multiple edges (or curves) to form a single geometry.
    
    Args:
        *args (Geometry2D, ...): A series of figures to be assembled with.

    Returns:
        xy (np.ndarray): (x, y) coordinates consisting of the resulted geometry.
    """
    xy = [e[:-1] for e in args]

    return np.concatenate(tuple(xy), axis=0)


def convex_hull(xy:COORDINATES) -> np.ndarray:
    """
    Convex hulls in N dimensions.

    Args:
        xy (tuple | list | np.ndarray): iterable container of points.

    Returns:
        exterior_points (np.ndarray): the (x, y) coordinates of vertices that consist of the boundary.
        exterior_edges (list): list of edges where their two endpoints are included in exterior points. 
    """
    hull = ConvexHull(xy)

    v = hull.vertices

    exterior_edges = [(xy[v[i]], xy[v[(i+1)%len(v)]]) for i in range(len(v))]
    exterior_points = [xy[i] for i in v]

    return exterior_points, exterior_edges


def concave_hull(xy:COORDINATES, alpha:float = 0.9) -> np.ndarray:
    """
    Compute the concave hull of a set of points.
    See reference: https://gist.github.com/jclosure/d93f39a6c7b1f24f8b92252800182889.

    Args:
        xy (tuple | list | np.ndarray): iterable container of points.
        alpha (float): alpha value to influence the gooeyness of the border.
            Smaller numbers don't fall inward as much as larger numbers.
            Too large, and you lose everything!

    Returns:
        exterior_points (np.ndarray): the (x, y) coordinates of vertices that consist of the boundary.
        exterior_edges (list): list of edges where their two endpoints are included in exterior points.
    """
    if len(xy) < 4:
        # When you have a triangle, there is no sense in computing an alpha shape
        return xy, [(xy[i], xy[(i+1)%len(xy)]) for i in range(len(xy))]
    
    Q = []
    opp = {}
    neighbors = [[] for _ in range(len(xy))]
    
    xs, ys, xS, yS = bounding_box(xy)
    scale = dist((xs, ys), (xS, yS))/2
    n = len(xy)
    
    tri = Delaunay(xy)

    def find_opp(opp, i, j, k):
        if (i, j) in opp :
            opp[(i, j)].append(k)
            return
        
        opp[(i, j)] = [k]
        neighbors[i].append(j)
        neighbors[j].append(i)

    for i, j, k in tri.simplices:
        i, j, k = sorted([i, j, k])
        pa = xy[i]
        pb = xy[j]
        pc = xy[k]

        # Lengths of sides of triangle
        a = dist(pa, pb)
        b = dist(pb, pc)
        c = dist(pa, pc)

        # Semiperimeter of triangle
        s = (a + b + c)/2.0

        # Area of triangle by Heron's formula
        area = sqrt(max(0, s*(s-a)*(s-b)*(s-c)))

        if area == 0 :
            continue

        r = a*b*c/(4.0*area)

        # Here's the radius filter.
        if r < scale/(alpha):
            find_opp(opp, i, j, k)
            find_opp(opp, j, k, i)
            find_opp(opp, i, k, j)

    for k,v in opp.items():
        if len(v) == 1:
            Q.append(k)

    ER = set()
    
    while Q:
        i, j = Q.pop()

        k = opp[(i, j)][0]

        erasable = True

        for nb in neighbors[k]:
            _i, _j = min(nb, k), max(nb, k)

            if len(opp[(_i, _j)]) == 1:
                erasable = False
                break

        if not erasable:
            continue

        ER.add((i, j))

        _i, _k = min(i, k), max(i, k)
        opp[(_i, _k)].remove(j)
        Q.append((_i, _k))

        _j, _k = min(j, k), max(j, k)
        opp[(_j, _k)].remove(i)
        Q.append((_j, _k))

    edges = [k for k,v in opp.items() if len(v) == 1 and k not in ER]

    if len(edges) < 3:
        return None, None

    exterior_edges = []
    exterior_points = []

    adj = {}
    chk = {}

    for e in edges:
        if e[0] not in adj:
            adj[e[0]] = set()

        if e[1] not in adj:
            adj[e[1]] = set()

        adj[e[0]].add(e[1])
        adj[e[1]].add(e[0])
        chk[e[0]] = 0
        chk[e[1]] = 0

    def dfs(p, adj, chk):
        chk[p] = 1
        res = [p]

        for q in adj[p]:
            if chk[q] == 0:
                res = res + dfs(q, adj, chk)
                break

        return res

    _idx = dfs(edges[0][0], adj, chk)

    exterior_points = [xy[i] for i in _idx]
    exterior_edges = [(xy[_idx[i]], xy[_idx[(i+1)%len(_idx)]]) for i in range(len(_idx))]

    return np.array(exterior_points), exterior_edges