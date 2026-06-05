
_missing = object()
def cache_unary_function_result(f):
    def f_wrapper(x, CACHE={}):
        r = CACHE.get(x, _missing)
        if r is _missing:
            r = f(x)
            CACHE[x] = r
        return r
    return f_wrapper


