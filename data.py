"""Lesson 8. TDD. Класс с тестовым покрытием"""

from warnings import warn


class Data:
    """Example class with some string methods"""
    def __init__(self):
        self.string = ''  # str
        self.number = None  # int
        self.bool = None  # bool

    def to_upper_case(self, s):
        """Transforms string <s> to upper case"""
        if isinstance(s, str):
            self.string = s.upper()
        else:
            raise TypeError("Doesn't support this data type.")

    def to_lower_case(self, s):
        """Transforms string <s> to lower case"""
        if isinstance(s, str):
            self.string = s.lower()
        else:
            raise TypeError("Doesn't support this data type.")

    def find_index_of_object(self, s, target):
        """Checks if string <s> contains string <target>"""
        if isinstance(s, str) and isinstance(target, str):
            if s.count(target) <= 1:
                self.number = s.find(target)
            else:
                warn(f"It's better not to use the method, because {target}"
                     f' exists in {s} more than one time.', UserWarning)
        else:
            raise TypeError("Doesn't support this data type.")

    def ends_with(self, s, target):
        """Checks if string <s> ends with string <target>"""
        if isinstance(s, str) and isinstance(target, str):
            self.bool = s.endswith(target)
        else:
            raise TypeError("Doesn't support this data type.")
