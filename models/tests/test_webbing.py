import numpy as np
import pytest

from models.model_exception import StretchCurveException, WebbingException
from models.webbing import StretchCurve, Webbing, Segment


def test_stretch_curve_init():
    sc = StretchCurve([0, 1, 2], [0, 2, 4])
    assert sc.stretch[2] == 2
    assert sc.force[1] == 2


def test_stretch_curve_incorrect_raises_exception():
    with pytest.raises(StretchCurveException):
        not_same_length = StretchCurve([0, 1, 2], [0, 1])
    with pytest.raises(StretchCurveException):
        no_points = StretchCurve([0], [0])
    with pytest.raises(StretchCurveException):
        not_zero = StretchCurve([1, 2], [0, 1])
    with pytest.raises(StretchCurveException):
        not_increasing = StretchCurve([0, 1, 2], [0, 2, 1])
    with pytest.raises(StretchCurveException):
        not_increasing = StretchCurve([0, 3, 2], [0, 0.5, 1])


def test_webbing_init():
    wb = Webbing("paul", [0, 1, 2], [0, 2, 4], 1)
    assert wb.name == "paul"
    assert wb.weight == 1
    assert wb.stretch_curve.stretch[2] == 2
    assert wb.stretch_curve.force[1] == 2


def test_webbing_incorrect_raises_exception():
    with pytest.raises(WebbingException):
        no_name = Webbing("    ", [0, 1, 2], [0, 2, 4], 1)
    with pytest.raises(WebbingException):
        light = Webbing("Paul", [0, 1, 2], [0, 2, 4], 0)
    with pytest.raises(WebbingException):
        super_light = Webbing("Paul", [0, 1, 2], [0, 2, 4], -1)
    with pytest.raises(StretchCurveException):
        not_increasing = Webbing("Paul",[0, 3, 2], [0, 0.5, 1], 2)


def test_segment_init():
    se = Segment(np.array([10.0, 11, 12]), np.array([0.0, 1, 2]), 1)
    assert se.weight == 1


def test_segment_from_webbing():
    wb = Webbing("paul", [0, 10, 20], [0, 1, 2], 1)
    se = Segment.from_webbing(wb, 10)
    assert se.weight == 10
    assert se.length[0] == 10
    assert se.length[1] == 11
    assert se.length[2] == 12
    assert np.array_equal(se.force, wb.stretch_curve.force)
    assert se.force_from_length(11.5) == 1.5
    assert se.length_from_force(0.5) == 10.5
