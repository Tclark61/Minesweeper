import cv2
import numpy as np
import pyautogui
import cv2
image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
square = pyautogui.locateOnScreen('square.png')
print (square)