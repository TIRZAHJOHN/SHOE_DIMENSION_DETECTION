import json
import math

import pytest

import measure_shoes as ms


def test_distance_horizontal():
    assert ms.distance([0, 0], [3, 0]) == 3


def test_distance_pythagorean():
    assert ms.distance([0, 0], [3, 4]) == 5


def test_distance_is_symmetric():
    assert ms.distance([1, 2], [4, 6]) == ms.distance([4, 6], [1, 2])


def test_distance_same_point_is_zero():
    assert ms.distance([2, 5], [2, 5]) == 0


def _shape(label, point):
    return {"label": label, "points": [point]}


def test_extract_points_filters_unknown_labels_and_strips():
    data = {
        "shapes": [
            _shape(" heel_top ", [1, 1]),
            _shape("heel_bottom", [1, 5]),
            _shape("random_label", [9, 9]),
        ]
    }
    points = ms.extract_points(data)
    assert points == {"heel_top": [1, 1], "heel_bottom": [1, 5]}
    assert "random_label" not in points


def test_extract_points_handles_missing_shapes_key():
    assert ms.extract_points({}) == {}


def test_missing_keypoints_reports_all_when_empty():
    assert ms.missing_keypoints({}) == ms.keypoints_needed


def test_missing_keypoints_empty_when_complete():
    complete = {k: [0, 0] for k in ms.keypoints_needed}
    assert ms.missing_keypoints(complete) == []


def _full_points():
    return {
        "heel_top": [0, 0],
        "heel_mid": [0, 5],
        "heel_bottom": [0, 10],
        "instep_bottom": [10, 0],
        "instep_top": [10, 8],
        "toe_bottom": [20, 0],
        "toe_top": [20, 6],
        "curve_1": [0, 0],
        "curve_2": [3, 0],
        "curve_3": [3, 4],
        "curve_4": [6, 4],
    }


def test_compute_measurements_values():
    m = ms.compute_measurements(_full_points(), scale=1)
    # heel_top->heel_bottom = 10
    assert m["heel_height"] == 10
    # instep 0->8 = 8
    assert m["instep_height"] == 8
    # toe 0->6 = 6
    assert m["toe_length"] == 6
    # curve: 3 + 4 + 3 = 10
    assert m["curve_length"] == 10


def test_compute_measurements_applies_scale_and_rounds():
    m = ms.compute_measurements(_full_points(), scale=3)
    assert m["heel_height"] == round(10 / 3, 2)


def test_compute_measurements_raises_on_missing_keypoint():
    points = _full_points()
    del points["curve_4"]
    with pytest.raises(KeyError):
        ms.compute_measurements(points, scale=1)


def test_main_prints_measurements(tmp_path, capsys):
    data = {"shapes": [_shape(k, v) for k, v in _full_points().items()]}
    (tmp_path / "image1.json").write_text(json.dumps(data))
    ms.main(folder=str(tmp_path))
    out = capsys.readouterr().out
    assert "image1" in out
    assert "Heel Height" in out


def test_main_reports_missing(tmp_path, capsys):
    data = {"shapes": [_shape("heel_top", [0, 0])]}
    (tmp_path / "bad.json").write_text(json.dumps(data))
    ms.main(folder=str(tmp_path))
    out = capsys.readouterr().out
    assert "Missing in bad.json" in out


def test_main_ignores_non_json(tmp_path, capsys):
    (tmp_path / "note.txt").write_text("not json")
    ms.main(folder=str(tmp_path))
    out = capsys.readouterr().out
    assert "note" not in out
