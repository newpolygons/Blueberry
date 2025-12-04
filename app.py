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
    parser.add_argument("--video", action='store_true',
                        help="Wallpaper will be a video, other stylizations will be ignored.. for now.")
    parser.add_argument("--restorewall", action='store_true', 
                        help="Restore backed up wallpaper.")
    parser.add_argument("--download", default='', 
                        help="Download a spotify song, please provide the link in quotes eg 'https://spotify.com' ")                     
    parser.add_argument("--preview", action='store_true', 
                        help="Devolper function, opens image in image viewer while running.")
    args = parser.parse_args()

    
    if args.download != '':
        from src.helpers import download
        download.downloadCurrentSong(str(args.download))
    elif args.restorewall:
        print("This isnt implemented yet!")
        exit()
    elif args.video:
        #implement vid functionality.
        pass
    else:
        currentOS = platform.system()
        m.main(str(args.style), str(args.font), args.preview, str(currentOS))



if __name__ == '__main__':
    m.init()
    run()
