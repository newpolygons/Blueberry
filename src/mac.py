import shutil
import os 
import subprocess
import random
from appscript import app, mactypes
from AppKit import NSScreen
from pathlib import Path


def applyWallpaperMac():
    #magic to force mac wallpaper to refresh (not proud of this implementation come back some day)

    number = random.randint(1, 999999)
    imagePath = "ImageCache/finalImage.png"
    pathList = os.path.splitext(imagePath)
    path = pathList[0] + str(number)
    
    #handle deleting old images.
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
    subprocess.run(["./src/chwall.swift", path + ".png"])
    
def backupWallpaper():
    '''
    currentWallpaper = app('Finder').desktop_picture.get().path
    shutil.copy(currentWallpaper, '../ImageCache/backupwallpaper.png')
    '''
    pass


def getScreenResolution():
    width = int(NSScreen.mainScreen().frame().size.width)
    height = int(NSScreen.mainScreen().frame().size.height)
    width = str(width)
    height = str(height)
    res = width + "x" + height
    return res

    
    