import math

import measure_shoe as msh


def test_euclidean_pythagorean():
    assert msh.euclidean((0, 0), (6, 8)) == 10


def test_distance_in_cm_uses_scale():
    # 10 px at 5 px/cm = 2 cm
    assert msh.distance_in_cm((0, 0), (6, 8), ppc=5) == 2


def test_distance_in_cm_default_scale():
    expected = 10 / msh.pixels_per_cm
    assert msh.distance_in_cm((0, 0), (6, 8)) == expected


def test_curve_length_sums_segments():
    pts = [(0, 0), (3, 0), (3, 4)]  # 3 px + 4 px = 7 px
    assert msh.curve_length(pts, ppc=1) == 7


def test_curve_length_single_point_is_zero():
    assert msh.curve_length([(1, 1)], ppc=1) == 0


def test_curve_length_empty_is_zero():
    assert msh.curve_length([], ppc=1) == 0
