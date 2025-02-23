import pytest
import numpy as np

from models.model_exception import SetUpException, SetUpComputeException
from models.setup import Setup
from models.webbing import Webbing


@pytest.fixture
def webbing_nylon():
    return Webbing('nylon', [0,10], [0,5], 60)


@pytest.fixture
def webbing_polyester():
    return Webbing('poly', [0,8], [0,8], 50)


@pytest.fixture
def webbing_dyneema():
    return Webbing('dyneema', [0,2], [0,1], 30)


@pytest.fixture
def setup(webbing_nylon, webbing_polyester):
    main = [(webbing_nylon, 50), (webbing_nylon, 50)]
    backup = [(webbing_polyester, 60), (webbing_polyester, 60)]
    connections = [True]
    return Setup(main, backup, connections)


def test_setup_init(setup):
    assert len(setup.main) == 2
    assert len(setup.backup) == 2
    assert len(setup.connections) == 1


def test_setup_raises_error_if_numbers_of_pieces_wrong(webbing_nylon, webbing_polyester):
    main_too_long = [(webbing_nylon, 50), (webbing_nylon, 50), (webbing_nylon, 50), (webbing_nylon, 50)]
    main = [(webbing_nylon, 50), (webbing_nylon, 50), (webbing_nylon, 50)]
    main_too_short = [(webbing_nylon, 50), (webbing_nylon, 50)]
    backup_too_long = [(webbing_polyester, 60), (webbing_polyester, 60), (webbing_polyester, 60), (webbing_polyester, 60)]
    backup = [(webbing_polyester, 60), (webbing_polyester, 60), (webbing_polyester, 60)]
    backup_too_short = [(webbing_polyester, 60), (webbing_polyester, 60)]
    connections_too_long = [True, True, True]
    breaks = [True, True, True]
    breaks_too_short = [True, True]
    connections = [True, True]
    connections_too_short = [True]
    with pytest.raises(SetUpException):
        setup = Setup(main_too_long, backup, connections, breaks)
    with pytest.raises(SetUpException):
        setup = Setup(main, backup_too_long, connections, breaks)
    with pytest.raises(SetUpException):
        setup = Setup(main, backup_too_short, connections)
    with pytest.raises(SetUpException):
        setup = Setup(main_too_short, backup, connections)
    with pytest.raises(SetUpException):
        setup = Setup(main, backup, connections_too_long, breaks)
    with pytest.raises(SetUpException):
        setup = Setup(main, backup, connections_too_short, breaks)
    with pytest.raises(SetUpException):
        setup = Setup(main, backup, connections, breaks_too_short)


def test_setup_get_cumul_lengths(webbing_nylon, webbing_polyester):
    main = [(webbing_nylon, 50), (webbing_nylon, 65), (webbing_nylon, 30), (webbing_nylon, 40)]
    backup = [(webbing_polyester, 60), (webbing_polyester, 35), (webbing_polyester, 75), (webbing_polyester, 48)]
    connections = [True, False, True]
    setup = Setup(main, backup, connections)
    assert setup.lengths == [0, 50, 105, 145, 185]
    with pytest.raises(SetUpComputeException):
        setup.get_index_along_main(190)
    sub_setup = setup.create_segment(100, 160)
    assert sub_setup.main == [(webbing_nylon, 15), (webbing_nylon, 30), (webbing_nylon, 15)]
    assert sub_setup.backup == [(webbing_polyester, 0), (webbing_polyester, 45 * 110 / 95), (webbing_polyester, 15*48/40)]
