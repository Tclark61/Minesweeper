import numpy as np
import pyautogui
import cv2

image = cv2.imread('template.png', 0)
screen = pyautogui.screenshot()
screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
template = pyautogui.locateOnScreen('template.png')

print (template)

small = cv2.resize(image, (0,0), fx=0.5, fy=0.5, interpolation = cv2.INTER_LANCZOS4)
cv2.imwrite('resizetemplate.png', small)
newtemplate = pyautogui.locateOnScreen('resizetemplate.png')

print (newtemplate)