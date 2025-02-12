import numpy as np

from models.model_exception import StretchCurveException, WebbingException


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
    def __init__(self, name: str, stretches: [float], forces: [float], linear_weight: float):
        if linear_weight <= 0:
            raise WebbingException("weight of webbing has to be positive")
        if name.strip() == "":
            raise WebbingException("Name should not be empty")
        self.stretch_curve = StretchCurve(stretches, forces)
        self.linear_weight = linear_weight
        self.name = name

