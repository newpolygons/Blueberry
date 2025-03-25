import os
import argparse
import platform
from src import main

def init():
    #initialize ... sanity check
    imPath = 'src/helpers/.cache/newCover.png'
    curWal = 'src/helpers/.cache/currentWallpaper.txt'
    finIm = "src/helpers/.cache/finalImage.png"
    if not os.path.isfile(imPath):
        try:
            from PIL import Image
            img = Image.new('RGB', (512, 512), (255, 102, 102))
            img.save(imPath)
        except Exception as e:
            print("No 'newCover.png' in .cache")
            exit()
    if not os.path.isfile(finIm):
        try:
            from PIL import Image
            img = Image.new('RGB', (512, 512), (255, 102, 102))
            img.save(finIm)
        except Exception as e:
            print("No 'finalImage.png' in .cache")
            exit()
    if not os.path.isfile(curWal):
        try:
            os.system('touch src/helpers/.cache/currentWallpaper.txt')
        except:
            print("Issue with 'currentWallpaper.txt in .cache'")
            exit()

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", default='gradient', 
                        help="Choose the background style 'gradient' or 'block', default is gradient.")
    parser.add_argument("--font", default='Rubik',
                        help="Choose the font 'Rubik', 'Signature' or 'CreamCake', default is Rubik. ")
    parser.add_argument("--restorewall", action='store_true', 
                        help="Restore backed up wallpaper.")
    parser.add_argument("--download", default='', 
                        help="Download a spotify song, please provide the link in quotes eg 'https://spotify.com' ")
    parser.add_argument("--clean", action='store_true', 
                        help="Clear all files in src/helpers/.cache")                        
    args = parser.parse_args()

    
    if args.download != '':
        from src.helpers import download
        download.downloadCurrentSong(str(args.download))
    elif args.clean:
        main.removeCache()
    elif args.restorewall:
        print("This isnt implemented yet but backing up wallpapers is (!ONMACRN!)  !!! go to src/wallpaperBackup to find your original wallpaper :)")
    else:
        currentOS = platform.system()
        main.main(str(args.style), str(args.font), str(currentOS))



if __name__ == '__main__':
    run()
