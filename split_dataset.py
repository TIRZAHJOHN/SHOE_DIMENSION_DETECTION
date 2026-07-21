import os
import shutil
import random

# === CONFIG ===
source_dir = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset"
output_dir = os.path.join(source_dir, "YOLODataset")
split_ratio = 0.8  # 80% for training


def make_dirs(base):
    """Create the train/val image and label directories under ``base``."""
    for sub in ['images/train', 'images/val', 'labels/train', 'labels/val']:
        os.makedirs(os.path.join(base, sub), exist_ok=True)


def list_images(directory):
    """Return the ``.jpeg`` files found directly under ``directory``."""
    return [f for f in os.listdir(directory) if f.endswith('.jpeg')]


def split_images(image_files, ratio=split_ratio):
    """Split ``image_files`` into (train, val) lists using ``ratio``."""
    split_index = int(len(image_files) * ratio)
    return image_files[:split_index], image_files[split_index:]


def move_pair(image_name, target_split, src=source_dir, out=output_dir):
    base = os.path.splitext(image_name)[0]
    json_name = base + ".json"

    img_src = os.path.join(src, image_name)
    json_src = os.path.join(src, json_name)

    img_dst = os.path.join(out, f"images/{target_split}", image_name)
    json_dst = os.path.join(out, f"labels/{target_split}", json_name)

    if os.path.exists(img_src) and os.path.exists(json_src):
        shutil.copy(img_src, img_dst)
        shutil.copy(json_src, json_dst)
        return True
    else:
        print(f"⚠️ Skipping {image_name}: missing JSON or image")
        return False


def main(src=source_dir, out=output_dir, ratio=split_ratio):
    make_dirs(out)

    image_files = list_images(src)
    random.shuffle(image_files)

    train_images, val_images = split_images(image_files, ratio)

    for img in train_images:
        move_pair(img, 'train', src, out)

    for img in val_images:
        move_pair(img, 'val', src, out)

    print(f"✅ Split complete: {len(train_images)} train and {len(val_images)} val images")


if __name__ == "__main__":
    main()
