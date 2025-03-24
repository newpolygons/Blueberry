import os

# https://www.baeldung.com/linux/change-desktop-wallpaper-from-terminal linux wallpaper things

#Subprocess this?
def applyWallpaperLinux():
    os.system("gsettings set org.gnome.desktop.background picture-uri file://" + os.getcwd() + "/src/helpers/.cache/finalImage.png")