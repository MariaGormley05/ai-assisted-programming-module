"""Tests for stats.py. One of them fails, and that failure is the lab's task.

Fix the code so this file passes. Do not change what a test expects -- if a
test looks wrong to you, say so and explain why, rather than editing it.
"""
import pytest

from stats import mean, median, mode, spread


def test_mean():
    assert mean([1, 2, 3, 4]) == 2.5


def test_median_of_an_odd_length_list():
    assert median([3, 1, 2]) == 2


def test_median_of_an_even_length_list():
    # The middle of an even-length list is the mean of its two middle values.
    assert median([4, 1, 3, 2]) == 2.5


def test_mode_prefers_the_first_value_of_a_tie():
    assert mode([2, 1, 2, 1]) == 2


def test_spread():
    assert spread([5, 1, 9]) == 8


def test_empty_input_is_rejected():
    with pytest.raises(ValueError):
        mean([])
