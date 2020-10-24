#coding=utf-8

import psutil
import os
import signal

print("----------------------------- show all processes info --------------------------------")
# show processes info
pids = psutil.pids()
for pid in pids:
    p = psutil.Process(pid)
    # get process name according to pid
    process_name = p.name()

    print("Process name is: %s, pid is: %s" % (process_name, pid))

print("----------------------------- kill specific process --------------------------------")
while True:
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
            # get process name according to pid
            process_name = p.name()
            print("process name: (%s)" % (process_name))
            # kill process "sleep_test1"
            if 'chrome' == process_name:
                print("kill specific process: name(%s)-pid(%s)" % (process_name, pid))
                os.kill(pid, signal.SIGKILL)
        except Exception as e:
            print e
exit(0)