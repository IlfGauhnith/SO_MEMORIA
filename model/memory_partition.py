

class Partition:

    def __init__(self, size):
        self.size = size
        self.process = None
        self.fragmented = False

    def __str__(self):
        return f'(process:{self.process}, frag?{self.fragmented}' + (':' + str(self.size - self.process.size) + ', ' if self.fragmented else ', ') + 'size:' + f'{self.size})'
