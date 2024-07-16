import cv2

def test_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Test Frame', frame)
        cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
