import os
import argparse
import platform
from src import main as m


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
    args = parser.parse_args()

    
    if args.download != '':
        from src.helpers import download
        download.downloadCurrentSong(str(args.download))
    elif args.restorewall:
        print("This isnt implemented yet!")
    else:
        currentOS = platform.system()
        m.main(str(args.style), str(args.font), str(currentOS))



if __name__ == '__main__':
    m.init()
    run()
