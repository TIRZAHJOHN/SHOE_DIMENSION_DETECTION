import os

from shoe_utils import KEYPOINTS_NEEDED, euclidean, load_labelme_points, polyline_length

# === CONFIGURATION ===
json_folder = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Dataset"
px_per_cm = 1680 / 21  # pixels per cm based on A4 width

print("\n📏 Shoe Measurements (in cm):\n")

for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        filepath = os.path.join(json_folder, filename)
        _, points = load_labelme_points(filepath)

        missing = [k for k in KEYPOINTS_NEEDED if k not in points]
        if missing:
            print(f"⚠️ Missing in {filename}: {missing}")
            continue

        # Compute distances
        heel_height_px = euclidean(points['heel_top'], points['heel_bottom'])
        instep_height_px = euclidean(points['instep_bottom'], points['instep_top'])
        toe_length_px = euclidean(points['toe_bottom'], points['toe_top'])
        curve_pts = [points['curve_1'], points['curve_2'], points['curve_3'], points['curve_4']]
        curve_length_px = polyline_length(curve_pts)

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
