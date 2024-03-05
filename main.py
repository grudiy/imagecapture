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

    if first_frame is None:
        first_frame = grey_frame_gau

    # Delta with first frame
    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)

    # Threshold of delta to make high contrast of pixels
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Add dilate to threshold
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # cv2.imshow("Video from Camera. Press Q to Exit", dil_frame)
    # Find contours of diff image
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("Video from Camera. Press Q to Exit", frame)
    key = cv2.waitKey(1)
    # Exit if user press "q" button
    if key == ord('q'):
        break

video.release()
