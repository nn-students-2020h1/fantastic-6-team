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
            self.number = s.find(target)
        else:
            raise TypeError('Doesn\'t support this data type.')
