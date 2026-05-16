import os
import json
import math

# === CONFIGURATION ===
json_folder = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset"
px_per_cm = 1680 / 21  # pixels per cm based on A4 width

# Your 11 keypoints
keypoints_needed = [
    'heel_top', 'heel_mid', 'heel_bottom',
    'instep_bottom', 'instep_top',
    'toe_bottom', 'toe_top',
    'curve_1', 'curve_2', 'curve_3', 'curve_4'
]

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

print("\n📏 Shoe Measurements (in cm):\n")

for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        filepath = os.path.join(json_folder, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)

        points = {}
        for shape in data.get('shapes', []):
            label = shape['label'].strip()
            if label in keypoints_needed:
                points[label] = shape['points'][0]

        missing = [k for k in keypoints_needed if k not in points]
        if missing:
            print(f"⚠️ Missing in {filename}: {missing}")
            continue

        # Compute distances
        heel_height_px = distance(points['heel_top'], points['heel_bottom'])
        instep_height_px = distance(points['instep_bottom'], points['instep_top'])
        toe_length_px = distance(points['toe_bottom'], points['toe_top'])
        curve_pts = [points['curve_1'], points['curve_2'], points['curve_3'], points['curve_4']]
        curve_length_px = sum(distance(curve_pts[i], curve_pts[i + 1]) for i in range(3))

        # Convert to cm
        heel_height_cm = round(heel_height_px / px_per_cm, 2)
        instep_height_cm = round(instep_height_px / px_per_cm, 2)
        toe_length_cm = round(toe_length_px / px_per_cm, 2)
        curve_length_cm = round(curve_length_px / px_per_cm, 2)

        # Print result
        print(f"🖼️ {filename.replace('.json', '')}")
        print(f"  • Heel Height       : {heel_height_cm} cm")
        print(f"  • Instep Height     : {instep_height_cm} cm")
        print(f"  • Toe Length        : {toe_length_cm} cm")
        print(f"  • Front Curve Length: {curve_length_cm} cm\n")
