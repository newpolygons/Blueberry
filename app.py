# Run this file to begin. File should be ran from its directory directly.
# python3 -m flask run
#Threading https://stackoverflow.com/questions/63500768/how-to-work-with-background-threads-in-flask
# https://vmois.dev/python-flask-background-thread/
import os
import sys
from rich import print
sys.path.insert(1, 'src')
import main



def wallpaperFunc():
    print(":large_blue_circle:[bold blue]Blueberry[/bold blue]")
    print("[blue]by: NewPolygons[/blue]")
    main.main()




wallpaperFunc()