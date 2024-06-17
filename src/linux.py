import os
def applyWallpaperLinux():
    cwd = os.getcwd()
    os.system("gsettings set org.gnome.desktop.background picture-uri " + cwd + "/ImageCache/finalImage.png")