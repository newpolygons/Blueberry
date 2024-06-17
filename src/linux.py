import os
def applyWallpaperLinux():
    os.chdir('..')
    print("Changing wallpaper")
    os.system("gsettings set org.gnome.desktop.background picture-uri file://" + os.getcwd() + "/ImageCache/finalImage.png")
    os.chdir('src')