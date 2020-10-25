class ProcessTimeoutDto():
    def __init__(self,
                 pid=None,
                 pname=None,
                 past=None,
                 isTimeout=None):
        self.pid = pid
        self.pname = pname
        self.past = past
        self.isTimeout = isTimeout

    def __getitem__(self, item):
        if item == 'pid':
            return self.pid
        if item == 'pname':
            return self.pname
        elif item == 'past':
            return self.past
        elif item == 'isTimeout':
            return self.isTimeout