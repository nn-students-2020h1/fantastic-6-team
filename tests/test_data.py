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
    def test_to_lower_case_string_result_is_lowercase(self):
        self.data.to_lower_case('HELLO World!')
        self.assertTrue(self.data.string.islower())

    def test_to_lower_case_string_result_is_string(self):
        self.data.to_lower_case('HELLO World!')
        self.assertIs(type(self.data.string), str)

    def test_to_lower_case_string_result_is_not_uppercase(self):
        self.data.to_lower_case('HELLO World!')
        self.assertFalse(self.data.string.isupper())

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
    def test_to_upper_case_string_result_is_uppercase(self):
        self.data.to_upper_case('HELLO World!')
        self.assertEqual(self.data.string, 'HELLO WORLD!')

    def test_to_upper_case_string_result_is_string(self):
        self.data.to_upper_case('HELLO World!')
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

    # find_index_of_object methods tests
    def test_find_index_of_object_string(self):
        self.data.find_index_of_object('Hello, welcome to my world.', 'world')
        self.assertNotEqual(self.data.number, -1)

    def test_find_index_of_object_string_result_is_not_empty(self):
        self.data.find_index_of_object('Hello, welcome to my world.', 'world')
        self.assertNotIsInstance(self.data.number, str)

    def test_find_index_of_object_string_result_is_not_none(self):
        self.data.find_index_of_object('Hello, welcome to my world.', 'world')
        self.assertIsNotNone(self.data.number)

    def test_find_index_of_object_string__result_is_not_string(self):
        self.data.find_index_of_object('Hello, welcome to my world.', 'world')
        self.assertIsNot(type(self.data.number), str)


    def test_find_index_of_object_int(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object(5, 5)

    def test_find_index_of_object_float(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object(5.9, 5.9)

    def test_find_index_of_object_bool(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object(True, True)

    def test_find_index_of_object_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object([2, 'something'], 'something')

    def test_find_index_of_object_tupple(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object([2, 'something'], 'something')

    def test_find_index_of_object_set(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object({4, 5}, 4)

    def test_find_index_of_object_none(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object(None, None)

    def test_find_index_of_object_dict(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.find_index_of_object({'hello': 'hi'}, 'hello')

    def test_find_index_of_object_warnings(self):
        with self.assertWarns(UserWarning):
            self.data.find_index_of_object('Hello, welcome to my world, a great world.', 'world')

    # ends_with methods tests
    def test_ends_with_string_result_is_bool(self):
        self.data.ends_with('Hello, welcome to my world.', '.')
        self.assertIsInstance(self.data.bool, bool)

    def test_ends_with_string_target_is_in_input(self):
        self.data.ends_with('Hello, welcome to my world.', '.')
        self.assertIn('.', 'Hello, welcome to my world.')

    def test_ends_with_string_target_is_not_in_input(self):
        self.data.ends_with('Hello, welcome to my world.', '.')
        self.assertNotIn('!', 'Hello, welcome to my world.')

    def test_ends_with_int(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with(5, 5)

    def test_ends_with_float(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with(5.9, 9)

    def test_ends_with_bool(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with(True, 'e')

    def test_ends_with_list(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with([2, 'something'], 'something')

    def test_ends_with_tupple(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with([2, 'something'], 'something')

    def test_ends_with_set(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with({4, 5}, 5)

    def test_ends_with_none(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with(None, None)

    def test_ends_with_dict(self):
        with self.assertRaises(TypeError, msg='Data type of input data should be string'):
            self.data.ends_with({'hello': 'hi'}, 'hi')

if __name__ == '__main__':
    unittest.main()
