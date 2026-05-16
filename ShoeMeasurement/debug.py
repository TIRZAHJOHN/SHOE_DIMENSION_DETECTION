import cv2

# Try changing CAP_BACKEND here (like CAP_MSMF, CAP_VFW)
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

if not cap.isOpened():
    print("❌ Camera not opened")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame")
        break

    cv2.imshow("Test Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
