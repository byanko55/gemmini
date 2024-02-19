from gemmini.misc import *
from gemmini.calc.coords import _isPoint, _isNumber

class Line2D:
    def __init__(
        self,
        p1:Tuple[float, float], 
        p2:Tuple[float, float] = None,
        slope:float = None,
        **kwargs
    ) -> None:
        """
        Infinite long straight line.
        Either p2 or slope has to be given.

        Args:
            p1, p2 (float, float): Points for the line to pass through.
            slope (float): The slope of the line.
        """

        gem_type = self.__class__.__name__

        if (p2 == None and slope == None) or (p2 != None and slope != None):
            raise ValueError("[ERROR] %s: Either p2 or slope has to be given"%(gem_type))
        
        if not _isPoint(p1, dim=2) or (p2 != None and not _isPoint(p2, dim=2)):
            raise ValueError(" \
                [ERROR] %s: check every points to conform the 2D format (x, y) \
            "%(gem_type))
        
        if slope != None and not _isNumber(slope):
            raise ValueError(" \
                [ERROR] %s: slope should be a numeric value \
            "%(gem_type))
        
        self.p1 = p1
        self.p2 = p2
        self.slope = slope

    def grad(self) -> float:
        """
        Return the gradient of the line
        """
        if self.slope != None:
            return self.slope

        if self.p1[0] == self.p2[0]:
            return inf

        return (self.p2[1]-self.p1[1])/(self.p2[0]-self.p1[0])
    
    def parallel(self, other) -> bool:
        """
        True, if two line are parallel
        """
        if type(other) != Line2D:
            raise ValueError("[Error] parallel: the input is not a `Line2D` object")

        return self.grad() == other.grad()
    
    def orthog(self, other) -> bool:
        """
        True, if two line are orthogonal
        """
        if type(other) != Line2D:
            raise ValueError("[Error] orthognal: the input is not a `Line2D` object")

        ga = self.grad()
        gb = other.grad()

        if (ga == inf and gb == 0) or (ga == 0 and gb == inf):
            return True
        
        if ga*gb == -1:
            return True
 
        return False
    
    def intersect(self, other) -> Tuple[float, float]:
        """
        Return the coordinates of intersection point of two lines
        """
        if self.parallel(other):
            warnings.warn("[WARN] intersect: given two line are parallel")
            return None
        
        ga = self.grad()
        gb = other.grad()

        rx = (ga*self.p1[0] - gb*self.p2[0] - self.p1[1] + self.p2[1])/(ga-gb)
        ry = ga*(rx - self.p1[0]) + self.p1[1]

        return rx, ry

    def __and__(self, other) -> Tuple[float, float]:
        return self.intersect(other)