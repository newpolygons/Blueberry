import argparse
import platform
from src import main

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", default='video', 
                        help="Choose the background style 'video', 'gradient' or 'block', default is video.")
    parser.add_argument("--font", default='Rubik',
                        help="Choose the font 'Rubik', 'Signature' or 'CreamCake', default is Rubik. ")
    parser.add_argument("--restore-wall", action='store_true', 
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
    elif args.restore-wall:
        print("This isnt implemented yet but backing up wallpapers is! go to src/wallpaperBackup to find your original wallpaper :)")
    else:
        currentOS = platform.system()
        main.main(str(args.style), str(args.font), str(currentOS))



if __name__ == '__main__':
    run()
