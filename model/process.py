
class Process:

    def __init__(self, name, id, size, pageId=0, lru_counter=-1):
        self.id = id
        self.size = size
        self.name = name
        self.pageId = pageId
        self.lru_counter = lru_counter

    def __str__(self):
        return f'(id:{self.id}, name:{self.name}, size:{self.size}' + (f', pageId:{self.pageId}' if self.pageId != 0 else '') + (f', lru_counter: {self.lru_counter}' if self.lru_counter != -1 else '') + ')'
