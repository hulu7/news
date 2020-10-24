class ProcessTimeoutDto():
    def __init__(self,
                 pid=None,
                 past=None,
                 isTimeout=None):
        self.pid = pid
        self.past = past
        self.isTimeout = isTimeout

    def __getitem__(self, item):
        if item == 'pid':
            return self.pid
        elif item == 'past':
            return self.past
        elif item == 'isTimeout':
            return self.isTimeout