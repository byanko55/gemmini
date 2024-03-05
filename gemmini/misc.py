import inspect
import warnings
import itertools

import numpy as np
from typing import Callable, Any, List, Optional, Tuple, Union
from math import sqrt, cos, sin, tan, atan, pi, inf, ceil, floor, exp, log, log10

COORDINATES = Union[Tuple, List, np.ndarray]

linear_seq = lambda *args: list(range(*args))
linear_ring = lambda *args: linear_seq(*args) + [0 if len(args) == 1 else args[0]]


def isNumber(n:Any) -> bool:
    return isinstance(n, (int, float, np.number))


def isNumberArray(a:Any) -> bool:
    if isinstance(a, np.ndarray) and len(a.shape) == 1 and isNumber(a[0]):
        return True
    
    if isinstance(a, (tuple, list)) and not isinstance(a[0], (tuple, list)) and isNumber(a[0]):
        return True
    
    return False


def isPoint(p:Any, dim:int = None) -> bool:
    if not isinstance(p, (tuple, list, np.ndarray)):
        return False
    
    if len(p) < 2 or len(p) > 3:
        return False
    
    if dim != None and len(p) != dim:
        return False
    
    return all(isNumber(i) for i in p)


def isPointSet(p:Any, dim:int = None) -> bool:
    if not isinstance(p, (list, np.ndarray)):
        return False
    
    if isinstance(p, list) and not isinstance(p[0], list):
        return False
    
    if isinstance(p[0], list) and (len(p[0]) < 2 or len(p[0]) > 3):
        return False
    
    if dim != None and len(p[0]) != dim:
        return False
    
    if isinstance(p, np.ndarray) :
        if len(p.shape) != 2 or (p.shape[1] < 2 or p.shape[1] > 3):
            return False
    
    return True


def isSame(a:object, b:object, bound=1e-6) -> bool:
    if isNumber(a) and isNumber(b):
        return abs(a-b) <= bound

    if isNumberArray(a) and isNumberArray(b):
        if len(a) != len(b):
            return False
        
        check = [abs(a[i]-b[i]) <= bound for i in range(len(a))]
        return bool(np.array(check).all())

    if isPoint(a) and isPoint(b):
        if len(a) != len(b):
            return False
        
        check = [abs(a[i]-b[i]) <= bound for i in range(len(a))]
        return bool(np.array(check).all())

    if isPointSet(a) and isPointSet(b):
        if len(a) != len(b):
            return False
        
        if len(a[0]) != len(b[0]):
            return False
        
        _a = np.array(a)
        _b = np.array(b)

        return len(np.where(np.abs(_a - _b) > bound)[0]) == 0

    return False


def inspect_args(func, aliases, error_tag, *args, **kwargs):
    spec = inspect.getfullargspec(func)

    for name, alias in aliases.items():
        if alias in kwargs:
            continue

        if alias not in kwargs and name in kwargs:
            kwargs[alias] = kwargs[name]
            continue

    arg_names = spec.args[1:] if spec.args[0] == 'self' else spec.args

    defaults = [None]*len(arg_names)

    if type(spec.defaults) != type(None):
        for i, v in enumerate(spec.defaults):
            defaults[i + len(arg_names) - len(spec.defaults)] = v

    for i, v in enumerate(defaults):
        arg = arg_names[i]

        if arg in kwargs:
            continue

        if len(args) > i:
            kwargs[arg] = args[i]
            continue

        if type(v) != type(None):
            kwargs[arg] = v
            continue

        raise ValueError(" \
            [ERROR] %s: Argument `%s` is missing \
            "%(error_tag, arg_names[i])
        )
    
    return kwargs


def alias(aliases):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            new_kwargs = inspect_args(func, aliases, func.__name__, *args, **kwargs)

            return func(**new_kwargs)
        return func_wrapper
    return decorator


def geminit(aliases={}):
    def decorator(init):
        def func_wrapper(self, *args, **kwargs):
            gem_type = self.__class__.__name__
            setattr(self, 'gem_type', gem_type)

            new_kwargs = inspect_args(init, aliases, gem_type, *args, **kwargs)

            return init(self, **new_kwargs)
        return func_wrapper
    return decorator


def _convert_tuple(a):
    if isinstance(a, list):
        if isinstance(a[0], list):
            return tuple(itertools.chain(*a))
        
        return tuple(a)
    
    if isinstance(a, np.ndarray):
        if len(a.shape) != 1:
            return tuple(a.flatten().tolist())
        
        return tuple(a.tolist())

    return a

def get_hash(*args, **kwargs):
    base = []
    
    for arg in args:
        base.append(_convert_tuple(arg))
        
    for k, v in kwargs.items():
        _v = _convert_tuple(v)
        base.append((k, _v))
        
    return hash(tuple(base))

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
                        [ERROR] %s: you can't pass the both `%s` and `%s` arguments. \
                        "%(gem_type, arg_name, _s)
                    )
            
                arg_name = _s
        elif isinstance(full_name, str) and full_name in kwargs:
            arg_name = full_name

        if type(abbr) != type(None) and arg_name != '':
            raise ValueError(" \
                [ERROR] %s: same flag used two times. \
                "%(gem_type)
            )
        
        if type(abbr) == type(None) and arg_name == '':
            raise ValueError("\
                [ERROR] %s: '%s' argument was not given. \
                "%(gem_type, full_name if type(full_name) == str else full_name[0])
            )
        
        v = abbr if type(abbr) != type(None) else kwargs[arg_name]
        res.append(v)
    
    if len(res) == 1:
        return res[0]

    return tuple(res)