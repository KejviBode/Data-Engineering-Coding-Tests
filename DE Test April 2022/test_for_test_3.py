import pytest
from test_3 import sum_current_time


def test_valid_time():
    assert sum_current_time("21:21:21") == 63
    assert sum_current_time("01:02:03") == 6
    assert sum_current_time("00:00:00") == 0


def test_invalid_time():
    with pytest.raises(ValueError):
        sum_current_time("99:12:12")
    with pytest.raises(ValueError):
        sum_current_time("12:99:00")
    with pytest.raises(ValueError):
        sum_current_time("12:12:99")
    with pytest.raises(ValueError):
        sum_current_time("qwertyui")
    with pytest.raises(TypeError):
        sum_current_time("qwer:qer:qwer")
