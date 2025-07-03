from GUI import GUI
from HAL import HAL
import cv2
import numpy as np 

kp = 0.005

while True:
    frame = HAL.getImage()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        line_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(line_contour)

        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            image_center = frame.shape[1] // 2
            error = cx - image_center
            steering = kp * error

            cv2.drawContours(frame, [line_contour], -1, (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            HAL.setV(1)
            HAL.setW(-steering)

    GUI.showImage(frame)
