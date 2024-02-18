import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as pth

import warnings
from math import sqrt, cos, sin, tan, pi, inf, log10
from typing import Callable, Any, List, Optional, Tuple, Union

COORDINATES = Union[Tuple, List, np.ndarray]

def assignArg(gem_type:str, list_abbrs:List[Any], list_full_names:List[str], kwargs):
    res = []
    
    for abbr, full_name in zip(list_abbrs, list_full_names):
        arg_name = ''

        if isinstance(full_name, list):
            for _s in full_name:
            
                if _s not in kwargs:
                    continue

                if arg_name != '':
                    raise ValueError(" \
                        [ERROR] %s: you can't pass the both `%s` and `%s` arguments' \
                        "%(gem_type, arg_name, _s)
                    )
            
                arg_name = _s
        elif isinstance(full_name, str) and full_name in kwargs:
            arg_name = full_name

        if abbr != None and arg_name != '':
            raise ValueError("[ERROR] %s: same flag used two times"%(gem_type))
        
        if abbr == None and arg_name == '':
            raise ValueError("\
                [ERROR] %s: '%s' argument was not given \
            "%(gem_type, full_name if type(full_name) == str else full_name[0]))
        
        v = abbr if abbr != None else kwargs[arg_name]
        res.append(v)
    
    if len(res) == 1:
        return res[0]

    return tuple(res)