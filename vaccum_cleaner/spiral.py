import WebGUI
import HAL
import Frequency
import time

v = 1.0
w = 1.5          
w_min = 0.15     

while True:
    Frequency.tick()

    bumper = HAL.getBumperData()

    if bumper.state:
      
        HAL.setV(0)
        HAL.setW(1.5)
        time.sleep(1)

        
        w = 1.5
        continue

    
    HAL.setV(v)
    HAL.setW(w)

    
    w -= 0.005
    if w < w_min:
        w = w_min
