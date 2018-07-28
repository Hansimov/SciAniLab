class People(object):
    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value):
        self._age = value
        print('New age is: {}!'.format(value))

x = People()

x.age = 1
x.age = 2