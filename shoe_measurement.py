import sys
from ultralytics import YOLO
import cv2
import numpy as np

def log_error(message):
    print(message, file=sys.stderr)

# 1. Load your trained model (update with your best model path)
model_path = r"C:\Users\tirza\runs\pose\train\weights\best.pt"
try:
    model = YOLO(model_path)
except Exception as e:
    log_error(f"❌ Failed to load model from {model_path}: {e}")
    sys.exit(1)

# 2. Load a shoe image placed over A4 sheet
img_path = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Json dataset\image1.jpeg"
img = cv2.imread(img_path)
if img is None:
    log_error(f"❌ Could not read image: {img_path}")
    sys.exit(1)

# 3. Run prediction
results = model(img)

# 4. Save and show prediction image
annotated_img = results[0].plot()  # image with keypoints
if not cv2.imwrite("output_with_keypoints.jpg", annotated_img):
    log_error("❌ Failed to write output_with_keypoints.jpg")
    sys.exit(1)
cv2.imshow("Prediction", annotated_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 5. Check if keypoints are detected
if results[0].keypoints is None or len(results[0].keypoints.xy[0]) < 10:
    log_error("❌ No keypoints detected. Please check the image or retrain the model.")
    sys.exit(1)

# 6. Get keypoints
keypoints = results[0].keypoints.xy[0].cpu().numpy()

# 7. Assign keypoints in order (based on your training)
try:
    (
        heel_top, heel_bottom, heel_back, heel_front,
        toe_start, toe_tip,
        curve1, curve2, curve3, curve4
    ) = keypoints[:10]
except ValueError as e:
    log_error(f"❌ Unexpected number of keypoints ({len(keypoints)}): {e}")
    sys.exit(1)

# 8. Function to find distance between 2 points
def euclidean(p1, p2):
    return np.linalg.norm(p1 - p2)

# 9. Measure in pixels
heel_height_px = euclidean(heel_top, heel_bottom)
shoe_length_px = euclidean(heel_back, toe_tip)
curve_points = [curve1, curve2, curve3, curve4]
curve_length_px = sum(euclidean(curve_points[i], curve_points[i + 1]) for i in range(len(curve_points) - 1))

# 10. Convert pixel distances to cm (assuming A4 width = 21cm)
a4_width_px = img.shape[1]
scale = 21 / a4_width_px  # cm per pixel

heel_height_cm = heel_height_px * scale
shoe_length_cm = shoe_length_px * scale
curve_length_cm = curve_length_px * scale

# 11. Show results
print("\n✅ Prediction completed. Key measurements:")
print(f"Heel Height       : {heel_height_cm:.2f} cm")
print(f"Shoe Length       : {shoe_length_cm:.2f} cm")
print(f"Front Curve Length: {curve_length_cm:.2f} cm")
