import numpy as np

from models.model_exception import StretchCurveException, WebbingException, SegmentException, SegmentComputeError, \
    SegmentJoinError


class StretchCurve:
    def __init__(self, stretches: [float], forces: [float]):
        self.stretch = np.array(stretches)
        self.force = np.array(forces)

        if len(self.force) != len(self.stretch):
            raise StretchCurveException("Stretch Values and Forces have to be float lists of the same length")
        if len(self.force) < 2:
            raise StretchCurveException("A stretch curve needs at least 2 points")
        if self.force[0] != 0 or self.stretch[0] != 0:
            raise StretchCurveException("A stretch curve starts from point (0,0)")
        if not np.all(np.diff(self.force) > 0):
            raise StretchCurveException("Forces in a stretch curve have to be increasing")
        if not np.all(np.diff(self.stretch) > 0):
            raise StretchCurveException("Stretches in a stretch curve have to be increasing")


class Webbing:
    def __init__(self, name: str, stretches: [float], forces: [float], weight: float):
        if weight <= 0:
            raise WebbingException("weight of webbing has to be positive")
        if name.strip() == "":
            raise WebbingException("Name should not be empty")
        self.stretch_curve = StretchCurve(stretches, forces)
        self.weight = weight
        self.name = name


class Segment:
    def __init__(self, length: np.ndarray, force: np.ndarray, weight: float):
        print(length.dtype)
        if length.dtype != np.float64 or force.dtype != np.float64:
            raise SegmentException("Input must be a numpy array of floats")
        if weight <= 0:
            raise SegmentException("weight of webbing has to be positive")
        if len(force) != len(length):
            raise SegmentException("Length Values and Forces have to be float lists of the same length")
        if len(force) < 2:
            raise SegmentException("A curve needs at least 2 points")
        if force[0] != 0 or length[0] <= 0:
            raise SegmentException("A stretch curve starts from point (0,l)")
        if not np.all(np.diff(force) > 0):
            raise SegmentException("Forces in a stretch curve have to be increasing")
        if not np.all(np.diff(length) > 0):
            raise SegmentException("length in a stretch curve have to be increasing")
        self.length = length
        self.force = force
        self.weight = weight

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
    def tape_main_and_backup(cls, main: 'Segment', backup: 'Segment') -> 'Segment':
        if main.length[0] < backup.length[0]:
            raise SegmentJoinError("Back-up shorter than Main")
        