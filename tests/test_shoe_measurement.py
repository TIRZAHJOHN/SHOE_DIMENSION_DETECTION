import numpy as np

import shoe_measurement as sm


def test_euclidean_accepts_sequences():
    assert sm.euclidean([0, 0], [3, 4]) == 5


def test_euclidean_accepts_numpy_arrays():
    a = np.array([1.0, 1.0])
    b = np.array([4.0, 5.0])
    assert sm.euclidean(a, b) == 5


def test_curve_length_px_sums_segments():
    pts = [np.array([0, 0]), np.array([3, 0]), np.array([3, 4])]
    assert sm.curve_length_px(pts) == 7


def test_curve_length_px_single_point():
    assert sm.curve_length_px([np.array([2, 2])]) == 0


def test_pixels_to_cm_scales_by_a4_width():
    # a4 width 210 px, 21 cm reference => 0.1 cm/px; 100 px => 10 cm
    assert sm.pixels_to_cm(100, a4_width_px=210) == 10


def test_pixels_to_cm_custom_reference():
    assert sm.pixels_to_cm(50, a4_width_px=100, a4_width_cm=10) == 5
