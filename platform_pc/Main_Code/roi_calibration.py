import cv2

# Change this to your camera index if needed
CAMERA_INDEX = 0

# Store points
points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point {len(points)}: (x={x}, y={y})")
        # Draw a small circle where you clicked
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Camera', frame)
        if len(points) == 2:
            print("\nCopy these values to your config.py as:")
            print(f"'start_x': {points[0][0]}, 'start_y': {points[0][1]}, 'end_x': {points[1][0]}, 'end_y': {points[1][1]}")
            cv2.destroyAllWindows()

# Open camera
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Click on the TOP-LEFT corner, then the BOTTOM-RIGHT corner of your arena.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break
    cv2.imshow('Camera', frame)
    cv2.setMouseCallback('Camera', click_event)
    if cv2.waitKey(1) & 0xFF == 27 or len(points) == 2:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
