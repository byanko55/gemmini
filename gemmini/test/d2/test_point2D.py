from gemmini.misc import *
from gemmini.plot import *
from gemmini.d2.point2D import *

if __name__ == "__main__":
    p = Point2D(3,4)
    plot(p)
    
    points = 10*np.random.rand(10, 2)
    pc = Pointcloud2D(points)

    print("bounding box: ", pc.bounding_box())
    print("centroid: ", pc.center())
    print("width x height:", pc.dim())
    print("radius: ", pc.rad())
    plot(pc)

    print("2~5th dots: ", pc[1:4])