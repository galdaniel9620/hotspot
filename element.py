class Element :

    def __init__(self, id, node1, node2, node3) :
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.is_hotspot = False
        self.value = 0
        self.neighbors = set()
