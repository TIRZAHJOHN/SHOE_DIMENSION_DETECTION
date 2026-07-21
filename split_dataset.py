import os
import shutil
import random
import sys

# === CONFIG ===
source_dir = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset"
output_dir = os.path.join(source_dir, "YOLODataset")
split_ratio = 0.8  # 80% for training

def log_error(message):
    print(message, file=sys.stderr)

if not os.path.isdir(source_dir):
    log_error(f"❌ Source directory not found: {source_dir}")
    sys.exit(1)

# Create required directories
for sub in ['images/train', 'images/val', 'labels/train', 'labels/val']:
    os.makedirs(os.path.join(output_dir, sub), exist_ok=True)

# Get all image files (.jpeg)
image_files = [f for f in os.listdir(source_dir) if f.endswith('.jpeg')]
random.shuffle(image_files)

split_index = int(len(image_files) * split_ratio)
train_images = image_files[:split_index]
val_images = image_files[split_index:]

had_errors = False

# Helper to move files
def move_pair(image_name, target_split):
    global had_errors
    base = os.path.splitext(image_name)[0]
    json_name = base + ".json"

    img_src = os.path.join(source_dir, image_name)
    json_src = os.path.join(source_dir, json_name)

    img_dst = os.path.join(output_dir, f"images/{target_split}", image_name)
    json_dst = os.path.join(output_dir, f"labels/{target_split}", json_name)

    if os.path.exists(img_src) and os.path.exists(json_src):
        try:
            shutil.copy(img_src, img_dst)
            shutil.copy(json_src, json_dst)
        except OSError as e:
            log_error(f"❌ Failed to copy {image_name}: {e}")
            had_errors = True
    else:
        log_error(f"⚠️ Skipping {image_name}: missing JSON or image")
        had_errors = True

# Move training files
for img in train_images:
    move_pair(img, 'train')

# Move validation files
for img in val_images:
    move_pair(img, 'val')

print(f"✅ Split complete: {len(train_images)} train and {len(val_images)} val images")

if had_errors:
    sys.exit(1)
