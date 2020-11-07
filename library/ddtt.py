import unittest
from ddt import ddt, data, unpack


@ddt
class MyTesting(unittest.TestCase):
    def setUp(self):
        print('this is the setUp')
    
    @data([1, 2, 3])
    def test_1(self, value):
        print(value)
    
    @data([3, 2, 1], [5, 3, 2], [10, 4, 6])
    @unpack
    def test_minus(self, a, b, expected):
        actual = int(a) - int(b)
        expected = int(expected)
        self.assertEqual(actual, expected)
    
    @data([2, 3], [4, 5])
    def test_compare(self, a, b):
        self.assertEqual(a, b)
    
    def tearDown(self):
        print('this is tearDown')


if __name__ == '__main__':
    unittest.main(verbosity=2)