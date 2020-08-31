import queue


class Node():
    def __init__(self, guid, parent=None):
        self.parent = parent
        self.guid = guid
        self.children = []

    def add_element(self, guid, parentid):
        if self.guid == parentid:
            node = Node(guid, parent=self)
            self.children.append(node)
        for child in self.children:
            child.add_element(guid, parentid)

    def remove_element(self, guid):
        for child in self.children:
            if child.guid == guid:
                self.children.pop(child)
                return
            child.remove_element(guid)

    def __repr__(self):
        return 'id: {}, {} children'.format(
            self.guid, len(self.children))

    def show_tree(self, level=0):
        print('{}{}'.format("." * level, self.guid))
        for node in self.children:
            node.show_tree(level + 2)

    def __iter__(self):
        yield self
        for child in self.children:
            for node in child:
                yield node

    def __contains__(self, item):
        if self.guid == item:
            return True
        for child in self.children:
            if item in child:
                return True
        return False


class Tree(Node):
    def __init__(self):
        self.guid = -1
        self.children = []

    def add_element(self, guid, parentid=None):
        if not parentid:
            node = Node(guid)
            self.children.append(node)
        super().add_element(guid, parentid)

    def __iter__(self):
        for child in self.children:
            for node in child:
                yield node
        # yield self
        # return DepthFirst(self.children)

    def breadth_first(self):
        stack = queue.Queue()
        [stack.put(child) for child in self.children]
        while not stack.empty():
            node = stack.get()
            [stack.put(c) for c in node.children]
            yield node

    # def depth_first(self):
    #     stack = queue.Queue()
    #     [stack.put(child) for child in self.children]
    #     while not stack.empty():
    #         node = stack.get()
    #         [stack.put(c) for c in node.children]
    #         yield node


class DepthFirst():
    def __init__(self, elements):
        self.stack = elements.copy()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        node = self.stack.pop()
        self.stack += node.children
        return node

    def add_children(self, node):
        self.stack += node.children


if __name__ == '__main__':
    t = Tree()
    t.add_element(1)
    t.add_element(2)
    t.add_element(20, parentid=2)
    t.add_element(10, parentid=1)

    # t.show_tree()
    # for e in t:
    #     print(e)

    s = []
    for n in t.breadth_first():
        s.append(n.guid)
    assert s == [1, 2, 10, 20]

    # s = []
    # for n in t.depth_first():
    #     s.append(n.guid)
    # assert s == [1, 2, 10, 20]

    print(10 in t)
