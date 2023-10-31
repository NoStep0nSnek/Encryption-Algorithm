# https://mcsp.wartburg.edu/zelle/python/graphics/graphics/node3.html

from os import walk
import os

from threading import Thread
import winsound
#import keyboard  # using module keyboard
import tkinter as tk
#pip install graphics.py
from graphics import *
import msvcrt
import EncryptionAndDecryption

MainBoxW = 64

win = GraphWin(width = 550, height = 300) # create a window
#win.canvas.cords()
win.setBackground("white")
screenW = 110
screenH = 60
win.setCoords(0, screenH, screenW, 0) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)

Recent_Paths = [] # Search through "Recent Paths" file

# Draws plus button
# Draws minus button

# Draws text: "Enter encrypted folder path:"
pathText = Text(Point(MainBoxW/2,15), "Enter the path of the folder to encrypt:")
pathText.draw(win)

# Draws text entry box
textEntry = Entry(Point(MainBoxW/2,20),32)
textEntry.draw(win)
text = textEntry.getText()


# Draws text: "Enter password:"
pathText = Text(Point(MainBoxW/2,25), "Enter password:")
pathText.draw(win)

# Draws password entry box
PasswordTextEntry = Entry(Point(MainBoxW/2,30),32)
PasswordTextEntry.draw(win)
PasswordText = textEntry.getText()

# Generates folder selection border
border = Rectangle(Point(2,2), Point(MainBoxW-2, screenH - 2))
border.draw(win)




# Creates gen new folder box and text
checkBox_W_H = 2 # The width and height of the checkbox
newFolderCheckBox = Rectangle(Point(MainBoxW+2,5), Point(MainBoxW+2 + checkBox_W_H, 5 + checkBox_W_H))
newFolderCheckBox.setFill(color_rgb(20, 200, 20))
#newFolderBox.setOutline(color_rgb(0, 0, 0))
newFolderCheckBox.draw(win)

folderText = Text(Point(88,5+(checkBox_W_H/2)), "Generate a new folder upon\n decryption & Encryption?")
folderText.draw(win)

# Draws "Decrypt" & "Encrypt" Buttons
DecryptBox = Rectangle(Point(2 + 2, screenH - 4 - 6), Point(MainBoxW / 2 - 1, screenH - 4))
DecryptBox.setFill(color_rgb(150,190,255))
DecryptBox.draw(win)

decryptLabel = Text(Point(2 + (MainBoxW / 4), screenH - 4 - 3), "DECRYPT")
#decryptLabel.setFill(color_rgb(255,255,255))
decryptLabel.draw(win)

EncryptBox = Rectangle(Point(1 + (MainBoxW/2), screenH - 4 - 6), Point(MainBoxW - 4, screenH - 4))
EncryptBox.setFill(color_rgb(245, 245, 220))
EncryptBox.draw(win)

encryptLabel = Text(Point((MainBoxW)-(MainBoxW/4)-2, screenH - 4 - 3), "ENCRYPT")
#encryptLabel.setFill(color_rgb(255,255,255))
encryptLabel.draw(win)

#Plus_Button = Image(Point(10,10),)
#Plus_Button.draw(win)
#Minus_Button = Image()
#Minus_Button.draw(win)


# Draws progress bar Border
ProgressBarBorder = Rectangle(Point(64, 50), Point(screenW - 2, screenH - 2))
ProgressBarBorder.draw(win)

ProgressBarFill = 0
# Percent ranges from 0 to 1
def fillProgressBar(percent):
    global ProgressBarFill
    if ProgressBarFill != 0:
        ProgressBarFill.undraw()
        ProgressBarFill = 0

    if (ProgressBarFill == 0):
        diffW = 64 - (screenW- 2)
        print(diffW)
        ProgressBarFill = Rectangle(Point(64, 50), Point((-diffW * percent) + 64,screenH - 2))
        ProgressBarFill.setFill(color_rgb(20, 200, 20))
        ProgressBarFill.draw(win)

def checkForClick(mousePos, Obj):
    #mousePos = win.getMouse()
    if (mousePos.getX() > Obj.getP1().getX() and mousePos.getX() < Obj.getP2().getX() and mousePos.getY() > Obj.getP1().getY() and mousePos.getY() < Obj.getP2().getY()):
        return True
    else:
        return False

GenNewFolder = True

# Create missing paths (decrypted folder, encrypted folder) in case they are missing
writePath = ""
decryptPath = ""
def createMissingPaths(basePath):
    global writePath
    global decryptPath
    writePath = basePath + " - Encrypted"
    if not os.path.exists(writePath):
        os.makedirs(writePath)

    decryptPath = basePath + " - Decrypted"
    if not os.path.exists(decryptPath):
        os.makedirs(decryptPath)

code = "Password"
while True:
    mousePos = win.getMouse()
    if (checkForClick(mousePos, EncryptBox)):
        filepath = textEntry.getText()
        password = PasswordTextEntry.getText()
        createMissingPaths(filepath)
        EncryptionAndDecryption.clearContents(writePath) # Do not put this in the encrypt function or it will break it
        EncryptionAndDecryption.getFiles(filepath, writePath, True)
        EncryptionAndDecryption.encryptFolderNames(writePath, code)
        print("A")
    if (checkForClick(mousePos, DecryptBox)):
        filepath = textEntry.getText()
        password = PasswordTextEntry.getText()
        print("name", filepath[0:-12])
        createMissingPaths(filepath[0:-12])
        EncryptionAndDecryption.clearContents(decryptPath)
        EncryptionAndDecryption.getFiles(writePath, decryptPath, False)
        EncryptionAndDecryption.decryptFolderNames(decryptPath, code)
    if (checkForClick(mousePos, newFolderCheckBox)):
        GenNewFolder = not GenNewFolder
        if (GenNewFolder):
            newFolderCheckBox.setFill(color_rgb(200, 20, 20))
        else:
            newFolderCheckBox.setFill(color_rgb(20, 200, 20))
        print("A")

win.close()
