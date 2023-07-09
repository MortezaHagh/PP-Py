
class TopNode(object):
    def __init__(self):
        self.key = 0
        self.ind = 0
        self.node = 0


class Open(object):
    def __init__(self, top_node):
        self.list = [top_node]
        self.count = 1


class Start(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.key = 0
        self.node = 0


class Sol(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dirs = 0
        self.nodes = 0
        self.proc_time = 0
