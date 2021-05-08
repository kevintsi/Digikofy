class Coffee:
    def __init__(self,name, description,id=None):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return "{}".format(self.id)