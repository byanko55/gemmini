
from gemplib.misc import *

class Geometry:
    def __init__(
        self,
        gem_type:str,
        **kwargs
    ):
        """
        Basic structure of gemplib geometry instance
        It also includes a collection of transformation operations. 

        Args:
            gem_type (str): explicit type of a geometric object
        """
        self.gem_type = gem_type
        
    