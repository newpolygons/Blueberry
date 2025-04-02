import os 
import subprocess
import random as r
from ast import literal_eval


def applyWallpaperMac():
    imagePath = "src/helpers/.cache/finalImage.png"
    
    #Force macOS to change wallpaper by appending a number to end of file name (safely)
    pathList = os.path.splitext(imagePath)
    path = (pathList[0] + str(r.randint(1,50))) + pathList[1]
    
    try:
        os.rename(imagePath, path)
        subprocess.run(["./src/swift/changeWallpaper.swift", path])
        
        # also implement cleanup of images without breaking
        for i in os.listdir('src/helpers/.cache/'):
            if i.endswith('.png') and ('src/helpers/.cache/' + i) != path:
                os.remove('src/helpers/.cache/' + i)
    
    except Exception as e:
        print(e)
        print('Unable to create image and apply wallpaper :( ')
        print('Check src/helpers/.cache and make sure there is a finalImage.png there.')


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

    
    
