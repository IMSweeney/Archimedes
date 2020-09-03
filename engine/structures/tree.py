import queue


class Node():
    def __init__(self, guid, data, parent=None):
        self.parent = parent
        self.guid = guid
        self.data = data
        self.children = []

    def add_element(self, guid, data, parentid=None):
        if self.guid == parentid:
            node = Node(guid, data, parent=self)
            self.children.append(node)
        else:
            for child in self.children:
                child.add_element(guid, data, parentid)

    def remove_element(self, guid):
        for i, child in enumerate(self.children):
            if child.guid == guid:
                self.children.pop(i)
                return
            child.remove_element(guid)

    def is_root(self):
        return not self.parent

    def update_data(self, guid, data):
        node = self.get_item(guid)
        if node:
            node.data = data
            return guid
        else:
            return False

    def get_item(self, guid):
        if self.guid == guid:
            return self
        for child in self.children:
            item = child.get_item(guid)
            if item:
                return item
        return False

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
        super().__init__(None, None)

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
    t.add_element(1, '1')
    t.add_element(2, '2')
    t.add_element(20, '20', parentid=2)
    t.add_element(10, '10', parentid=1)

    t.show_tree()

    # -- Test breadth first
    s = []
    for n in t.breadth_first():
        s.append(n.guid)

    assert s == [1, 2, 10, 20]

    # s = []
    # for n in t.depth_first():
    #     s.append(n.guid)
    # assert s == [1, 2, 10, 20]

    # -- Test contains
    assert 10 in t

    # -- Test contains fail
    assert 30 not in t

    # -- Test update_data (and get item)
    t.update_data(10, '10n')
    assert t.get_item(10).data == '10n'

    # -- Test remove_item
    t.remove_element(20)
    s = [n.guid for n in t.breadth_first()]
    assert set(s) == set([1, 2, 10])
