import unittest
from data import Data

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def tearDown(self):
        self.data.string = ''

    def test_to_lower_case_string(self):
        self.data.to_lower_case('HELLO World!')
        self.assertEqual(self.data.string, 'hello world!')
        self.assertNotEqual(self.data.string, 'HELLO World!')
        self.assertTrue(self.data.string.islower())
        self.assertFalse(self.data.string.isupper())

    def test_to_lower_case_int(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case(5)

    def test_to_lower_case_float(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case(5.9)

    def test_to_lower_case_bool(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case(True)

    def test_to_lower_case_list(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case([2, 'something'])

    def test_to_lower_case_tupple(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case([2, 'something'])

    def test_to_lower_case_set(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case({4, 5})

    def test_to_lower_case_empty_list(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case([])

    def test_to_lower_case_none(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case(None)

    def test_to_lower_case_dict(self):
        with self.assertRaises(TypeError):
            self.data.to_lower_case({'hello': 'hi'})

    def test_to_upper_case_string(self):
        self.data.to_upper_case('HELLO World!')
        self.assertEqual(self.data.string, 'HELLO WORLD!')
        self.assertNotEqual(self.data.string, 'HELLO World!')
        self.assertTrue(self.data.string.islower())
        self.assertFalse(self.data.string.isupper())

    def test_to_upper_case_int(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case(5)

    def test_to_upper_case_float(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case(5.9)

    def test_to_upper_case_bool(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case(True)

    def test_to_upper_case_list(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case([2, 'something'])

    def test_to_upper_case_tupple(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case([2, 'something'])

    def test_to_upper_case_set(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case({4, 5})

    def test_to_upper_case_empty_list(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case([])

    def test_to_upper_case_none(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case(None)

    def test_to_upper_case_dict(self):
        with self.assertRaises(TypeError):
            self.data.to_upper_case({'hello': 'hi'})


if __name__ == '__main__':
    unittest.main()

# Add tests:
#.assertEqual()++ / .assertNotEqual()++
#.assertTrue()++ / .assertFalse++
#.assertIs() / .assertIsNot()
#.assertIn() / .assertNotIn()
#.assertIsNone() / .assertIsNotNone()
#.assertIsInstance() / .assertNotInstance()
#.assertWarns()
#.assertRaises()++