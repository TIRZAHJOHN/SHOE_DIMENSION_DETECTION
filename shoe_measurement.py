import cv2
import numpy as np

model_path = r"C:\Users\tirza\runs\pose\train\weights\best.pt"
img_path = r"C:\Users\tirza\OneDrive\Desktop\SHOE\Json dataset\image1.jpeg"


# Function to find distance between 2 points
def euclidean(p1, p2):
    return np.linalg.norm(np.asarray(p1) - np.asarray(p2))


def curve_length_px(curve_points):
    """Sum of segment lengths along an ordered list of curve points."""
    return sum(euclidean(curve_points[i], curve_points[i + 1]) for i in range(len(curve_points) - 1))


def pixels_to_cm(px, a4_width_px, a4_width_cm=21):
    """Convert a pixel measurement to cm using the A4 sheet width as reference."""
    scale = a4_width_cm / a4_width_px  # cm per pixel
    return px * scale


def main():
    from ultralytics import YOLO

    # 1. Load your trained model (update with your best model path)
    model = YOLO(model_path)

    # 2. Load a shoe image placed over A4 sheet
    img = cv2.imread(img_path)

    # 3. Run prediction
    results = model(img)

    # 4. Save and show prediction image
    annotated_img = results[0].plot()  # image with keypoints
    cv2.imwrite("output_with_keypoints.jpg", annotated_img)
    cv2.imshow("Prediction", annotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 5. Check if keypoints are detected
    if results[0].keypoints is None or len(results[0].keypoints.xy[0]) < 10:
        print("❌ No keypoints detected. Please check the image or retrain the model.")
        return

    # 6. Get keypoints
    keypoints = results[0].keypoints.xy[0].cpu().numpy()

    # 7. Assign keypoints in order (based on your training)
    (
        heel_top, heel_bottom, heel_back, heel_front,
        toe_start, toe_tip,
        curve1, curve2, curve3, curve4
    ) = keypoints

    # 9. Measure in pixels
    heel_height_px = euclidean(heel_top, heel_bottom)
    shoe_length_px = euclidean(heel_back, toe_tip)
    curve_points = [curve1, curve2, curve3, curve4]
    curve_len_px = curve_length_px(curve_points)

    # 10. Convert pixel distances to cm (assuming A4 width = 21cm)
    a4_width_px = img.shape[1]

    heel_height_cm = pixels_to_cm(heel_height_px, a4_width_px)
    shoe_length_cm = pixels_to_cm(shoe_length_px, a4_width_px)
    curve_length_cm = pixels_to_cm(curve_len_px, a4_width_px)

    # 11. Show results
    print("\n✅ Prediction completed. Key measurements:")
    print(f"Heel Height       : {heel_height_cm:.2f} cm")
    print(f"Shoe Length       : {shoe_length_cm:.2f} cm")
    print(f"Front Curve Length: {curve_length_cm:.2f} cm")


if __name__ == "__main__":
    main()
