import unittest
from itertools import chain
from random import sample

from binarytree import *

SAMPLES_SIZE = 10
SLICE_SIZE = 5


class SortTestTree(unittest.TestCase):

    tree = BinarySearchTree()

    @classmethod
    def setUpClass(cls):

        cls.sorted_sample =  sample(range(0, SAMPLES_SIZE), SAMPLES_SIZE)
        cls.sorted_sample.sort()
        cls.almost_sorted_sample = list(chain(cls.sorted_sample[-SLICE_SIZE:],
                                              cls.sorted_sample[SLICE_SIZE:-SLICE_SIZE],
                                              cls.sorted_sample[:SLICE_SIZE]))

    def setUp(self):
        self.test_list = sample(range(0, SAMPLES_SIZE), SAMPLES_SIZE)
        self.expected_list = self.test_list[:]
        self.expected_list.sort()
        self.sorted_list = self.sorted_sample[:]
        self.almost_sorted_list = self.almost_sorted_sample[:]

    def test_sort_empty_list(self):
        data = []
        self.tree.insert(data)
        self.assertEqual(data, [])

    def test_sort_one_item_list(self):
        data = [1]
        self.tree.insert(data)
        self.assertEqual(data, [1])

    def test_sort_random_list(self):
        self.tree.insert(self.test_list)
        self.assertEqual(self.expected_list, self.test_list)

    def test_sort_sort_wrong_data(self):
        self.assertRaises(TypeError, self.tree.insert, "test")

    def test_sort_sort_sorted_list(self):
        self.tree.insert(self.sorted_list)
        self.assertEqual(self.sorted_list, self.sorted_sample)

    def test_sort_sort_almost_sorted_list(self):
        self.tree.insert(self.almost_sorted_list)
        self.assertEqual(self.sorted_sample, self.almost_sorted_list)


if __name__ == '__main__':
    unittest.main()
