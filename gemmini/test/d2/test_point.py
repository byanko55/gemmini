from gemmini.misc import *
from gemmini.d2.point import *

if __name__ == "__main__":
    p = Point2D(3,4)
    p.plot()
    
    points = np.random.rand(10, 2)
    pc = Pointcloud2D(points)
    pc.plot()