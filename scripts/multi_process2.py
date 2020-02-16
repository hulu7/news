# -*- coding: UTF-8 -*-

from multiprocessing import Process
# We must import this explicitly, it is not imported by the top-level
# multiprocessing module.
from multiprocessing.pool import Pool
import time

from random import randint


class NoDaemonProcess(Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(Pool):
    Process = NoDaemonProcess

def sleepawhile(t):
    print("Sleeping %i seconds..." % t)
    time.sleep(t)
    print t

def work(num_procs):
    print("Creating %i (daemon) workers and jobs in child." % num_procs)
    pool = Pool(num_procs)
    for i in range(2):
        pool.apply_async(sleepawhile, args=(i,))

    # The following is not really needed, since the (daemon) workers of the
    # child's pool are killed when the child is terminated, but it's good
    # practice to cleanup after ourselves anyway.
    pool.close()
    pool.join()

def test():
    print("Creating 5 (non-daemon) workers and jobs in main process.")
    pool = MyPool(2)
    a = [1,1]
    pool.map(work, a)
    pool.close()
    pool.join()

if __name__ == '__main__':
    test()