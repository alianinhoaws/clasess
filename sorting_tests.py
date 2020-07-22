import unittest
from itertools import chain
from random import sample

from sorting import *


'''
https://pythonworld.ru/moduli/modul-unittest.html

https://techrocks.ru/2018/12/08/different-types-of-testing/

https://habr.com/ru/post/358950/

https://stokito.wordpress.com/2016/08/07/%D0%B2-%D1%87%D1%91%D0%BC-%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8C%D0%BD%D1%8B%D0%BC%D0%B8-%D0%B8%D0%BD%D1%82%D0%B5%D0%B3%D1%80/
'''

'''
testing from data perspective 

1. Empty data
2. Single data (e.x. for sort [7] == len 1)
3. Many len > 1
4. Wrong data type -> check exception raising

-------------------------------------------------
context dependency 

for sort context 
5. sorted data
6. almost sorted data 

'''


SAMPLES_SIZE = 3000
SLICE_SIZE = 5


class SortTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sorted_sample = sample(range(0, SAMPLES_SIZE), SAMPLES_SIZE)
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

    def test_bubble_sort_empty_list(self):
        data = []
        bubble_sort(data)
        self.assertEqual(data, [])

    def test_bubble_sort_one_item_list(self):
        data = [1]
        bubble_sort(data)
        self.assertEqual(data, [1])

    def test_bubble_sort_random_list(self):
        bubble_sort(self.test_list)
        self.assertEqual(self.test_list, self.expected_list)

    def test_bubble_sort_wrong_data(self):
        self.assertRaises(TypeError, bubble_sort, "test")

    def test_bubble_sort_sorted_list(self):
        bubble_sort(self.sorted_list)
        self.assertEqual(self.sorted_list, self.sorted_sample)

    def test_bubble_sort_almost_sorted_list(self):
        bubble_sort(self.almost_sorted_list)
        self.assertEqual(self.almost_sorted_list, self.sorted_sample)


    def test_merge_sort_empty_list(self):
        data = []
        merge_sort(data)
        self.assertEqual(data, [])

    def test_merge_sort_one_item_list(self):
        data = [1]
        merge_sort(data)
        self.assertEqual(data, [1])

    def test_merge_sort_wrong_data(self):
        self.assertRaises(TypeError, merge_sort, "test")

    def test_merge_sort_random_list(self):
        merge_sort(self.test_list)
        self.assertEqual(self.test_list, self.expected_list)

    def test_merge_sort_sorted_list(self):
        merge_sort(self.sorted_list)
        self.assertEqual(self.sorted_list, self.sorted_sample)

    def test_merge_sort_almost_sorted_list(self):
        merge_sort(self.almost_sorted_list)
        self.assertEqual(self.almost_sorted_list, self.sorted_sample)


    def test_insert_sort_empty_list(self):
        data = []
        insert_sort(data)
        self.assertEqual(data, [])

    def test_insert_sort_one_item_list(self):
        data = [1]
        insert_sort(data)
        self.assertEqual(data, [1])

    def test_insert_sort_wrong_data(self):
        self.assertRaises(TypeError, insert_sort, "test")

    def test_insert_sort_random_list(self):
        insert_sort(self.test_list)
        self.assertEqual(self.test_list, self.expected_list)

    def test_insert_sort_sorted_list(self):
        insert_sort(self.sorted_list)
        self.assertEqual(self.sorted_list, self.sorted_sample)

    def test_insert_sort_almost_sorted_list(self):
        insert_sort(self.almost_sorted_list)
        self.assertEqual(self.almost_sorted_list, self.sorted_sample)


    def test_choice_sort_empty_list(self):
        data = []
        choice_sort(data)
        self.assertEqual(data, [])

    def test_choice_sort_one_item_list(self):
        data = [1]
        choice_sort(data)
        self.assertEqual(data, [1])

    def test_choice_sort_wrong_data(self):
        self.assertRaises(TypeError, choice_sort, "test")

    def test_choice_sort_random_list(self):
        choice_sort(self.test_list)
        self.assertEqual(self.test_list, self.expected_list)

    def test_choice_sort_sorted_list(self):
        choice_sort(self.sorted_list)
        self.assertEqual(self.sorted_list, self.sorted_sample)

    def test_choice_sort_almost_sorted_list(self):
        choice_sort(self.almost_sorted_list)
        self.assertEqual(self.almost_sorted_list, self.sorted_sample)


    def tearDown(self):
        self.test_list = None
        self.expected_list = None

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()