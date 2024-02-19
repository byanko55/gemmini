from gemmini.misc import *
from gemmini.plot import *
from gemmini.d2.line2D import Line2D

import unittest

class SelfTests(unittest.TestCase): 
    def line1(self):
        l = Line2D((1,0), slope=1.5)
        self.assertTrue(l.grad() == 1.5)
        plot(l)

    def line2(self):
        l = Line2D((1,0), (2,2))
        self.assertTrue(l.grad() == 2)
        plot(l)

    def line_invalid1(self):
        with self.assertRaises(ValueError):
            l = Line2D((1,0), (2,2), slope=1.5)

    def line_invalid2(self):
        with self.assertRaises(ValueError):
            l = Line2D((1,0), 4)

    def line_invalid3(self):
        with self.assertRaises(ValueError):
            l = Line2D((1,0), slope='1.5')

    def two_lines(self):
        a = Line2D((0, 0), slope=2)
        b = Line2D((0, 1), slope=2)
        c = Line2D((0, 0), slope=-1/2)
        d = Line2D((2, 2), (2, -2))
        e = Line2D((3, 0), (-3, 0))

        self.assertTrue(a.parallel(b))
        self.assertFalse(a.parallel(c))
        self.assertTrue(a.orthog(c))
        self.assertTrue(d.orthog(e))

        x, y = d.intersect(e)
        self.assertTrue(x == 2 and y == 0)
        x, y = d & e
        self.assertTrue(x == 2 and y == 0)

if __name__ == '__main__':  
    unittest.main()