from HAL import HAL
from GUI import GUI
import numpy as np
import cv2 as cv


kp = 0.005
ki = 0.0001
kd = 0.0001


prev_error = 0
error_sum = 0

while True:
    frame = HAL.getImage()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    mask = cv.inRange(hsv, lower_red, upper_red)

    
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        line_contour = max(contours, key=cv.contourArea)

        M = cv.moments(line_contour)
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            
            image_center = frame.shape[1] // 2
            error = cx - image_center

            
            p_control = kp * error
            error_sum += error
            i_control = ki * error_sum
            d_control = kd * (error - prev_error)
            prev_error = error

            steering = p_control + i_control + d_control

            
            HAL.setV(1)
            HAL.setW(-steering)

            
            cv.drawContours(frame, [line_contour], -1, (0, 255, 0), 2)
            cv.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    
    GUI.showImage(frame)
