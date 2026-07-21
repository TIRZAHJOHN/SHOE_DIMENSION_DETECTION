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


def extract_points(data, keypoints=keypoints_needed):
    """Return a mapping of keypoint label -> [x, y] from a LabelMe-style dict."""
    points = {}
    for shape in data.get('shapes', []):
        label = shape['label'].strip()
        if label in keypoints:
            points[label] = shape['points'][0]
    return points


def missing_keypoints(points, keypoints=keypoints_needed):
    """Return the list of required keypoints that are absent from ``points``."""
    return [k for k in keypoints if k not in points]


def compute_measurements(points, scale=px_per_cm):
    """Compute shoe measurements (in cm) from a keypoint mapping.

    Raises KeyError if a required keypoint is missing.
    """
    heel_height_px = distance(points['heel_top'], points['heel_bottom'])
    instep_height_px = distance(points['instep_bottom'], points['instep_top'])
    toe_length_px = distance(points['toe_bottom'], points['toe_top'])
    curve_pts = [points['curve_1'], points['curve_2'], points['curve_3'], points['curve_4']]
    curve_length_px = sum(distance(curve_pts[i], curve_pts[i + 1]) for i in range(3))

    return {
        'heel_height': round(heel_height_px / scale, 2),
        'instep_height': round(instep_height_px / scale, 2),
        'toe_length': round(toe_length_px / scale, 2),
        'curve_length': round(curve_length_px / scale, 2),
    }


def main(folder=json_folder):
    print("\n📏 Shoe Measurements (in cm):\n")

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)

            points = extract_points(data)

            missing = missing_keypoints(points)
            if missing:
                print(f"⚠️ Missing in {filename}: {missing}")
                continue

            m = compute_measurements(points)

            # Print result
            print(f"🖼️ {filename.replace('.json', '')}")
            print(f"  • Heel Height       : {m['heel_height']} cm")
            print(f"  • Instep Height     : {m['instep_height']} cm")
            print(f"  • Toe Length        : {m['toe_length']} cm")
            print(f"  • Front Curve Length: {m['curve_length']} cm\n")


if __name__ == "__main__":
    main()
