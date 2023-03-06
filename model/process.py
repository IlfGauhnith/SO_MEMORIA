
class Process:

    def __init__(self, name, id, size, pageId=0):
        self.id = id
        self.size = size
        self.name = name
        self.pageId = pageId

    def __str__(self):
        return f'(id:{self.id}, name:{self.name}, size:{self.size}' + (f', pageId:{self.pageId}' if self.pageId != 0 else '') + ')'
