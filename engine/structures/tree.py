class Node():
    def __init__(self, guid, data, parent=None):
        self.parent = parent
        self.guid = guid
        self.data = data
        self.children = []

    def add_element(self, guid, data, parentid):
        if self.guid == parentid:
            node = Node(guid, data, parent=self)
            self.children.append(node)
        for child in self.children:
            child.add_element(guid, data, parentid)

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
        self.data = None
        self.children = []

    def add_element(self, guid, data, parentid=None):
        if not parentid:
            node = Node(guid, data)
            self.children.append(node)
        super().add_element(guid, data, parentid)

    def __iter__(self):
        for child in self.children:
            for node in child:
                yield node
        # yield self
        # return DepthFirst(self.children)


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
    t.add_element(10, '10', parentid=2)

    t.show_tree()
    for e in t:
        print(e)

    print(10 in t)
