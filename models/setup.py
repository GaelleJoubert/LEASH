from models.model_exception import SetUpException, SetUpComputeException
from models.webbing import Webbing


class Setup:
    def __init__(self, main: [(Webbing, float)], backup: [(Webbing, float)], connections: [bool], breaks: [bool] = []):
        # each segment (webbing type and length) and whether there is a main/backup connection after it.
        self.main = main
        self.backup = backup
        self.connections = connections
        self.breaks = breaks
        if len(self.breaks) == 0:
            self.breaks = [False for _ in self.main]
        if len(self.main) == 0:
            raise SetUpException("A setup need at least 1 segment")
        if len(self.main) != len(self.backup):
            raise SetUpException("Main and Backup need to have the same number of pieces")
        if len(self.main) != len(self.breaks):
            raise SetUpException("Number of segments and information if it breaks do not match")
        if len(self.connections) != len(self.main) - 1:
            raise SetUpException("There needs to be one connection less than the number of segments")
        self.lengths = [0]
        for m in self.main:
            self.lengths.append(self.lengths[-1] + m[1])

    def create_segment(self, l1: float, l2: float):
        if (l1 < 0) or (l1 > l2) or (l2 > self.lengths[-1]):
            raise SetUpComputeException(
                "Lengths to create a segment have to be in order and between 0 and the total setup length"
            )
        index_start = 0
        index_unconnected_start_start = 0
        while index_start < len(self.main) and self.lengths[index_start + 1] < l1:
            index_start += 1
            if self.connections[index_start - 1]:
                index_unconnected_start_start = index_start
        index_unconnected_start_end = index_start
        while index_unconnected_start_end < len(self.main) and not self.connections[index_unconnected_start_end - 1]:
            index_unconnected_start_end += 1

        index_end = index_start
        index_unconnected_end_start = index_unconnected_start_start
        while index_end < len(self.main) and self.lengths[index_end + 1] < l1:
            index_end += 1
            if self.connections[index_end - 1]:
                index_unconnected_end_start = index_end
        index_unconnected_end_end = index_end
        while index_unconnected_end_end < len(self.main) and not self.connections[index_unconnected_end_end - 1]:
            index_unconnected_end_end += 1
