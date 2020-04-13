from warnings import warn
class Data(object):
    def __init__(self):
        self.string = ''
        self.number = None

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

    def count_number_of_object(self, s, target):
        if isinstance(s, str):
            if s.count(target) <= 1:
                self.number = s.find(target)
            else:
                warn(f'It\'s better to use count_number_of_object function, because {target} exists in {s} more than one time.', UserWarning)
        else:
            raise TypeError('Doesn\'t support this data type.')
