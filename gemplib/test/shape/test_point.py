from gemplib.misc import *
from gemplib.shape.point import *

if __name__ == "__main__":
    p = Point(3,4)
    p.plot()
    
    points = np.random.rand(10, 2)
    pc = Pointcloud(points)
    pc.plot()