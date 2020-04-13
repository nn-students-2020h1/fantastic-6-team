import unittest
from data import Data

class TestData(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def tearDown(self):
        self.data.string = ''

    def test_to_lower_case_string(self):
        self.data.to_lower_case('HELLO World!')
        self.assertEqual(self.data.string, 'hello world!')

    def test_to_lower_case_string(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case(5)

    def test_to_upper_case_string(self):
        self.data.to_upper_case('hello World!')
        self.assertEqual(self.data.string, 'HELLO WORLD!')

    def test_to_lower_case_string(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case(5)


if __name__ == '__main__':
    unittest.main()

# Add tests:
#.assertEqual()++ / .assertNotEqual()
#.assertTrue() / .assertFalse
#.assertIs() / .assertIsNot()
#.assertIn() / .assertNotIn()
#.assertIsNone() / .assertIsNotNone()
#.assertIsInstance() / .assertNotInstance()
#.assertWarns()
#.assertRaises()++