from gemmini.misc import *
from gemmini.canvas import plot
from gemmini.d2.point2D import *
from gemmini.d2.transform2D import *

if __name__ == "__main__":
    _o = to_ndarray(np.array([3, 2]))
    assert _o.tolist() == [[3, 2]]
    assert _o.shape == (1, 2)
    assert type(_o) == np.ndarray
    
    _o = to_ndarray([3, 2])
    assert _o.tolist() == [[3, 2]]
    assert _o.shape == (1, 2)
    
    _o = to_ndarray((3, 2))
    assert _o.tolist() == [[3, 2]]
    assert _o.shape == (1, 2)
    
    _o = to_ndarray([[3, 2], [4, 5]])
    assert _o.tolist() == [[3, 2], [4, 5]]
    assert _o.shape == (2, 2)
    
    _o = to_ndarray(np.array([[3, 2], [4, 5]]))
    assert _o.tolist() == [[3, 2], [4, 5]]
    assert _o.shape == (2, 2)
    assert type(_o) == np.ndarray
    
    nx, ny = (10, 10)
    x = np.linspace(-10, 10, nx)
    y = np.linspace(-10, 10, ny)
    xv, yv = np.meshgrid(x, y)
    coord = np.stack((xv.reshape(-1), yv.reshape(-1)), axis=1)
    
    p = PointSet2D(coord)
    print("Figure: Original")
    plot(p)
    
    c = scale(coord, 1.5)
    p = PointSet2D(c)
    print("Scale: 1.5")
    plot(p)
    
    c = scale(coord, 2, 3)
    p = PointSet2D(c)
    print("Scale: x=2, y=3")
    plot(p)
    
    c = scaleX(coord, 3)
    p = PointSet2D(c)
    print("ScaleX: 3")
    plot(p)
    
    c = scaleY(coord, 2.5)
    p = PointSet2D(c)
    print("ScaleY: 2.5")
    plot(p)
    
    c = translate(coord, mx=5, my=-25)
    p = PointSet2D(c)
    print("Translate: mx=5, my=-25")
    plot(p)
    
    c = translateX(coord, mx=5)
    p = PointSet2D(c)
    print("TranslateX: mx=5")
    plot(p)
    
    c = translateY(coord, my=25)
    p = PointSet2D(c)
    print("TranslateY: 25")
    plot(p)
    
    c = rotate(coord, a=pi/6)
    p = PointSet2D(c)
    print("Rotate: pi/6")
    plot(p)
    
    c = rotateX(coord, a=pi/6)
    p = PointSet2D(c)
    print("RotateX: pi/6")
    plot(p)
    
    c = rotateY(coord, a=pi/6)
    p = PointSet2D(c)
    print("RotateY: pi/6")
    plot(p)
    
    c = rotateZ(coord, a=pi/6)
    p = PointSet2D(c)
    print("RotateZ: pi/6")
    plot(p)
    
    c = rotate3D(coord, yaw=pi/6, pitch=pi/3, roll=0)
    p = PointSet2D(c)
    print("Rotate3D: yaw:pi/6, pitch:pi/3")
    plot(p)
    
    c = rotate3D(coord, pi/6, 0, -pi/4)
    p = PointSet2D(c)
    print("Rotate3D: yaw:pi/6, roll:-pi/4")
    plot(p)
    
    c = skew(coord, pi/6)
    p = PointSet2D(c)
    print("Skew: ax:pi/6, ay:pi/6")
    plot(p)
    
    c = skew(coord, ax=pi/6)
    p = PointSet2D(c)
    print("Skew: ax:pi/6")
    plot(p)
    
    c = skew(coord, ay=pi/6)
    p = PointSet2D(c)
    print("Skew: ay:pi/6")
    plot(p)
    
    c = skewX(coord, angle=pi/3)
    p = PointSet2D(c)
    print("SkewX: pi/3")
    plot(p)
    
    c = skewY(coord, angle=pi/3)
    p = PointSet2D(c)
    print("SkewY: pi/3")
    plot(p)
    
    c = reflect(coord, p=[-15, 10])
    p = PointSet2D(c)
    print("Reflect: [-15, 10]")
    plot(p)
    
    coord2 = to_ndarray(coord)
    coord2[:, 0] += 20
    coord2[:, 1] -= 30
    
    c = reflectX(coord2)
    p = PointSet2D(c)
    print("ReflectX")
    plot(p)
    
    c = reflectY(coord2)
    p = PointSet2D(c)
    print("ReflectY")
    plot(p)
    
    c = reflectXY(coord2)
    p = PointSet2D(c)
    print("ReflectXY")
    plot(p)
    
    c = reflectDiagonal(coord2)
    p = PointSet2D(c)
    print("ReflectDiagonal")
    plot(p)
    
    c = flip(coord, p=[-15, 10])
    p = PointSet2D(c)
    print("Flip: [-15, 10]")
    plot(p)
    
    c = flipX(coord2)
    p = PointSet2D(c)
    print("FlipX")
    plot(p)
    
    c = flipY(coord2)
    p = PointSet2D(c)
    print("FlipY")
    plot(p)
    
    c = flipXY(coord2)
    p = PointSet2D(c)
    print("FlipXY")
    plot(p)
    
    c = flipDiagonal(coord2)
    p = PointSet2D(c)
    print("FlipDiagonal")
    plot(p)
    
    c = dot(coord, m=np.array([[1, 0.5], [-0.5, -2]]))
    p = PointSet2D(c)
    print("Dot: [[1, 0.5], [-0.5, -2]]")
    plot(p)

    c = distort(coord)
    p = PointSet2D(c)
    print("Distort: method='barrel', rate=0.5")
    plot(p)
    
    c = distort(coord, rate=1.0)
    p = PointSet2D(c)
    print("Distort: method='barrel', rate=1.0")
    plot(p)
    
    c = distort(coord, method='pincushion')
    p = PointSet2D(c)
    print("Distort: method='pincushion', rate=0.5")
    plot(p)
    
    c = focus(coord, p=[25,25])
    p = PointSet2D(c)
    print("Focus: p=(25,25)")
    plot(p)
    
    c = focus(coord, p=[25,25], rate=2)
    p = PointSet2D(c)
    print("Focus: p=(25,25), rate=2")
    plot(p)
    
    c = shatter(coord, p=[25,25])
    p = PointSet2D(c)
    print("Shatter: p=(25,25)")
    plot(p)
    
    c = shatter(coord, p=[25,25], rate=2)
    p = PointSet2D(c)
    print("Shatter: p=(25,25), rate=2")
    plot(p)