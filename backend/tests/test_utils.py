import pytest

from backend.app.utils import add


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-5, -7) == -12


def test_add_mixed_types():
    assert add("4", 6) == 10
