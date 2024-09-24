import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Capture frame-by-frame
ret, frame = cap.read()

# Save the captured frame as an image file
cv2.imwrite('webcam_photo.jpg', frame)

# Release the capture
cap.release()

print("Image captured and saved as 'webcam_photo.jpg'")