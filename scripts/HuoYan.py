#!/usr/bin/env python
# encoding:utf-8

import os
from fireWatcher import FireWatcher


class EventHandler(ProcessEvent):

    def process_IN_CREATE(self, event):
        print  "Create file: %s " % os.path.join(event.path, event.name)

    def process_IN_DELETE(self, event):
        print  "Delete file: %s " % os.path.join(event.path, event.name)

    def process_IN_MODIFY(self, event):
        print  "Modify file: %s " % os.path.join(event.path, event.name)

class FireWatcher():
    def Watch(self, path='.'):
        wm = WatchManager()
        mask = IN_DELETE | IN_CREATE | IN_MODIFY
        notifier = Notifier(wm, EventHandler())
        wm.add_watch(path, mask, auto_add=True, rec=True)
        print 'now starting monitor %s' % (path)
        while True:
            try:
                notifier.process_events()
                if notifier.check_events():
                    notifier.read_events()
            except KeyboardInterrupt:
                notifier.stop()
                break

if __name__ == "__main__":
    fire1 = FireWatcher()
    fire1.Watch('/home/dev/rsyncData/prd2/IP.txt')