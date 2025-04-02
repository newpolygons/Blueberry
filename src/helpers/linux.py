import os
import subprocess
# https://www.baeldung.com/linux/change-desktop-wallpaper-from-terminal linux wallpaper things


def applyWallpaperLinux(colorMode):
    colorMode = colorMode.strip("' ")
    cacheDir = 'src/helpers/.cache/'
    if colorMode == 'default':
        os.system("gsettings set org.gnome.desktop.background picture-uri file://" + os.getcwd() + "/src/helpers/.cache/finalImage.png")
    elif colorMode == 'prefer-dark':
        os.system("gsettings set org.gnome.desktop.background picture-uri-dark file://" + os.getcwd() + "/src/helpers/.cache/finalImage.png")
    else:
        print("Issues in the applyWallpaperLinux() function report the following string as an issue on github.")
        print('Cannot set picture uri ' + str(colorMode))

    # also implement cleanup of images without breaking
    for i in os.listdir(cacheDir):
        if i.endswith('.png') and cacheDir+i != "src/helpers/.cache/finalImage.png":
            print(i)
            print(cacheDir+i)
            try:
                os.remove(cacheDir+i)
            except Exception as e:
                print(e)
                return


# This function will collect  display resolution and light/dark mode prefernece
def getScreenResolution():
    
    try:
        cmdColorMode = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"], capture_output = True)
        colorMode = cmdColorMode.stdout.decode('ASCII').strip()
    except Exception as e:
        print("There was an issue with getting your light/dark prefernece assuming light.")
        print("Change line 19 in src/helpers/linux.py to 'prefer-dark' if this is wrong.")
        colorMode = 'default'
        print("This is the error: ")
        print(str(e))
    
    try:

        cmdScreenRes = os.popen("xrandr | grep '*' | awk '{ print $1 }'").read()
        screenRes = cmdScreenRes.split('x')
        screenRes = [number.strip() for number in screenRes]
    except Exception as e:
        print("There was an issue getting the current diplay resolution!")
        print("Setting display res to 1920x1080! You can modify this behavior in src/helpers/linux.py")
        screenRes = ['1920', '1080']
        print(str(e))

    return colorMode, screenRes


def backupWallpaper():
    pass

