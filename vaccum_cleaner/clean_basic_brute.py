from GUI import GUI
from HAL import HAL
import time

while True:
    if HAL.getBumperData().state:
        HAL.setV(0)
        HAL.setW(0)
        HAL.setV(0)
        HAL.setW(3.0)
        time.sleep(1.0)
        HAL.setW(0)
        HAL.setV(0.5)
    else:
        HAL.setV(0.5)
        HAL.setW(0)
    time.sleep(0.05)


