import os
import json
import shutil
import random
import sys

# === PATHS ===
json_folder = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset"
output_image_train = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset\YOLODataset\images\train"
output_label_train = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset\YOLODataset\labels\train"
output_image_val = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset\YOLODataset\images\val"
output_label_val = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset\YOLODataset\labels\val"

def log_error(message):
    print(message, file=sys.stderr)

# Create folders if not exist
for path in [output_image_train, output_label_train, output_image_val, output_label_val]:
    os.makedirs(path, exist_ok=True)

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

# === LOAD AND PROCESS ===
if not os.path.isdir(json_folder):
    log_error(f"❌ JSON folder not found: {json_folder}")
    sys.exit(1)

json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
random.shuffle(json_files)
split_idx = int(0.8 * len(json_files))

had_errors = False

for idx, json_file in enumerate(json_files):
    json_path = os.path.join(json_folder, json_file)
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        log_error(f"❌ Failed to read {json_file}: {e}")
        had_errors = True
        continue

    image_name = data.get('imagePath')
    if not image_name:
        log_error(f"⚠️ Skipping {json_file}: no 'imagePath' field")
        had_errors = True
        continue
    image_path = os.path.join(json_folder, image_name)

    if not os.path.exists(image_path):
        log_error(f"⚠️ Skipping {json_file}: Image file missing")
        had_errors = True
        continue

    width = data.get('imageWidth', 1)
    height = data.get('imageHeight', 1)

    try:
        label_dict = {shape['label']: shape['points'][0] for shape in data.get('shapes', [])}
    except (KeyError, IndexError, TypeError) as e:
        log_error(f"❌ Malformed shape data in {json_file}: {e}")
        had_errors = True
        continue
    kpts = []

    skip = False
    for kp in keypoints_needed:
        if kp in label_dict:
            x, y = normalize(label_dict[kp], width, height)
            kpts.extend([x, y, 1])
        else:
            log_error(f"⚠️ Skipping {image_name}: Missing keypoint '{kp}'")
            skip = True
            break

    if skip or len(kpts) != 33:
        had_errors = True
        continue

    label_line = "0 " + " ".join(map(str, kpts))

    # Save to train or val
    if idx < split_idx:
        dst_img = output_image_train
        dst_lbl = output_label_train
    else:
        dst_img = output_image_val
        dst_lbl = output_label_val

    txt_name = os.path.splitext(image_name)[0] + ".txt"
    try:
        shutil.copy(image_path, os.path.join(dst_img, image_name))
        with open(os.path.join(dst_lbl, txt_name), 'w') as f:
            f.write(label_line + "\n")
    except OSError as e:
        log_error(f"❌ Failed to write outputs for {image_name}: {e}")
        had_errors = True
        continue

print("✅ All valid JSONs converted and saved into train/val folders!")

if had_errors:
    sys.exit(1)
