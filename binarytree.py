from random import randint


class Node:
    def __init__(self, value=None):
        self.value = value
        self.left_child = None
        self.right_child = None


class BinarySearchTree:
    def __init__(self):
        self.root = None  # root node

    def insert(self, value):  # add elements to the tree
        if not self.root:  # check if root exist
            self.root = Node(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, cur_node):
        # check if the new value < current node go LEFT otherwise RIGHT
        if value < cur_node.value:  # LEFT SIDE
            if cur_node.left_child == None:  # check if has node, if not create
                cur_node.left_child = Node(value)
            else:
                self._insert(value, cur_node.left_child)  # insert value go recurse left part
        elif value > cur_node.value:  # RIGHT SIDE
            if cur_node.right_child == None:
                cur_node.right_child = Node(value)
            else:
                self._insert(value, cur_node.right_child)  # go to next right child to insert a data recursively check
        else:
            print("value already in tree")

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, cur_node):
        if cur_node is not None:
            self._print_tree(cur_node.left_child)
            print(str(cur_node.value))
            self._print_tree(cur_node.right_child)

    def search(self, value):
        if self.root is not None:
            return self._search(value, self.root)

    def _search(self, value, cur_node):
        if value == cur_node.value:
            return True
        elif value < cur_node.value and cur_node.left_child is not None:
            return self._search(value, cur_node.left_child)
        elif value > cur_node.value and cur_node.right_child is not None:
            return self._search(value, cur_node.right_child)
        return False   #no found

    def search2(self, value):
        search_value = Iterator(value, self.root)
        for search in search_value:
            search()

class Iterator(BinarySearchTree):

    def __init__(self, value, cur_node):
        self.value = value
        self.cur_node = cur_node

    def __iter__(self):
        return self

    def __next__(self):
        if self.value == self.cur_node:
            return True
        if self.value < self.cur_node.value and self.cur_node.left_child is not None:
            return self._search(self.value, self.cur_node.left_child)
        elif self.value > self.cur_node.value and self.cur_node.right_child is not None:
            return self._search(self.value, self.cur_node.right_child)
        return False


if __name__ == '__main__':
    tree = BinarySearchTree()
    max_int_number = 100
    for _ in range(100):
        cur_elem = randint(0, max_int_number)
        tree.insert(cur_elem)


tree.print_tree()
print(tree.search(10))
print(tree.search2(2))  # does not work
