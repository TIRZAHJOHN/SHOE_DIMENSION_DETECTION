"""Shared utilities for the shoe dimension detection project.

Consolidates helpers that were previously duplicated across the various
scripts (distance/curve math, LabelMe JSON parsing, image loading and the
list of keypoints used by the pose model).
"""

import json
import math

# The 11 keypoints annotated for every shoe, in the order expected by the
# YOLO pose model.
KEYPOINTS_NEEDED = [
    'heel_top', 'heel_mid', 'heel_bottom',
    'instep_bottom', 'instep_top',
    'toe_bottom', 'toe_top',
    'curve_1', 'curve_2', 'curve_3', 'curve_4',
]


def euclidean(p1, p2):
    """Return the Euclidean distance between two 2D points.

    Works with any indexable points (tuples, lists or NumPy arrays).
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def polyline_length(points):
    """Return the total length of the polyline through ``points``."""
    return sum(euclidean(points[i], points[i + 1]) for i in range(len(points) - 1))


def load_labelme_points(json_path):
    """Load a LabelMe JSON file and return it plus a ``label -> point`` dict.

    Returns a ``(data, points)`` tuple where ``data`` is the parsed JSON and
    ``points`` maps each shape label to its first annotated point.
    """
    with open(json_path, 'r') as f:
        data = json.load(f)

    points = {}
    for shape in data.get('shapes', []):
        label = shape['label'].strip()
        points[label] = shape['points'][0]

    return data, points


def load_image(image_path, scale_percent=None):
    """Load an image with OpenCV, exiting with a message if it is missing.

    When ``scale_percent`` is given the image is resized to that percentage of
    its original dimensions.
    """
    import cv2

    img = cv2.imread(image_path)
    if img is None:
        print("❌ Image not found.")
        raise SystemExit(1)

    if scale_percent is not None:
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    return img
