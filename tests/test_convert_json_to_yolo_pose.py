import json
import os

import convert_json_to_yolo_pose as conv


def test_normalize_basic():
    assert conv.normalize([50, 25], 100, 50) == (0.5, 0.5)


def test_normalize_rounds_to_six_places():
    x, y = conv.normalize([1, 1], 3, 3)
    assert x == round(1 / 3, 6)
    assert y == round(1 / 3, 6)


def test_build_label_dict_uses_first_point():
    data = {
        "shapes": [
            {"label": "heel_top", "points": [[1, 2], [9, 9]]},
            {"label": "toe_top", "points": [[3, 4]]},
        ]
    }
    assert conv.build_label_dict(data) == {"heel_top": [1, 2], "toe_top": [3, 4]}


def test_build_label_dict_empty():
    assert conv.build_label_dict({}) == {}


def _full_label_dict():
    return {k: [10, 20] for k in conv.keypoints_needed}


def test_build_keypoints_complete():
    kpts, missing = conv.build_keypoints(_full_label_dict(), 100, 200)
    assert missing is None
    assert len(kpts) == 33  # 11 keypoints * (x, y, visibility)
    # each keypoint: x=0.1, y=0.1, v=1
    assert kpts[0] == 0.1
    assert kpts[1] == 0.1
    assert kpts[2] == 1


def test_build_keypoints_reports_first_missing():
    ld = _full_label_dict()
    del ld["toe_top"]
    kpts, missing = conv.build_keypoints(ld, 100, 200)
    assert missing == "toe_top"
    # keypoints only accumulated up to the missing one
    assert len(kpts) < 33


def test_build_keypoints_visibility_flag_present():
    kpts, _ = conv.build_keypoints(_full_label_dict(), 100, 200)
    assert kpts[2::3] == [1] * 11


def test_format_label_line_default_class():
    line = conv.format_label_line([0.1, 0.2, 1])
    assert line == "0 0.1 0.2 1"


def test_format_label_line_custom_class():
    assert conv.format_label_line([0.5], class_id=3) == "3 0.5"


def test_main_generates_labels(tmp_path, monkeypatch, capsys):
    folder = tmp_path / "data"
    folder.mkdir()
    (folder / "image1.jpeg").write_text("img")
    data = {
        "imagePath": "image1.jpeg",
        "imageWidth": 100,
        "imageHeight": 200,
        "shapes": [{"label": k, "points": [[10, 20]]} for k in conv.keypoints_needed],
    }
    (folder / "image1.json").write_text(json.dumps(data))

    lbl_train = tmp_path / "lbl_train"
    lbl_val = tmp_path / "lbl_val"
    monkeypatch.setattr(conv, "output_image_train", str(tmp_path / "img_train"))
    monkeypatch.setattr(conv, "output_label_train", str(lbl_train))
    monkeypatch.setattr(conv, "output_image_val", str(tmp_path / "img_val"))
    monkeypatch.setattr(conv, "output_label_val", str(lbl_val))

    conv.main(folder=str(folder))

    # With a single file split_idx == 0, so the item lands in the val split.
    label_files = list(lbl_train.glob("*.txt")) + list(lbl_val.glob("*.txt"))
    assert len(label_files) == 1
    content = label_files[0].read_text().strip()
    assert content.startswith("0 ")
    assert len(content.split()) == 34  # class id + 33 keypoint values
    assert "All valid JSONs converted" in capsys.readouterr().out


def test_main_skips_missing_image(tmp_path, monkeypatch, capsys):
    folder = tmp_path / "data"
    folder.mkdir()
    data = {"imagePath": "gone.jpeg", "imageWidth": 100, "imageHeight": 100, "shapes": []}
    (folder / "x.json").write_text(json.dumps(data))

    for attr in ["output_image_train", "output_label_train", "output_image_val", "output_label_val"]:
        monkeypatch.setattr(conv, attr, str(tmp_path / attr))

    conv.main(folder=str(folder))
    assert "Image file missing" in capsys.readouterr().out
