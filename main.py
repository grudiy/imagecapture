import cv2
import numpy
import time

video = cv2.VideoCapture(1)
# 0 - primary, 1 - secondary cam
time.sleep(1)

first_frame = None

while True:
    check, frame = video.read()
    # Convert frame to grey to decrease volume of data
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Add Gaussian Blur
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)
    # cv2.imshow("My Video", grey_frame_gau)

    if first_frame is None:
        first_frame = grey_frame_gau

    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Video from Camera. Press Q to Exit", thresh_frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
