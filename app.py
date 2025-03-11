import argparse
import platform
#from src import main


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", default='gradient', 
                        help="Choose the background style, 'gradient' or 'block'")
    parser.add_argument("--download", action='store_true', 
                        help="Download currently playing Spotify song")
    args = parser.parse_args()

    currentOS = platform.system()

    print(str(args))
    #main.main(args.style, args.download, currentOS)



if __name__ == '__main__':
    run()
