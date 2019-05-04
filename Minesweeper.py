import numpy as np
import pyautogui
import cv2

image = cv2.imread('template.png', 0)
screen = pyautogui.screenshot()
screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
template = pyautogui.locateOnScreen('template.png')

scalex = 0.5
scaley = 0.5
small = cv2.resize(image, None, fx=scalex, fy=scaley, interpolation = cv2.INTER_LANCZOS4)
cv2.imwrite('resizetemplate.png', small)

while(True):
    small = cv2.resize(image, (0,0), fx=scalex, fy=scaley, interpolation = cv2.INTER_LANCZOS4)
    cv2.imwrite('resizetemplate.png', small)
    newtemplate = pyautogui.locateOnScreen('resizetemplate.png', confidence = .85)
    if newtemplate != None:
        break
    scalex = scalex + 0.1
    scaley = scaley + 0.1
    if(scalex > 5):
        print("No minesweeper template found")
        exit()
    
print("Final Scale: " + str(scalex))
    