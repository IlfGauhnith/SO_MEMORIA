
class Process:

    def __init__(self, id, size, name):
        self.id = id
        self.size = size
        self.name = name

    def __str__(self):
        return f'({self.id}, {self.name}, {self.size})'
