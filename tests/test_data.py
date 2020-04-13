import unittest
from data import Data


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.data = Data()

    def tearDown(self):
        self.data.string = ''
        self.data.number = None
        self.data.bool = None

    # to_lower_case methods tests
    def test_to_lower_case_string(self):
        self.data.to_lower_case('HELLO World!')
        self.assertEqual(self.data.string, 'hello world!')
        self.assertNotEqual(self.data.string, 'HELLO World!')
        self.assertTrue(self.data.string.islower())
        self.assertFalse(self.data.string.isupper())
        self.assertIsInstance(self.data.string, str)
        self.assertNotIsInstance(self.data.string, int)
        self.assertIsNotNone(self.data.string)
        self.assertIs(type(self.data.string), str)

    def test_to_lower_case_int(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case(5)

    def test_to_lower_case_float(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case(5.9)

    def test_to_lower_case_bool(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case(True)

    def test_to_lower_case_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case([2, 'something'])

    def test_to_lower_case_tupple(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case([2, 'something'])

    def test_to_lower_case_set(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case({4, 5})

    def test_to_lower_case_empty_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case([])

    def test_to_lower_case_none(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case(None)

    def test_to_lower_case_dict(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_lower_case({'hello': 'hi'})

    # to_upper_case methods tests
    def test_to_upper_case_string(self):
        self.data.to_upper_case('HELLO World!')
        self.assertEqual(self.data.string, 'HELLO WORLD!')
        self.assertNotEqual(self.data.string, 'HELLO World!')
        self.assertTrue(self.data.string.isupper())
        self.assertFalse(self.data.string.islower())
        self.assertIsInstance(self.data.string, str)
        self.assertNotIsInstance(self.data.string, int)
        self.assertIsNotNone(self.data.string)
        self.assertIs(type(self.data.string), str)

    def test_to_upper_case_int(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case(5)

    def test_to_upper_case_float(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case(5.9)

    def test_to_upper_case_bool(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case(True)

    def test_to_upper_case_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case([2, 'something'])

    def test_to_upper_case_tupple(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case([2, 'something'])

    def test_to_upper_case_set(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case({4, 5})

    def test_to_upper_case_empty_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case([])

    def test_to_upper_case_none(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case(None)

    def test_to_upper_case_dict(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.to_upper_case({'hello': 'hi'})

    # count_number_of_object_in_string methods tests
    def test_find_index_of_object_string(self):
        self.data.find_index_of_object('Hello, welcome to my world.', 'world')
        self.assertEqual(self.data.number, 21)
        self.assertNotEqual(self.data.number, -1)
        self.assertTrue(self.data.number == 21)
        self.assertFalse(self.data.number != 21)
        self.assertIsInstance(self.data.number, int)
        self.assertNotIsInstance(self.data.number, str)
        self.assertIsNotNone(self.data.number)
        self.assertIs(type(self.data.number), int)


    def test_find_index_of_object_int(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object(5)

    def test_find_index_of_object_float(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object(5.9)

    def test_find_index_of_object_bool(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object(True)

    def test_find_index_of_object_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object([2, 'something'])

    def test_find_index_of_object_tupple(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object([2, 'something'])

    def test_find_index_of_object_set(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object({4, 5})

    def test_find_index_of_object_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object([])

    def test_find_index_of_object_none(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object(None)

    def test_find_index_of_object_dict(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object({'hello': 'hi'})

    def test_find_index_of_object_warnings(self):
        with self.assertWarns(UserWarning):
            self.data.find_index_of_object('Hello, welcome to my world, a great world.', 'world')

    # ends_with methods tests
    def test_ends_with_string(self):
        self.data.ends_with('Hello, welcome to my world.', '.')
        self.assertEqual(self.data.bool, True)
        self.assertIsInstance(self.data.bool, bool)
        self.assertIn('.', 'Hello, welcome to my world.')
        self.assertIs(type(self.data.bool), bool)

    def test_ends_with_int(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with(5)

    def test_ends_with_float(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with(5.9)

    def test_ends_with_bool(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with(True)

    def test_ends_with_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with([2, 'something'])

    def test_ends_with_tupple(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with([2, 'something'])

    def test_ends_with_set(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with({4, 5})

    def test_ends_with_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with([])

    def test_ends_with_none(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with(None)

    def test_ends_with_dict(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with({'hello': 'hi'})

if __name__ == '__main__':
    unittest.main()

# Add tests:
# .assertEqual()++ / .assertNotEqual()++
# .assertTrue()++ / .assertFalse++
# .assertIs()++ / .assertIsNot()
# .assertIn()++ / .assertNotIn()
# .assertIsNone() / .assertIsNotNone() ++
# .assertIsInstance()++ / .assertNotInstance()++
# .assertWarns()++
# .assertRaises()++
