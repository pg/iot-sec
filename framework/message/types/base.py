# Base Message format

class BaseMessage(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        return