import os 
import subprocess
import random
import shutil
from ast import literal_eval


def applyWallpaperMac():
    #magic to force mac wallpaper to refresh (not proud of this implementation come back some day)

    number = random.randint(1, 999999)
    imagePath = "ImageCache/finalImage.png"
    pathList = os.path.splitext(imagePath)
    path = pathList[0] + str(number)
    
    with open("src/currentWallpaper.txt", "r") as f:
        currentWall = f.read()
        f.close()
    if currentWall != path:
        with open("src/currentWallpaper.txt", "w") as f:
            try:
                os.remove("ImageCache/" + currentWall + ".png")
            except:
                print("The file was likely empty if this is your first time running disreguard.")
            f.write(path)
            f.close()
        
    os.rename(imagePath, path + ".png")
    subprocess.run(["./src/swift/changeWallpaper.swift", path + ".png"])
    
def backupWallpaper():
    cmd = """
    tell application "Finder"
    set theDesktopPic to desktop picture as alias
    set theName to posix path of theDesktopPic
    end tell
    """
    wallPath = subprocess.run(['osascript', '-e', cmd], capture_output = True)
    if os.listdir('backup') == []:
        try:
            shutil.copy(str(wallPath.stdout.decode('ASCII')).replace('\n', ''), 'backup')
        except Exception as e:
            print("An issue occured with the original wallpaper backup!")
            print("Exiting application to prevent loss of original wallpaper.")
            print(e)
            exit()

    else:
        print("!WARNING! backupfolder already contains files we will not backup the current wallpaper to avoid overwriting actual original :)")


def getScreenResolution():
    cmd = subprocess.run(["./src/swift/screenResolution.swift"], capture_output = True)
    resString = cmd.stdout.decode('ASCII')
    resTuple = literal_eval(resString)
    width = str(int(resTuple[2]))
    height = str(int(resTuple[3]))
    res = width + "x" + height
    return res

    
    