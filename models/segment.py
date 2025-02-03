import numpy as np

from models.model_exception import SegmentException, SegmentComputeError
from models.webbing import Webbing


class Segment:
    def __init__(self, webbings: [Webbing], lengths: [float]):
        if len(webbings) != len(lengths):
            raise SegmentException("One length per webbing, each webbing has a length")
        if min(lengths <= 0):
            raise SegmentException("all lengths must be positive")
        self.lengths = np.array(lengths, float)
        self.total_length = sum(lengths)
        self.webbings = webbings

    @classmethod
    def from_webbing(cls, webbing: Webbing, length: float):
        weight = webbing.weight * length
        lengths = length * (1 + webbing.stretch_curve.stretch / 100)
        return cls(lengths, webbing.stretch_curve.force * 1.0, weight)

    def force_from_length(self, length: float):
        if length < self.length[0]:
            return 0
        if length > self.length[-1]:
            raise SegmentComputeError("Length longer than modelisation curve")
        return np.interp(length, self.length, self.force)

    def length_from_force(self, force: float):
        if force <= 0:
            return self.length[0]
        if force > self.force[-1]:
            raise SegmentComputeError("Force higher than modelisation curve")
        return np.interp(force, self.force, self.length)

    @classmethod
    def tape_two_segments(cls, main: 'Segment', backup: 'Segment') -> 'Segment':
        lengths = [l for l in sorted(set(main.length).union(backup.length)) if
                  l <= min(main.length[-1], backup.length[-1])]
        forces = [main.force_from_length(l) + backup.force_from_length(l) for l in lengths]
        return cls(np.array(lengths), np.array(forces), main.weight+backup.weight)

    @classmethod
    def join_two_segments(cls, left: 'Segment', right: 'Segment') -> 'Segment':
        forces = [f for f in sorted(set(left.length).union(right.length)) if
                  f <= min(left.force[-1], right.force[-1])]
        lengths = [left.length_from_force(f) + right.length_from_force(f) for f in forces]
        return cls(np.array(forces), np.array(lengths), np.array(forces), left.weight+right.weight)
