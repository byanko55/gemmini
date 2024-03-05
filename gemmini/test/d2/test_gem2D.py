from gemmini.misc import *
from gemmini.canvas import plot
from gemmini.d2.point2D import PointSet2D
from gemmini.d2.polygon2D import ConcaveStar
from gemmini.d2._gem2D import *

if __name__ == "__main__":
    nx, ny = (20, 20)
    x = np.linspace(-10, 10, nx)
    y = np.linspace(-10, 10, ny)
    xv, yv = np.meshgrid(x, y)
    coord = np.stack((xv.reshape(-1), yv.reshape(-1)), axis=1)
    
    ori = PointSet2D(coord)
    print("Figure: Original")
    plot(ori)
    
    f = ori.copy()
    f.scale(1.5)
    print("Scale: 1.5")
    plot(f, show_size=True)
    
    f = ori.copy()
    f.scale(2, 3)
    print("Scale: x=2, y=3")
    plot(f, show_size=True)
    
    f = ori.copy()
    f.scaleX(3)
    print("ScaleX: 3")
    plot(f, show_size=True)
    
    f = ori.copy()
    f.scaleY(2.5)
    print("ScaleY: 2.5")
    plot(f, show_size=True)
    
    f = ori.copy()
    f.translate(mx=5, my=-25)
    print("Translate: mx=5, my=-25")
    plot(f, show_center=True)
    
    f = ori.copy()
    f.translateX(mx=5)
    print("TranslateX: mx=5")
    plot(f, show_center=True)
    
    f = ori.copy()
    f.translateY(my=25)
    print("TranslateY: 25")
    plot(f, show_center=True)
    
    f = ori.copy()
    f.rotate(a=pi/6)
    print("Rotate: pi/6")
    plot(f, show_radius=True)
    
    f = ori.copy()
    f.rotateX(a=pi/6)
    print("RotateX: pi/6")
    plot(f, show_radius=True)
    
    f = ori.copy()
    f.rotateY(a=pi/6)
    print("RotateY: pi/6")
    plot(f, show_radius=True)
    
    f = ori.copy()
    f.rotateZ(a=pi/6)
    print("RotateZ: pi/6")
    plot(f, show_radius=True)
    
    f = ori.copy()
    f.rotate3D(yaw=pi/6, pitch=pi/3, roll=0)
    print("Rotate3D: yaw:pi/6, pitch:pi/3")
    plot(f, show_radius=True)
    
    f = ori.copy()
    f.rotate3D(pi/6, 0, -pi/4)
    print("Rotate3D: yaw:pi/6, roll:-pi/4")
    plot(f, show_radius=True)
    
    f = ori.copy()
    f.skew(pi/6)
    print("Skew: ax:pi/6, ay:pi/6")
    plot(f)
    
    f = ori.copy()
    f.skew(ax=pi/6)
    print("Skew: ax:pi/6")
    plot(f)
    
    f = ori.copy()
    f.skew(ay=pi/6)
    print("Skew: ay:pi/6")
    plot(f)
    
    f = ori.copy()
    f.skewX(angle=pi/3)
    print("SkewX: pi/3")
    plot(f)
    
    f = ori.copy()
    f.skewY(angle=pi/3)
    print("SkewY: pi/3")
    plot(f)
    
    f = ori.copy()
    f.translate(20, -30)
    f.flip(p=[-15, 10])
    print("Flip: [-15, 10]")
    plot(f, show_center=True)
    
    f = ori.copy()
    f.translate(20, -30)
    f.flipX()
    print("FlipX")
    plot(f, show_center=True)
    
    f = ori.copy()
    f.translate(20, -30)
    f.flipY()
    print("FlipY")
    plot(f, show_center=True)
    
    f = ori.copy()
    f.translate(20, -30)
    f.flipXY()
    print("FlipXY")
    plot(f, show_center=True)
    
    f = ori.copy()
    f.translate(20, -30)
    f.flipDiagonal()
    print("FlipDiagonal")
    plot(f, show_center=True)
    
    f = ori.copy()
    f.dot(m=np.array([[1, 0.5], [-0.5, -2]]))
    print("Dot: [[1, 0.5], [-0.5, -2]]")
    plot(f)

    f = ori.copy()
    f.distort()
    print("Distort: method='barrel', rate=0.5")
    plot(f)
    
    f = ori.copy()
    f.distort(rate=1.0)
    print("Distort: method='barrel', rate=1.0")
    plot(f)
    
    f = ori.copy()
    f.distort(method='pincushion')
    print("Distort: method='pincushion', rate=0.5")
    plot(f)
    
    f = ori.copy()
    f.focus(p=[25,25])
    print("Focus: p=(25,25)")
    plot(f)
    
    f = ori.copy()
    f.focus(p=[25,25], rate=2)
    print("Focus: p=(25,25), rate=2")
    plot(f)
    
    f = ori.copy()
    f.shatter(p=[25,25])
    print("Shatter: p=(25,25)")
    plot(f)
    
    f = ori.copy()
    f.shatter(p=[25,25], rate=2)
    print("Shatter: p=(25,25), rate=2")
    plot(f)
    
    f = ConcaveStar(s=10, nD=6, nV=5)
    print("Original Star")
    plot(f)
    f.translate(5, 10)
    plot(f, show_center=True)
    f.flipXY()
    plot(f, show_center=True)
    f.translate(5, 5)
    plot(f, show_center=True)
    f.rotate(pi/6)
    plot(f, show_radius=True)
    
    f = ConcaveStar(s=10, nD=6, nV=5)
    print("At all")
    f.translate(5, 10)
    f.flipXY()
    f.translate(5, 5)
    f.rotate(pi/6)
    plot(f)