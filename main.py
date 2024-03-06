import os

import cv2
import numpy
import time

import emailing_mock

import glob

video = cv2.VideoCapture(1)
# 0 - primary, 1 - secondary cam
time.sleep(1)

first_frame = None
count = 1
status_list = []


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


while True:
    status = 0
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
        # Detect contours coordinates
        x, y, w, h = cv2.boundingRect(contour)
        my_rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if my_rectangle.any():
            status = 1
            # Capture image
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        # Object left the frame
        emailing_mock.send_email(image_with_object)
        # send_email() slows down the process. Python is trying to finish this function first.
        # So we have somehow to process it at the same time while next operations are being done.

        # After sending image of object, to clean the folder
        clean_folder()

    cv2.imshow("Video from Camera. Press Q to Exit", frame)
    key = cv2.waitKey(1)
    # Exit if user press "q" button
    if key == ord('q'):
        break

video.release()
