class Channel:
    def __init__(self, name):
        self.name = name
        self.clients = {}

    def __repr__(self):
        return "<Channel name:%s clients:%s>" % (self.name, self.clients)

    def __str__(self):
        return "From str method of Channel: \nname is %s, \nclients is %s" % (self.name, self.clients)

    def getName(self):
        return "%s" % (self.name)
