import numpy as np
import pyautogui
import cv2

image = cv2.imread('square.png', 0)
screen = pyautogui.screenshot()
screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
square = pyautogui.locateOnScreen('square.png')

print (square)

small = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
newSquare = pyautogui.locateOnScreen(small)

print (newSquare)