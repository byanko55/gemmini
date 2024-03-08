# Gemmini

[![Pypi](https://img.shields.io/badge/pypi-1.0.1-blue.svg)](https://pypi.org/project/gemmini/)
[![Python](https://img.shields.io/badge/python-%3E%3D%203.7-green.svg)](https://www.python.org/downloads/)
[![pytest](https://github.com/byanko55/gemmini/actions/workflows/pytest.yml/badge.svg)](https://github.com/byanko55/gemmini/actions/workflows/pytest.yml)
[![](https://img.shields.io/badge/License-BSD%203--Clause-orange.svg)](https://opensource.org/licenses/MIT)


> Python package for visualizing and manipulating diverse geometric shapes.

![Demo 1](https://i.ibb.co/9s4twNn/all-with-interior.webp)
![Demo 2](https://i.ibb.co/0QSnDdZ/all-with-exterior.webp)


`Gemmini` provides **70+ geometry classes** including common polygons, curves, and symbols. Built with `numpy` and `matplotlib` packages, it supports easy manipulation and illustration of geometry, while plenty of useful functions for mathematical analysis and 2D/3D transformation are also available.

## Geometries supported by Gemmini

### Pointset
* Point
* Pointcloud
* Grid

### Line
* Line
* Segment

### Polygon
* RegularPolygon
* IsoscelesTriangle
* RightTriangle
* Parallelogram
* Rhombus
* Trapezoid
* RightTrapezoid
* Rectangle
* Kite
* ConcaveKite
* ConcaveStar

### Curve
* Circle
* Arc
* Ellipse
* Spiral
* HyperbolicSpiral
* ParabolicSpiral
* LituusSpiral
* LogarithmicSpiral
* BoundedSpiral
* Cycloid
* Epicycloid
* Hypocycloid
* CurvedPolygon
* Lissajous
* Folium
* Bifolium

### Other shapes
* CircularSector
* CircularSegment
* Wave
* Helix
* Parabola
* SymmetricSpiral
* Star
* Heart
* ButterFly
* CottonCandy
* Boomerang
* Stellate
* Shuriken
* Flower_A
* Flower_B
* Flower_C
* Flower_D
* Flower_E
* Flower_F
* Clover
* FattyStar
* Moon
* Yinyang
* Polygontile
* Gear
* SnippedRect
* RoundedRect
* Plaque
* Ring
* BlockArc
* Cross_A
* Cross_B
* Cross_C
* SunCross
* CelticCross
* BasqueCross
* Lshape
* HalfFrame
* Arrow
* DoubleArrow
* ArrowPentagon
* ArrowChevron
* Teardrop
* Nosign

## Transformation

```Python
import gemmini as gm

f = gm.SunCross(s=9)
gm.plot((f), fill=True)

f.shatter((2, 4), rate=2)
gm.plot((f), fill=True)
gm.plot((f), show_area=True)
```

![Demo 3](https://i.ibb.co/2P1vcvn/example1.webp)

### List of transformations
* **Resizing** - `scale`, `scaleX`, `scaleY`
* **Position Shift** - `translate`, `translateX`, `translateY`
* **Rotation** - `rotate`, `rotateX`, `rotateY`, `rotateZ`, `rotate3D`
* **Symmetric Shift** - `flip`, `flipX`, `flipY`, `flipXY`, `flipDiagonal`
* **Distortion** - `skew`, `skewX`, `skewY`, `distort`, `focus`, `shatter`
* **Others** - `dot`

## Figure Visualization

Create a `Canvas`, on which your nice geometries will be drawn. Make a choice of color theme (default: `light`), canvas size, grid opacity, etc. You can plot either a single geometric object or multiple shapes altogether.

```Python
import gemmini as gm
import numpy as np

canva = gm.Canvas()

cluster_small = gm.Pointcloud2D(s=0.05, num_dot=10)
cluster_medium = gm.Pointcloud2D(s=0.1, num_dot=20)
cluster_large = gm.Pointcloud2D(s=0.2, num_dot=50)

canva.add((cluster_small, cluster_medium, cluster_large), show_center=True)
canva.plot()
```

![Demo 4](https://i.ibb.co/Vtzhhtt/output5.webp)

### Display Options

* **fill** - fill in the interior of the geometry
* **show_edges** - draw path enclosing the given geometry
* **show_radius** - display a radius vector and its length
* **show_size** - display a height/width of the geometry
* **show_center** - display (x, y) coordinates of the centroid
* **show_area** - display the area of the geometry
* **show_class** - display the class name ot the geometry

```Python
import gemmini as gm

canva = gm.Canvas(theme='horizon')

original = gm.IsoscelesTriangle(h=4, w=6)
figs = []

for i in range(6):
    f = original.copy()
    f.translate(8*(i%3), 8*(i//3))
    figs.append(f)

canva.add(figs[0], fill=True)
canva.add(figs[1], show_edges=True)
canva.add(figs[2], show_center=True)
canva.add(figs[3], show_radius=True)
canva.add(figs[4], show_size=True)
canva.add(figs[5], show_area=True)

canva.plot()
```

![Demo 5](https://i.ibb.co/MVrFFdz/example3.webp)

## Requirements

* **Python** >= 3.7
* **numpy** >= 1.21
* **scipy** >= 1.7
* **matplotlib** >= 3.3

## Work with Shapely

We added the simple way to convert geometry to a `shapely` object.  

```Python
import gemmini as gm

from shapely import geometry
import matplotlib.pyplot as plt

f = gm.Polygontile(s=4, v=5)
poly = geometry.Polygon(*f.coordSet())
print(poly.wkt)
```

> POLYGON ((0.8980559531591708 1.2360679774997896, 0.9597258534760096 1.4258684144441638, ... ))

```Python
from shapely.plotting import plot_polygon

plot_polygon(poly)
```

![Shapely](https://i.ibb.co/LPk95yY/output7.webp)

## Tutorials

The below page links contain several useful tutorials running on Ipython:

* **Plot a Point/Pointcloud** - [See here](https://github.com/byanko55/gemmini/blob/master/tutorials/test_point.ipynb)
* **Draw a Infinite/finite Line** - [See here](https://github.com/byanko55/gemmini/blob/master/tutorials/test_line.ipynb)
* **Draw various Geometries** - [Polygons](https://github.com/byanko55/gemmini/blob/master/tutorials/test_polygon.ipynb), [Polar Curves](https://github.com/byanko55/gemmini/blob/master/tutorials/test_polar.ipynb), [Other Symbols & Shapes](https://github.com/byanko55/gemmini/blob/master/tutorials/test_shape.ipynb)
* **Apply Transformation to Geometry** - [See here](https://github.com/byanko55/gemmini/blob/master/tutorials/test_transform.ipynb)
* **Plot Geometry on Python Interactive Window** - [See here](https://github.com/byanko55/gemmini/blob/master/tutorials/test_canvas.ipynb)
* **Use case with Shapely package** - [See here](https://github.com/byanko55/gemmini/blob/master/tutorials/test_shapely.ipynb)
* **List of geometrical illustrations** - [All you want is here!](https://github.com/byanko55/gemmini/blob/master/tutorials/test_all.ipynb)

## Contribution

If you'd like a new shape, transformation, or other mathematical operations to be included, **feel free to leave a issue on this repo**. We are welcome to any kinds of request and feedbacks! 