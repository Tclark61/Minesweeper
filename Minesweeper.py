import numpy as np
import pyautogui
import cv2

CONFIDENCE = 0.85

def findCoordinates(imageLoc):
    image = cv2.imread(imageLoc, 0)
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    return pyautogui.locateOnScreen(imageLoc, confidence = CONFIDENCE)

def determineScale(imageLoc):
    
    scale = 0.5
    image = cv2.imread(imageLoc, 0)
    scaledImage = cv2.resize(image, None, fx=scale, fy=scale, interpolation = cv2.INTER_LANCZOS4)
    cv2.imwrite('resizetemplate.png', scaledImage)
    while(True):
        scaledImage = cv2.resize(image, (0,0), fx=scale, fy=scale, interpolation = cv2.INTER_LANCZOS4)
        cv2.imwrite('resizetemplate.png', scaledImage)
        newtemplate = pyautogui.locateOnScreen('resizetemplate.png', confidence = CONFIDENCE)
        if newtemplate != None:
            break
        scale = scale + 0.05
        if(scale > 5):
            print("No minesweeper template found")
            exit()
    
    print("Final Scale: " + str(scale))
    return scale
    
def main():
    template = findCoordinates('template.png')
    scale = determineScale('template.png')

if __name__ == '__main__':
    main()