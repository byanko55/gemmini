from gemmini.misc import *
from gemmini.plot import *
from gemmini.d2.line2D import Line2D

import unittest

class SelfTests(unittest.TestCase): 
    def line1(self):
        l = Line2D((1,0), slope=1.5)
        plot(l)

    def line2(self):
        l = Line2D((1,0), (2,2))
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


if __name__ == '__main__':  
    unittest.main()