class BaseSerializer:
    table = None
    
    def __init__(self, data: list[table] | table):
        self.data = data
        