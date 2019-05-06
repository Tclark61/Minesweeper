import numpy as np
import pyautogui
pyautogui.FAILSAFE= True
import cv2
import math
import random

CONFIDENCE = 0.85

#Every box in minesweeper is a Node
class Node:
    def __init__(self, x, y, width, height):
        self.coords = (x,y)
        self.tuple = (x,y,width,height)

def probabilityChange(probabilityDelta, box):
    box.probability = box.probability + probabilityDelta
    if (box.probability > 1):
        box.probability = 1
    if (box.probability < 0):
        box.probability = 0
        
def changeNeighbors(board, clickIndex, boardInfo):
    #Check to see how many neighbors the clicked node has
    
    #Set a constant probabilityDelta for now
    probabilityDelta = 0.4
    #Check for neighbor behind
    if(clickIndex > 0):
        if(board[clickIndex - 1].isClicked == False):
            probabilityChange(probabilityDelta, board[clickIndex - 1])
    #Check for neighbor ahead
    if(clickIndex < (boardInfo[0] - 1)):
        if(board[clickIndex - 1].isClicked == False):
            probabilityChange(probabilityDelta, board[clickIndex + 1])
    #Check for neighbor above
    if(clickIndex >= boardInfo[1]):
        if(board[clickIndex - boardInfo[1]].isClicked == False):
            probabilityChange(probabilityDelta, board[clickIndex - boardInfo[1]])
    


    
def findCoordinates(imageLoc, scale, color):
    if scale == None:
        scale = 1
    image = cv2.imread(imageLoc, color)
    scaledImage = cv2.resize(image, None, fx = scale, fy = scale, interpolation = cv2.INTER_LANCZOS4)
    cv2.imwrite('scaledImage.png', scaledImage)
    return pyautogui.locateOnScreen('scaledImage.png', confidence = CONFIDENCE)

def determineScale(imageLoc, color):
    #Experimenting with being less safe, changed delta from 0.05 to 0.1 to half max computation time
    delta = 0.1
    scale = 5
    image = cv2.imread(imageLoc, 0)
    while(True):
        #If color is 0, search in greyscale. If 1, search in color
        newtemplate = findCoordinates(imageLoc, scale, color)
        if newtemplate != None:
            break
        scale = scale - delta
        if(scale < 0.5):
            print("No minesweeper template found")
            exit()
    
    return scale

def playGame(board, scale, boardInfo):
    lowestProb = 100
    lowestProbIndex = -1
    while(findCoordinates('oFace.png', scale, 1) != None or findCoordinates('happyFace.png', scale, 1) != None):
        for i in range(0, boardInfo[0]):
            if(board[i].probability == 1 and board[i].isClicked == False):
                print("Found a bomb at " + str(i) + ", box is unclicked: " + str(board[i].isClicked))
                pyautogui.click(pyautogui.center(board[lowestProbIndex].tuple), button='right')
                board[i].isClicked = True
            if board[i].probability < lowestProb and board[i].isClicked == False:
                lowestProb = board[i].probability
                lowestProbIndex = i
        pyautogui.click(pyautogui.center(board[lowestProbIndex].tuple), button='left')
        lowestProb = 100
        board[lowestProbIndex].isClicked = True
        changeNeighbors(board, i, boardInfo)
        print("Clicked the " + str(lowestProbIndex) + " box, it had probability " + str(board[lowestProbIndex].probability))
        
    if findCoordinates('XFace.png', scale, 1) != None:
        print("Game Over :(")
        exit()
    else:
        print("You won! Congratulations!")
    
def main():
    scale = determineScale('template.png', 0)
    #Loading Corner and resizing it to the correct size
    cornergui = findCoordinates('corner.png', scale, 0)
    if(cornergui == None):
        cornerscale = determineScale('corner.png', 0)
        cornergui = findCoordinates('corner.png', cornerscale, 0)
        if(cornergui == None):
            print("Corner could not be found. What did you do wrong this time?")
            exit()
    #Find thickness of border & bottomrightmost coordinate
    box = findCoordinates('template.png', scale, 0)
    botrightcoord = (cornergui[0] + box[2], cornergui[1] + box[3])
    
    #Calculate the dimensions of the board without the border
    #Image tuples are (left, top, width, height)
    topleftcoord = (box[0], box[1])
    botleftcoord = (box[0], botrightcoord[1])
    toprightcoord = (botrightcoord[0], box[1])

    totalWidth = botrightcoord[0] - botleftcoord[0]
    totalHeight = botrightcoord[1] - toprightcoord[1]
    numboxeswide = int(round((totalWidth-box[2])/box[2] + 1))
    numboxestall = int(round((totalHeight-box[3])/box[3] + 1))
    numboxes = numboxeswide*numboxestall
    boardInfo = [numboxes,numboxeswide, numboxestall]
    xCoord = box[0]
    yCoord = box[1]
    board = []
    print("Please enter the number of bombs: ")
    bombs = input()
    for i in range(0,numboxes):
        xCoord = box[0] + (box[2]*(i%numboxeswide))
        yCoord = box[1] + (box[3]*math.trunc(i/numboxeswide))
        board.append(Node(xCoord, yCoord,box[2],box[3]))
        #board[i].probability = bombs/numboxes
        board[i].probability = random.random()
        board[i].isClicked = False
        # pyautogui.click(pyautogui.center(board[i].tuple), button='left')
        # if(findCoordinates('oFace.png', scale, 1) == None and findCoordinates('happyFace.png', scale, 1) == None):
            # print("We couldn't find O Face")
            # break

    playGame(board, scale, boardInfo)

if __name__ == '__main__':
    main()



# Quick maffs: boxwidth * x = (total width - boxwidth)
#              x = (totalwidth-boxwidth) / boxwidth