#-*- encoding:utf-8 -*-
memfile = open('/proc/meminfo')
while True:
    mem = memfile.readline()
    if 'MemTotal' in mem:
        print '%s' % mem,
    if 'MemFree' in mem:
        print '%s' % mem,
        break
memfile.close()