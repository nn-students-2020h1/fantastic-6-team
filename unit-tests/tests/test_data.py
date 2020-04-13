import unittest
from data import Data

class TestData(unittest.TestCase):
    def test_something(self):
        self.data = Data()
    def tearDown(self):
        self.data.data_list = []


if __name__ == '__main__':
    unittest.main()

# Add tests:
#.assertEqual() / .assertNotEqual()
#.assertTrue() / .assertFalse
#.assertIs() / .assertIsNot()
#.assertIn() / .assertNotIn()
#.assertIsNone() / .assertIsNotNone()
#.assertIsInstance() / .assertNotInstance()
#.assertWarns()
#.assertRaises()