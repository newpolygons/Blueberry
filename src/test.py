# for testing functions individually.
import subprocess
import shutil
import os

# testing function for backing up current wallpaper MACOS
def testbackupWallpaperMAC():
    cmd = """
    tell application "Finder"
    set theDesktopPic to desktop picture as alias
    set theName to posix path of theDesktopPic
    end tell
    """
    wallPath = subprocess.run(['osascript', '-e', cmd], capture_output = True)
    print("This is the file path of the current wallpaper: ", str(wallPath.stdout.decode('ASCII')))
    
    if os.listdir('backup') == []:
        print("Backing up current wallpaper to /backup folder")
        try:
            shutil.copy(str(wallPath.stdout.decode('ASCII')).replace('\n', ''), 'backup')
        except Exception as e:
            print("An issue occured with the original wallpaper backup!")
            print("Exiting application to prevent loss of original wallpaper.")
            print(e)
            exit()

    else:
        print("!WARNING! backupfolder already contains files we will not backup the current wallpaper to avoid overwriting actual original :)")


# testing function for returning resolution of current main display MACOS
from ast import literal_eval
def testgetScreenResolutionMAC():
    cmd = subprocess.run(["./src/swift/screenResolution.swift"], capture_output = True)
    resString = cmd.stdout.decode('ASCII')
    resTuple = literal_eval(resString)
    width = str(int(resTuple[2]))
    height = str(int(resTuple[3]))
    res = width + "x" + height
    print("This is the resolution found for the main display:" , res)



# Uncomment below line of funtion you want to test then run python3 src/test.py from main dir

#testbackupWallpaperMAC()
#testgetScreenResolutionMAC()