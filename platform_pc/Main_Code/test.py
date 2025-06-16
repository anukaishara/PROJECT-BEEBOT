import cv2

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Error: Camera could not be opened")
else:
    ret, frame = cam.read()
    print("Frame read:", ret)
    if ret:
        ret2, buffer = cv2.imencode('.jpg', frame)
        print("JPEG encoding successful:", ret2)
        if ret2:
            with open("test_frame.jpg", "wb") as f:
                f.write(buffer)
            print("Frame saved as test_frame.jpg")
    cam.release()