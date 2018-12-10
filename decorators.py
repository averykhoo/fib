import time


def verbose(func):
    """
    Decorator to print function call details - parameters names and effective values
    """

    def wrapper(*func_args, **func_kwargs):
        # code = func.func_code  # py2
        code = func.__code__  # py3
        params = []
        for argNo in range(code.co_argcount):
            argName = code.co_varnames[argNo]
            argValue = func_args[argNo] if argNo < len(func_args) else func.func_defaults[
                argNo - code.co_argcount]
            params.append((argName, argValue))
        for argName, argValue in func_kwargs.items():
            params.append((argName, argValue))
        # params = [argName + ' = ' + repr(argValue) for argName, argValue in params]
        print(func.__name__ + ' ( ' + ', '.join(argName + ' = ' + repr(argValue) for argName, argValue in params) + ' )')
        print('  func_code.co_varnames =', code.co_varnames)
        print('  func_code.co_argcount =', code.co_argcount)
        print('  func_args =', func_args)
        print('  func_kwargs =', func_kwargs)
        t0 = time.time()
        out = func(*func_args, **func_kwargs)
        t1 = time.time()
        print('  returned =', str(out))
        print('  elapsed =', t1 - t0)
        return out

    return wrapper


def memodict(f):
    """
    Memoization decorator for a function taking a single argument
    """

    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret

    return memodict().__getitem__
