from GUI import GUI
from HAL import HAL
import rospy
import numpy as np

def turn_left():
    HAL.setV(0)
    HAL.setW(3.0)
    rospy.sleep(1.0)
    HAL.setW(0)

def turn_right():
    HAL.setV(0)
    HAL.setW(-3.0)
    rospy.sleep(1.0)
    HAL.setW(0)

while True:
    bumper_data = HAL.getBumperData()

    if bumper_data.state:
        if bumper_data.bumper == 0 or bumper_data.bumper == 1:
            turn_left()
        else:
            turn_right()
        HAL.setV(0.5)

    else:
        laser_data = HAL.getLaserData().values
        angle = np.argmax(laser_data)
        if laser_data[angle] > 1.0:
            HAL.setV(0.5)
            HAL.setW(0)
        else:
            HAL.setV(0)
            HAL.setW(0)

    rospy.sleep(0.05)



