import os

import split_dataset as sd


def test_make_dirs_creates_expected_layout(tmp_path):
    base = str(tmp_path / "out")
    sd.make_dirs(base)
    for sub in ["images/train", "images/val", "labels/train", "labels/val"]:
        assert os.path.isdir(os.path.join(base, sub))


def test_make_dirs_is_idempotent(tmp_path):
    base = str(tmp_path / "out")
    sd.make_dirs(base)
    sd.make_dirs(base)  # should not raise
    assert os.path.isdir(os.path.join(base, "images/train"))


def test_list_images_only_jpeg(tmp_path):
    (tmp_path / "a.jpeg").write_text("")
    (tmp_path / "b.jpeg").write_text("")
    (tmp_path / "c.json").write_text("")
    (tmp_path / "d.png").write_text("")
    result = sorted(sd.list_images(str(tmp_path)))
    assert result == ["a.jpeg", "b.jpeg"]


def test_split_images_default_ratio():
    files = [f"{i}.jpeg" for i in range(10)]
    train, val = sd.split_images(files)
    assert len(train) == 8
    assert len(val) == 2
    assert train + val == files


def test_split_images_custom_ratio():
    files = [f"{i}.jpeg" for i in range(10)]
    train, val = sd.split_images(files, ratio=0.5)
    assert len(train) == 5
    assert len(val) == 5


def test_split_images_empty():
    assert sd.split_images([]) == ([], [])


def test_move_pair_copies_both_files(tmp_path):
    src = tmp_path / "src"
    out = tmp_path / "out"
    src.mkdir()
    sd.make_dirs(str(out))
    (src / "image1.jpeg").write_text("img")
    (src / "image1.json").write_text("{}")

    assert sd.move_pair("image1.jpeg", "train", str(src), str(out)) is True
    assert (out / "images/train/image1.jpeg").read_text() == "img"
    assert (out / "labels/train/image1.json").read_text() == "{}"


def test_move_pair_skips_when_json_missing(tmp_path, capsys):
    src = tmp_path / "src"
    out = tmp_path / "out"
    src.mkdir()
    sd.make_dirs(str(out))
    (src / "image1.jpeg").write_text("img")

    assert sd.move_pair("image1.jpeg", "train", str(src), str(out)) is False
    assert "Skipping image1.jpeg" in capsys.readouterr().out
    assert not (out / "images/train/image1.jpeg").exists()


def test_main_splits_and_copies(tmp_path, capsys):
    src = tmp_path / "src"
    out = tmp_path / "out"
    src.mkdir()
    for i in range(5):
        (src / f"image{i}.jpeg").write_text("img")
        (src / f"image{i}.json").write_text("{}")

    sd.main(src=str(src), out=str(out), ratio=0.8)

    n_train = len(os.listdir(out / "images/train"))
    n_val = len(os.listdir(out / "images/val"))
    assert n_train + n_val == 5
    assert "Split complete" in capsys.readouterr().out
