import WebGUI
import HAL
import Frequency
import cv2 as cv
import numpy as np
# Enter sequential code!

kp = 0.005
ki = 0.0001
kd = 0.0001
prev_error = 0
error_sum = 0

while True:
    Frequency.tick()
    img = HAL.getImage()
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_red_low = np.array([0,100,100])
    lower_red_high = np.array([10,255,255])
    mask1 = cv.inRange(hsv,lower_red_low,lower_red_high)
    upper_red_low = np.array([160,100,100])
    upper_red_high = np.array([179,255,255])
    mask2 = cv.inRange(hsv,upper_red_low,upper_red_high)
    mask = mask1 | mask2
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        line_contour = max(contours,key=cv.contourArea)

        M = cv.moments(line_contour)

        if (M["m00"]!=0):
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            img_center = img.shape[1] // 2
            error = cx - img_center

            p_control = kp * error
            error_sum+=error
            i_control = ki*error_sum
            d_control = kd*(error-prev_error)
            prev_error = error
            steering = p_control + i_control + d_control 

            HAL.setV(1)
            HAL.setW(-steering)

            cv.drawContours(img,[line_contour],-1,[0,255,0],2)
            cv.circle(img, (cx, cy), 5, (0, 255, 0), -1)

    
    WebGUI.showImage(img)

    
    



