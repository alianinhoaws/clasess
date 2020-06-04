class Tree:

    class Node:
        def __init__(self):
            self.left = None
            self.right = None
            self.data = None

        def __str__(self):
            return 'Node [%s]' % self.data

    def __init__(self):
        self.root = None

    def __new_node(self, data):
        n = self.Node()
        n.data = data
        return n

    def build_from_lst(self, lst):

        self.root = self.__new_node(lst[0])
        self.root.left = self.__new_node(None)
        self.root.right = self.__new_node(None)
        leafs = [self.root.left, self.root.right]  # list of nodes on the current tree level
        next_leafs = []  # list of nodes on the next level
        counter = len(lst[1:]) - len(leafs)  #(9 - 2) need to create 7 node

        for item in lst[1:]:
            node = leafs.pop()
            node.data = item

            if counter > 0:
                node.left = self.__new_node(None)
                next_leafs.append(node.left)
                counter -= 1

            if counter > 0:
                node.right = self.__new_node(None)
                next_leafs.append(node.right)
                counter -= 1

            if len(leafs) == 0:
                leafs = next_leafs
                next_leafs = []

    def __str__(self):
        return self.root.__str__()


if __name__ == '__main__':
    t = Tree()
    t.build_from_lst(list(range(4, 11)))
    print(t)

# Implement binary search tree (left node < parent; right node > parent)
# BinaryTree()
# > input random integers
# < output BinaryTree().print() -> sorted integers 1,2,3,4,5,6
# Обход в глубину. (рекурсивно или спомощью циклов)

# **** for output implement inside class Tree iterator