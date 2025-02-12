from models.webbing import Webbing


class Connection(bool):
    pass


class Setup:
    def __init__(self, main: [Webbing], backup: [Webbing], connections: [bool]):
        # each segment and whether there is a main/backup connection after it.
        self.main = main
        self.backup = backup
        self.connections = connections
