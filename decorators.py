def verbose(func):
    """Decorator to print function call details - parameters names and effective values"""

    def wrapper(*func_args, **func_kwargs):
        print 'func_code.co_varnames =', func.func_code.co_varnames
        print 'func_code.co_argcount =', func.func_code.co_argcount
        print 'func_args =', func_args
        print 'func_kwargs =', func_kwargs
        params = []
        for argNo in range(func.func_code.co_argcount):
            argName = func.func_code.co_varnames[argNo]
            argValue = func_args[argNo] if argNo < len(func_args) else func.func_defaults[
                argNo - func.func_code.co_argcount]
            params.append((argName, argValue))
        for argName, argValue in func_kwargs.items():
            params.append((argName, argValue))
        params = [argName + ' = ' + repr(argValue) for argName, argValue in params]
        print(func.__name__ + ' ( ' + ', '.join(params) + ' )')
        return func(*func_args, **func_kwargs)

    return wrapper


def memodict(f):
    """ Memoization decorator for a function taking a single argument """

    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret

    return memodict().__getitem__
