import numpy as np
import pyautogui
import cv2

CONFIDENCE = 0.85

def findCoordinates(imageLoc, scale):
    if scale == None:
        scale = 1
    image = cv2.imread(imageLoc, 0)
    scaledImage = cv2.resize(image, None, fx = scale, fy = scale, interpolation = cv2.INTER_LANCZOS4)
    cv2.imwrite('scaledImage.png', scaledImage)
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    return pyautogui.locateOnScreen('scaledImage.png', confidence = CONFIDENCE)

def determineScale(imageLoc):
    
    scale = 5
    image = cv2.imread(imageLoc, 0)
    # scaledImage = cv2.resize(image, None, fx=scale, fy=scale, interpolation = cv2.INTER_LANCZOS4)
    # cv2.imwrite('resizetemplate.png', scaledImage)
    while(True):
        newtemplate = findCoordinates(imageLoc, scale)
        if newtemplate != None:
            break
        scale = scale - 0.05
        if(scale < 0.5):
            print("No minesweeper template found")
            exit()
    
    print("Final Scale: " + str(scale))
    return scale
    
def main():
    template = findCoordinates('template.png', None)
    scale = determineScale('template.png')
    #Loading Corner and resizing it to the correct size
    cornergui = findCoordinates('corner.png', scale)
    print(cornergui)
    cornerscale = determineScale('corner.png')
    cornergui = findCoordinates('corner.png', cornerscale)
    print(cornergui)

    #Find thickness of border & bottomrightmost coordinate
    #borderthickness = cornergui[2] - newtemplate[2]
    #botrightcoord = (cornergui[0] + newtemplate[2], cornergui[1] + newtemplate[3])


    #Calculate the dimensions of the board without the border
    #topleftcoord = (newtemplate[0], newtemplate[1])
   # botleftcoord = (newtemplate[0], botrightcoord[1])
    #toprightcoord = (botrightcoord[0], newtemplate[1])
    #print(topleftcoord)
    #print(toprightcoord)
    #print(botleftcoord)
    #print(botrightcoord)

if __name__ == '__main__':
    main()