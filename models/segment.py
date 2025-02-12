import numpy as np

from models.model_exception import SegmentException, SegmentComputeError
from models.webbing import Webbing, StretchCurve


class Segment:
    def __init__(self, lengths: [float], forces: [float], weight: float):
        self.lengths = lengths
        self.forces = forces
        self.weight = weight

    @classmethod
    def from_webbing(cls, webbing: Webbing, length: float):
        lengths = length * (1 + webbing.stretch_curve.stretch / 100)
        return cls(lengths, webbing.stretch_curve.force * 1.0, webbing.linear_weight*length)

    def force_from_length(self, length: float):
        if length < self.lengths[0]:
            return 0
        if length > self.lengths[-1]:
            raise SegmentComputeError("Length longer than modelisation curve")
        return np.interp(length, self.lengths, self.forces)

    def length_from_force(self, force: float):
        if force <= 0:
            return self.lengths[0]
        if force > self.forces[-1]:
            raise SegmentComputeError("Force higher than modelisation curve")
        return np.interp(force, self.forces, self.lengths)

    @classmethod
    def tape_two_segments(cls, main: 'Segment', backup: 'Segment') -> 'Segment':
        lengths = [l for l in sorted(set(main.lengths).union(backup.lengths)) if
                  l <= min(main.lengths[-1], backup.lengths[-1])]
        forces = [main.force_from_length(l) + backup.force_from_length(l) for l in lengths]
        return cls(np.array(lengths), np.array(forces), main.weight+backup.weight)

    @classmethod
    def join_two_segments(cls, left: 'Segment', right: 'Segment') -> 'Segment':
        forces = [f for f in sorted(set(left.lengths).union(right.lengths)) if
                  f <= min(left.forces[-1], right.forces[-1])]
        lengths = [left.length_from_force(f) + right.length_from_force(f) for f in forces]
        return cls(np.array(lengths), np.array(forces), left.weight+right.weight)
