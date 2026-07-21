import math

import cali


def test_euclidean_pythagorean():
    assert cali.euclidean((0, 0), (3, 4)) == 5


def test_euclidean_symmetric():
    assert cali.euclidean((1, 2), (5, 5)) == cali.euclidean((5, 5), (1, 2))


def test_euclidean_zero():
    assert cali.euclidean((7, 7), (7, 7)) == 0


def test_pixels_per_cm_default_reference():
    # 176 px measured across an 11 cm reference => 16 px/cm
    assert cali.pixels_per_cm(176) == 16


def test_pixels_per_cm_custom_reference():
    assert cali.pixels_per_cm(100, real_length_cm=10) == 10
