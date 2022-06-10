class Math2():

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.answer = 0

    def times(self):
        self.answer = self.a * self.b

    def div(self):
        if self.b == 0:
            raise ValueError('cannot div 0')
        else:
            self.answer = self.a / self.b

    def __str__(self):
        return 'Answer: {0}'.format(self.answer)
