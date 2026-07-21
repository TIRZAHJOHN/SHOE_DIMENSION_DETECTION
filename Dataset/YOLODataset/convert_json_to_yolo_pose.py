import os
import json
import shutil
import random

# === PATHS ===
json_folder = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset"
output_image_train = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset\YOLODataset\images\train"
output_label_train = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset\YOLODataset\labels\train"
output_image_val = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset\YOLODataset\images\val"
output_label_val = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset\YOLODataset\labels\val"

# === 11 KEYPOINTS ===
keypoints_needed = [
    'heel_top', 'heel_mid', 'heel_bottom',
    'instep_bottom', 'instep_top',
    'toe_bottom', 'toe_top',
    'curve_1', 'curve_2', 'curve_3', 'curve_4'
]


# === NORMALIZE FUNCTION ===
def normalize(point, w, h):
    return round(point[0] / w, 6), round(point[1] / h, 6)


def build_label_dict(data):
    """Map each shape label to its first point from a LabelMe-style dict."""
    return {shape['label']: shape['points'][0] for shape in data.get('shapes', [])}


def build_keypoints(label_dict, width, height, keypoints=keypoints_needed):
    """Build the flat YOLO keypoint list ``[x, y, v, ...]``.

    Returns ``(kpts, missing)`` where ``missing`` is the first absent
    keypoint label, or ``None`` when all keypoints were found.
    """
    kpts = []
    for kp in keypoints:
        if kp in label_dict:
            x, y = normalize(label_dict[kp], width, height)
            kpts.extend([x, y, 1])
        else:
            return kpts, kp
    return kpts, None


def format_label_line(kpts, class_id=0):
    """Format a YOLO pose label line for a single instance."""
    return f"{class_id} " + " ".join(map(str, kpts))


def main(folder=json_folder):
    for path in [output_image_train, output_label_train, output_image_val, output_label_val]:
        os.makedirs(path, exist_ok=True)

    json_files = [f for f in os.listdir(folder) if f.endswith('.json')]
    random.shuffle(json_files)
    split_idx = int(0.8 * len(json_files))

    for idx, json_file in enumerate(json_files):
        json_path = os.path.join(folder, json_file)
        with open(json_path, 'r') as f:
            data = json.load(f)

        image_name = data.get('imagePath')
        image_path = os.path.join(folder, image_name)

        if not os.path.exists(image_path):
            print(f"⚠️ Skipping {json_file}: Image file missing")
            continue

        width = data.get('imageWidth', 1)
        height = data.get('imageHeight', 1)

        label_dict = build_label_dict(data)
        kpts, missing = build_keypoints(label_dict, width, height)

        if missing is not None or len(kpts) != 33:
            if missing is not None:
                print(f"⚠️ Skipping {image_name}: Missing keypoint '{missing}'")
            continue

        label_line = format_label_line(kpts)

        # Save to train or val
        if idx < split_idx:
            dst_img = output_image_train
            dst_lbl = output_label_train
        else:
            dst_img = output_image_val
            dst_lbl = output_label_val

        shutil.copy(image_path, os.path.join(dst_img, image_name))

        txt_name = os.path.splitext(image_name)[0] + ".txt"
        with open(os.path.join(dst_lbl, txt_name), 'w') as f:
            f.write(label_line + "\n")

    print("✅ All valid JSONs converted and saved into train/val folders!")


if __name__ == "__main__":
    main()
