# https://mcsp.wartburg.edu/zelle/python/graphics/graphics/node3.html

import shutil
from os import walk
import os

from threading import Thread
import winsound
#import keyboard  # using module keyboard
import tkinter as tk
#pip install graphics.py
from graphics import *
import msvcrt
#import EncryptionAndDecryption

wraparound = 255

def clamp(input, LB, UB):
    val = input
    if (input < LB):
        val = LB
    elif (input > UB):
        val = UB
    return val

key_depth = 5
def Encrypt_Data(str_to_encrypt, code, nums):
    encrypted = [0] * len(str_to_encrypt)
    values = [0] * len(code)
    for i in range(len(code)):
        total = 0
        for j in range(key_depth):
            total += j * len(code) + i
        values[i] = total
        #encrypted[i] = (letter ^ num)
        #encrypted[i] = (encrypted[i] ^ num)
    for i in range(len(str_to_encrypt)):
        try:
            letter = ord(str_to_encrypt[i])
        except:
            letter = (str_to_encrypt[i])
        num = values[i % len(values)]
        encrypted[i] = letter ^ num
    return encrypted

def errorMessage(str):
    errorText = textEntry(Point(2+(MainBoxW/2), 50), str)
    errorText.draw(win)
    # Delete after a few seconds

#def Decrypt_Data(str_to_decrypt, nums):

def rotate(textIn):
    a = 'a'
    c = 'a'
    a = textIn[0]
    for i in range(0,len(textIn)):
        textIn[c] = textIn[c + 1]
    textIn[len(textIn) - 1] = a
    return textIn

# Calculate the rcon used in key expansion
def rcon(charIn):
    c=1
    if(charIn == 0):
        return 0
    while ord(charIn) != 1:
        b = c & 0x80
        c <<= 1
        if(b == 0x80):
            c ^= 0x1b
        charIn = chr(ord(charIn) - 1)
    return c

def generate_Keys(code):
    keys = [0] * len(code) * key_depth
    for i in range(len(code)):
        for j in range(key_depth):
            if (j == 0):
                keys[i*key_depth+j] = ord(code[i])
            elif j == key_depth:
                keys[i*key_depth+j] = keys[i*key_depth+j-1] ^ ord(keys[i])
            else:
                keys[i*key_depth+j-1] &= ord(code[i])
    
    return keys

def remove_invalid_characters(str, invalid_chars):
    for i in range(len(str)):
        for j in range(len(invalid_chars)):
            if (str[i] == invalid_chars[j]):
                lowest_diff = 126
                lowest_diff_char = ""
                for k in range(32, 126):
                    diff = abs(ord(str[i]) - k)
                    if (diff < lowest_diff and k != ord(invalid_chars[j]) and k != (str[i])):
                        lowest_diff = diff
                        lowest_diff_char = chr(k)
                str[i] = lowest_diff_char
                break
    print("STR:",str)
    return str
                


def encryptFolderName(my_str, code):
    #generates nums
    nums = [2,4,8,16,32,64] # must not be above 128
    for i in range(len(nums)):
        num = nums[i % len(nums)]
        nums[i] = ord(code[i])//num

    encyrptedStr = [0] * len(my_str)
    for i in range(len(my_str)):
        num = nums[i % len(nums)]
        try:
            encyrptedStr[i] = clamp((ord(my_str[i]) ^ num), 64,126)
        except:
            encyrptedStr[i] = clamp(((my_str[i]) ^ num), 64,126)
    bufferList = []
    for i in range(len(encyrptedStr)):
        bufferList.append(chr(encyrptedStr[i]))
    bufferList = remove_invalid_characters(bufferList, ['/', '\\', '?', '<', '>', ':', '*', '|', '-', '~', ' '])
    # converts list to STR
    bufferStr = ""
    for i in range(len(bufferList)):
        bufferStr += bufferList[i]
    return bufferStr

code = "Password"
nums = generate_Keys(code)

#if not os.path.exists(writePath):
    #os.makedirs(writePath)

def rename_directory(old_name, new_name):

    os.rename(old_name, new_name)

def clearContents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


total_done = 0

