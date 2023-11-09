import shutil
from os import walk
import os


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

def getFiles(path, Local_Write_Path, encrypting, addition_to_path = ""):
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
total_done = 0
def encryptFolderNames(path, code):
    global total_done
    total_done += 1
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
                fillProgressBar(file_count / total_done)

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

# clearContents(writePath) # Do not put this in the encrypt function or it will break it
# getFiles(mypath, writePath, True)
# encryptFolderNames(writePath, code)
# clearContents(decryptPath)
# getFiles(writePath, decryptPath, False)
# decryptFolderNames(decryptPath, code)
