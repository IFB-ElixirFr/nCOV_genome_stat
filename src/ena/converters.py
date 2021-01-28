class ThreeLetterCountryConverter:
    regex = '[a-zA-Z]{3}'

    def to_python(self, value):
        return str(value).upper()

    def to_url(self, value):
        return '%03s' % value
