import sys
import cv2
import math
import numpy as np

# === CONFIG ===
image_path = r"C:\Users\tirza\OneDrive\Desktop\SHOE\ShoeMeasurement\WhatsAppImage2025-07-01at12.37.42_a025ecbd.jpg"
pixels_per_cm = 15.86 # Set this based on your calibration (11 cm = 175 px)
scale_percent = 30  # Resize image to 30% of original

# === GLOBAL ===
line_points = []
curve_points = []

# === FUNCTIONS ===q
def euclidean(pt1, pt2):
    return math.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)

def distance_in_cm(pt1, pt2):
    return euclidean(pt1, pt2) / pixels_per_cm

def curve_length(points):
    total = 0
    for i in range(len(points) - 1):
        total += distance_in_cm(points[i], points[i + 1])
    return total

def mouse_events(event, x, y, flags, param):
    global img_display, line_points, curve_points

    if event == cv2.EVENT_LBUTTONDOWN:
        line_points.append((x, y))
        cv2.circle(img_display, (x, y), 4, (0, 255, 0), -1)
        if len(line_points) == 2:
            cv2.line(img_display, line_points[0], line_points[1], (255, 0, 0), 2)
            dist = distance_in_cm(line_points[0], line_points[1])
            mid = ((line_points[0][0] + line_points[1][0]) // 2,
                   (line_points[0][1] + line_points[1][1]) // 2)
            cv2.putText(img_display, f"{dist:.2f} cm", mid,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            line_points.clear()

    elif event == cv2.EVENT_RBUTTONDOWN:
        curve_points.append((x, y))
        cv2.circle(img_display, (x, y), 3, (255, 255, 0), -1)
        if len(curve_points) > 1:
            cv2.line(img_display, curve_points[-2], curve_points[-1], (0, 255, 255), 1)

        # Draw clean text box with curve length
        if len(curve_points) > 2:
            # Clear old text area
            cv2.rectangle(img_display, (10, 5), (300, 40), (255, 255, 255), -1)
            curve = curve_length(curve_points)
            cv2.putText(img_display, f"Curve: {curve:.2f} cm", (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)

# === MAIN ===
img = cv2.imread(image_path)
if img is None:
    print(f"❌ Image not found: {image_path}", file=sys.stderr)
    sys.exit(1)

# Resize to smaller size
w = int(img.shape[1] * scale_percent / 100)
h = int(img.shape[0] * scale_percent / 100)
img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
img_display = img.copy()

cv2.namedWindow("Shoe Tool")
cv2.setMouseCallback("Shoe Tool", mouse_events)

print("🟢 Instructions:")
print("👉 Left click 2 points: straight distance")
print("👉 Right click 3+ points: curve distance")
print("👉 Press 'q' to quit")

while True:
    cv2.imshow("Shoe Tool", img_display)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
