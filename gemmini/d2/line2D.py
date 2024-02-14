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