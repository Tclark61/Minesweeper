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
    scale = determineScale('template.png')
    #Loading Corner and resizing it to the correct size
    cornergui = findCoordinates('corner.png', scale)
    if(cornergui == None):
        cornerscale = determineScale('corner.png')
        cornergui = findCoordinates('corner.png', cornerscale)
        if(cornergui == None):
            print("Corner could not be found. What did you do wrong this time?")
            exit()
    print(cornergui)
    #Find thickness of border & bottomrightmost coordinate
    box = findCoordinates('template.png', scale)
    botrightcoord = (cornergui[0] + box[2], cornergui[1] + box[3])


    #Calculate the dimensions of the board without the border
    #Image tuples are (left, top, width, height)
    topleftcoord = (box[0], box[1])
    botleftcoord = (box[0], botrightcoord[1])
    toprightcoord = (botrightcoord[0], box[1])
    print(topleftcoord)
    print(toprightcoord)
    print(botleftcoord)
    print(botrightcoord)

    totalWidth = botrightcoord[0] - botleftcoord[0]
    totalHeight = botrightcoord[1] - toprightcoord[1]
    numboxeswide = round((totalWidth-box[2])/box[2] + 1)
    numboxestall = round((totalHeight-box[3])/box[3] + 1)
    numboxes = numboxeswide*numboxestall
    print(numboxes)

if __name__ == '__main__':
    main()



# Quick maffs: boxwidth * x = (total width - boxwidth)
#              x = (totalwidth-boxwidth) / boxwidth