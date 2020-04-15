from warnings import warn
class Data(object):
    def __init__(self):
        self.string = ''  # str
        self.number = None  # int
        self.bool = None  # bool

    def to_upper_case(self, s):
        if isinstance(s, str):
            self.string = s.upper()
        else:
            raise TypeError('Doesn\'t support this data type.')

    def to_lower_case(self, s):
        if isinstance(s, str):
            self.string = s.lower()
        else:
            raise TypeError('Doesn\'t support this data type.')

    def find_index_of_object(self, s, target):
        if isinstance(s, str) and isinstance(target, str):
            if s.count(target) <= 1:
                self.number = s.find(target)
            else:
                warn(f'It\'s better not to use the method, because {target} exists in {s} more than one time.', UserWarning)
        else:
            raise TypeError('Doesn\'t support this data type.')

    def ends_with(self, s, target):
        if isinstance(s, str) and isinstance(target, str):
            self.bool = s.endswith(target)
        else:
            raise TypeError('Doesn\'t support this data type.')