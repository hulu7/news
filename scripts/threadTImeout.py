import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import time

def worker(x, y, z):
    time.sleep(15)

def collectMyResult(result):
    print("Got result {}".format(result))

def abortable_worker(func, *args, **kwargs):
    timeout = kwargs.get('timeout', None)
    p = ThreadPool(1)
    res = p.apply_async(func, args=args)
    try:
        out = res.get(timeout)  # Wait timeout seconds for func to complete.
        return out
    except multiprocessing.TimeoutError:
        print("Aborting due to timeout")
        p.terminate()
        raise

if __name__ == "__main__":
    pool = multiprocessing.Pool()
    featureClass = [[1, 2, 10], [1, 2, 10]] #list of arguments
    for f in featureClass:
      abortable_func = partial(abortable_worker, worker, timeout=3)
      pool.apply_async(abortable_func, args=f, callback=collectMyResult)
    pool.close()
    pool.join()