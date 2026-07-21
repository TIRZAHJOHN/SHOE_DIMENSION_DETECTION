import os
import sys

import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shoe_utils import euclidean, load_image

image_path = r"C:\Users\tirza\OneDrive\Desktop\SHOE\ShoeMeasurement\WhatsAppImage2025-07-01at12.37.42_a025ecbd.jpg"
scale_percent = 30  # 🪄 Resize image to 30% of original size

points = []

def click_event(event, x, y, flags, param):
    global img_display
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img_display, (x, y), 5, (0, 0, 255), -1)
        if len(points) == 2:
            px_dist = euclidean(points[0], points[1])
            cv2.line(img_display, points[0], points[1], (0, 255, 0), 2)
            mid = ((points[0][0] + points[1][0]) // 2, (points[0][1] + points[1][1]) // 2)
            cv2.putText(img_display, f"{px_dist:.2f} px", mid, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            pixels_per_cm = px_dist / 11  # Real-life length = 11 cm
            print(f"📏 Pixel distance = {px_dist:.2f} → So pixels_per_cm = {pixels_per_cm:.2f}")
            cv2.imshow("Calibration", img_display)

# 💡 Load and resize to make it smaller on screen
img_display = load_image(image_path, scale_percent)

cv2.imshow("Calibration", img_display)
cv2.setMouseCallback("Calibration", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