def getFiles(path, Local_Write_Path, encrypting, addition_to_path = ""):
    global total_done
    global file_count
    f = []
    d = []
    nums = generate_Keys(code) # Generates keys
    write_path = Local_Write_Path
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        d.extend(dirnames)
        print("Folder names = ", dirnames)
        print("Filenames = ", filenames)
        # copies directories
        for i in range(len(dirnames)):
            newpath = (write_path + "\\" + addition_to_path + "\\" + d[i])
            if not os.path.exists(newpath):
                os.makedirs(newpath)
        # copies files
        for i in range(len(filenames)):
            total_done += 1
            fillProgressBar(total_done / file_count)
            print(filenames[i])
            fileObj = open(path + "\\"+filenames[i], mode="rb")
            filetext = fileObj.read()

            # Scrambles file data
            tempdata = list(filetext)
            tempdata = Encrypt_Data(tempdata, code, nums)

            # Scrambles file name
            if (encrypting):
                scrambledName = encryptFolderName(filenames[i], code)
            else:
                scrambledName = decryptFolderName(filenames[i], code)
            #StrBuffer = ''
            #for j in range(len(scrambledName)): # List to Str
                #StrBuffer += chr(scrambledName[j])
            #scrambledName = StrBuffer
            #print("Scrambed name: ",scrambledName)
            filenames[i] = scrambledName
            #os.rename(path + "\\"+filenames[i], scrambledName)
            #for j in range(len(tempdata)):
                #tempdata[j] = clamp(tempdata[j],0,255)
                #print(tempdata[j])
            #tempdata = encrypt_str(tempdata, [1,5,4,3,9])
            filetext = bytes(tempdata)
            #filetext = fileObj.read()
            # Writes files to folder
            #print("FN: " + write_path+addition_to_path+"\\"+filenames[i])
            # Must validate file name
            writeObj = open(write_path+addition_to_path+"\\"+filenames[i],"wb")
            writeObj.write(filetext)
        break

    if (len(d) > 0):
        for i in range(len(d)):
            getFiles(path + "\\" + d[i], write_path, encrypting, addition_to_path + "\\" + d[i])
            
def encryptFolderName(my_str, code):
    bufferStr = ""
    for i in range(len(my_str)):
        a = ord(my_str[i])
        a = a ^ ord(code[i % len(code)])
        bufferStr += str(a) + 'a'
    
    return bufferStr

def decryptFolderName(my_str, code):
    valueList = []
    bufferStr = ""
    count = 0
    for i in range(len(my_str)):
        if (my_str[i] == 'a'):
            valueList.append(int(bufferStr) ^ ord(code[count % len(code)]))
            bufferStr = ""
            count += 1
        else:
            bufferStr += my_str[i]
    bufferStr = ""
    for i in range(len(valueList)):
        bufferStr += chr(valueList[i])
    print(valueList)
    return bufferStr

def encryptFolderNames(path, code):
    f = []
    d = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        d.extend(dirnames)
        if (len(d) > 0):
            for i in range(len(d)):
                encryptedName = encryptFolderName(d[i], code)
                os.rename(path + "\\" + d[i], path + "\\" + encryptedName)
                encryptFolderNames(path + "\\" + encryptedName, code)

def decryptFolderNames(path, code):
    f = []
    d = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        d.extend(dirnames)
        if (len(d) > 0):
            for i in range(len(d)):
                decryptedName = decryptFolderName(d[i], code)
                print("d[i]: ",d[i])
                print("2:", path + "\\" + decryptedName)
                os.rename(path + "\\" + d[i], path + "\\" + decryptedName)
                decryptFolderNames(path + "\\" + decryptedName, code)
    
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
completeText = 0
def fillProgressBar(percent, complete = False):
    global completeText
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
    if complete:
        completeText = Text(Point((64 + (-diffW * percent) + 64) / 2, (50 + screenH - 2) / 2), "COMPLETE")
        completeText.setFill(color_rgb(255,255,255))
        completeText.draw(win)
    elif (completeText != 0):
        completeText.undraw()


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

# returns total number of files under a directory and it's subdirectories
def get_file_count(start_path = "C:\\Users\\tripp\\OneDrive\\Documents\Python\\Test Folder"):
    filecount = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                #filecount += os.path.getsize(fp)
                filecount += 1

    return filecount

code = "Password"

def removeExtraQuotes(str):
    newStr = str
    if (str[0] == '"' and str[len(str) - 1] == '"'):
        newStr = ""
        for i in range(1, len(str) - 1):
            newStr += str[i]
    else:
        newStr = str
    print(newStr)
    return newStr

def isPasswordValid(str, decrypting):
    if len(str) < 8:
        errorMessage("PASSWORD MUST BE AT LEAST CHARACTERS LONG")
        return False
    else:
        return True


while True:
    mousePos = win.getMouse()
    if (checkForClick(mousePos, EncryptBox)):
        fillProgressBar(0)
        filepath = textEntry.getText()
        filepath = removeExtraQuotes(filepath)
        password = PasswordTextEntry.getText()
        createMissingPaths(filepath)
        file_count = get_file_count(filepath)
        total_done = 0
        clearContents(writePath) # Do not put this in the encrypt function or it will break it
        getFiles(filepath, writePath, True)
        encryptFolderNames(writePath, code)
        fillProgressBar(1, True)
    if (checkForClick(mousePos, DecryptBox)):
        fillProgressBar(0)
        filepath = textEntry.getText()
        filepath = removeExtraQuotes(filepath)
        password = PasswordTextEntry.getText()
        print("name", filepath[0:-12])
        createMissingPaths(filepath[0:-12])
        file_count = get_file_count(writePath)
        total_done = 0
        clearContents(decryptPath)
        getFiles(writePath, decryptPath, False)
        decryptFolderNames(decryptPath, code)
        fillProgressBar(1, True)
    if (checkForClick(mousePos, newFolderCheckBox)):
        GenNewFolder = not GenNewFolder
        if (GenNewFolder):
            newFolderCheckBox.setFill(color_rgb(200, 20, 20))
        else:
            newFolderCheckBox.setFill(color_rgb(20, 200, 20))
        print("A")

win.close()
