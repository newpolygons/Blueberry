from appscript import app, mactypes
from pathlib import Path
import shutil, os, subprocess, random


def applyWallpaperMac():
    #magic to force mac wallpaper to refresh (not proud of this implementation come back some day)
    number = random.randint(1, 999999)
    imagePath = "ImageCache/finalImage.png"
    pathList = os.path.splitext(imagePath)
    path = pathList[0] + str(number)
    
    #handle deleting old images.
    with open("currentWallpaper.txt", "r") as f:
        currentWall = f.read()
        f.close()
    if currentWall != path:
        with open("currentWallpaper.txt", "w") as f:
            try:
                os.remove(str(Path(os.getcwd()).parents[0])+ "/" + currentWall + ".png")
            except:
                print("The file was likely empty if this is your first time running disreguard.")
            f.write(path)
            f.close()
        
    os.chdir('..')
    os.rename(imagePath, path + ".png")
    subprocess.run(["./src/chwall.swift", path + ".png"])
    os.chdir('src')
    
def backupWallpaper():
    '''
    currentWallpaper = app('Finder').desktop_picture.get().path
    shutil.copy(currentWallpaper, '../ImageCache/backupwallpaper.png')
    '''
    pass
    