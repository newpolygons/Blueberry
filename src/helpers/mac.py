import os 
import subprocess
import random
import shutil
import time
from ast import literal_eval


def applyWallpaperMac():
    number = random.randint(1, 999999)
    imagePath = "src/helpers/.cache/finalImage.png"
    pathList = os.path.splitext(imagePath)
    path = pathList[0] + str(number)
    with open("src/helpers/.cache/currentWallpaper.txt", "r") as f:
        currentWall = f.read()
        f.close()
    if currentWall != path:
        with open("src/helpers/.cache/currentWallpaper.txt", "w") as f:
            try:
                os.remove(currentWall + ".png")
            except Exception as e:
                print(e)
            f.write(path)
            f.close()
    
def backupWallpaper():
    '''
    cmd = """
    tell application "Finder"
    set theDesktopPic to desktop picture as alias
    set theName to posix path of theDesktopPic
    end tell
    """
    wallPath = subprocess.run(['osascript', '-e', cmd], capture_output = True, text = True).stdout.strip("\n")
    print("This is the file path of the current wallpaper: ", wallPath)
    try:
        timeStamp = str(time.time()).replace('.','')
        os.mkdir('src/wallpaperBackup/' + timeStamp + '/')
        wallBackPath = str('src/wallpaperBackup/' + timeStamp + '/')
        shutil.copy(wallPath, wallBackPath)
    except Exception as e:
        print(e)
        print("An issue occured with the original wallpaper backup!")
        print("Exiting application to prevent loss of original wallpaper.")
        exit()
    '''
    pass


def getScreenResolution():
    cmd = subprocess.run(["./src/swift/screenResolution.swift"], capture_output = True)
    resString = cmd.stdout.decode('ASCII')
    resTuple = literal_eval(resString)
    width = str(int(resTuple[2]))
    height = str(int(resTuple[3]))
    res = width + "x" + height
    return res

    
    
