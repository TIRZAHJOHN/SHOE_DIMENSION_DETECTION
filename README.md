# SHOE_DIMENSION_PREDICTION
# 👟 Shoe Measurement & Keypoint Detection System

## 📌 Project Overview

This project is an AI-powered shoe measurement system developed using **Python**, **YOLO Pose Estimation**, and **Computer Vision** techniques. The system detects important shoe keypoints from images and automatically calculates measurements such as:

* Heel Height
* Instep Height
* Toe Length
* Front Curve Length
* Shoe Length

The project uses a custom-trained YOLO pose model to identify keypoints on a shoe placed over an A4 sheet and converts pixel measurements into centimeters.

---

# 🚀 Features

✅ Automatic shoe keypoint detection
✅ Custom YOLO pose estimation model
✅ Accurate shoe measurement calculation
✅ Pixel-to-centimeter conversion using A4 scaling
✅ Visualization of detected keypoints
✅ JSON annotation support
✅ Supports custom shoe datasets

---

# 🛠️ Technologies Used

* Python
* OpenCV
* NumPy
* Ultralytics YOLO
* JSON
* Computer Vision
* Pose Estimation

---

# 📂 Project Structure

```plaintext
SHOE/
│
├── Dataset/
│   ├── image1.json
│   ├── image2.json
│   └── ...
│
├── Json dataset/
│   ├── image1.jpeg
│   └── ...
│
├── runs/
│   └── pose/
│       └── train/
│           └── weights/
│               └── best.pt
│
├── output_with_keypoints.jpg
├── measurement.py
└── README.md
```

---

# 🎯 Keypoints Used

The model detects the following keypoints:

```python
[
 'heel_top',
 'heel_mid',
 'heel_bottom',
 'instep_bottom',
 'instep_top',
 'toe_bottom',
 'toe_top',
 'curve_1',
 'curve_2',
 'curve_3',
 'curve_4'
]
```

---

# 📏 Measurements Calculated

## 1. Heel Height

Distance between:

* heel_top
* heel_bottom

## 2. Instep Height

Distance between:

* instep_bottom
* instep_top

## 3. Toe Length

Distance between:

* toe_bottom
* toe_top

## 4. Front Curve Length

Calculated using:

* curve_1
* curve_2
* curve_3
* curve_4

## 5. Shoe Length

Distance between:

* heel_back
* toe_tip

---

# ⚙️ Installation

## Step 1: Clone the Repository

```bash
git clone <repository-link>
cd SHOE
```

## Step 2: Install Required Libraries

```bash
pip install ultralytics
pip install opencv-python
pip install numpy
```

---

# ▶️ How to Run

## Run Measurement from JSON Files

```bash
python measurement.py
```

## Run YOLO Prediction

```bash
python predict.py
```

---

# 🧠 Model Training

The YOLO pose estimation model was trained using custom shoe keypoint annotations.

Training command:

```bash
yolo pose train data=data.yaml model=yolov8n-pose.pt epochs=100 imgsz=640
```

---

# 📸 Output Example

```plaintext
✅ Prediction completed. Key measurements:

Heel Height       : 6.45 cm
Shoe Length       : 27.82 cm
Front Curve Length: 13.67 cm
```

---

# 🔍 Working Process

1. Input shoe image placed on an A4 sheet
2. YOLO model detects shoe keypoints
3. Distances are measured in pixels
4. Pixel values converted into centimeters
5. Final measurements displayed to the user

---

# 📈 Future Enhancements

* Real-time webcam measurement
* Mobile application integration
* 3D shoe analysis
* Automatic shoe size recommendation
* Improved measurement accuracy

---

# 👩‍💻 Author

Developed by Tirzah John

---

# 📄 License

This project is developed for educational and research purposes.
