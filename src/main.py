import requests
import os 
import spotipy
import time as t
from src.helpers import image
from src.helpers import download
from src.helpers import authenticate
def setupPlatform(currentOS):
    if (currentOS == "Darwin"):
        from src import mac
        mac.backupWallpaper()
        display = mac.getScreenResolution()
        print("Display Resolution: " + display)
        return display
    elif (currentOS == "Linux"):
        from src import linux
        # Begin work to auto collect display resolution will be perminitly changed after Linux Testing
        datadict = get_variables()
        display = datadict["display_size"]
        print("Display Resolution: " + display)
        return display
    else:
        print("Your current Operating System:("+ str(currentOS)+") is currently unsupported!")
        exit()

# Get creds please enter your creds in creds.txt at path /Blueberry/creds.txt


def main(style, font, currentOS):
    display = setupPlatform(currentOS).split("x")
    fontPath = fontSelector(font)
    spotify_token = authenticate.spotify_authenticate()
    oldSong = ''
    while 1:
        songInformation = get_song_id(spotify_token)
        songTitle = image.albumImage(style, songInformation, display, fontPath)

        if songTitle != oldSong:
            oldSong = songTitle
            if (currentOS == 'Linux'):
                linux.applyWallpaperLinux()
                t.sleep(1)
            elif (currentOS == 'Darwin'):
                mac.applyWallpaperMac()
            print("Current Song: " + songInformation[1] + " - "  + songInformation[2])
        else:
            print("Song hasnt changed yet going to sleep...")
            t.sleep(5)
    

def get_song_id(spotify_token):
    songInfo = spotify_token.current_user_playing_track()
    try:
        songContent = songInfo
        id = songContent['item']['id']
        if not id:
            t.sleep(4)
            get_song_id()
        
        name = songContent['item']['name']    
        artistName = songContent['item']['album']['artists'][0]['name']
        imageUrl = songContent['item']['album']['images'][0]['url']         
        imageRequest = requests.get(str(imageUrl))

        
        file = open("src/helpers/.cache/newCover.png", "wb")
        file.write(imageRequest.content)
        file.close()
        return [id, name, artistName]
    except KeyError:
        print("KEY ERROR, attempting to reauthenticate!")
        spotify_token = authenticate.spotify_authenticate()
        
    except TypeError:
        print("Spotify Error: make sure valid song is playing")
        print("Waiting for valid song to be played.")
        t.sleep(5)
        get_song_id()
    except ValueError:
        print("[bold red]Error: looks like no song is playing[/bold red]")
        print("[yellow]:yawning_face:Waiting for valid song to be played.[/yellow]")
        t.sleep(5)
        get_song_id()


def get_variables():
    dicti = {}
    with open('creds.txt', 'r') as file:
        content = file.readlines()
        for line in content:
            if "=" in line:
                v = line.split("=")
                if len(v) == 2:
                    dicti[v[0].strip()] = v[1].strip()
                else:
                    print("Please fill in your information on the creds.txt file")
                    exit()
        return dicti



def removeCache():
    cacheDirectory = 'src/helpers/.cache'
    for file in os.listdir(cacheDirectory):
        filePath = os.path.join(cacheDirectory, file)
        if os.path.isfile(filePath):
            try:
                print("Deleting cache file: " + str(filePath))
                os.remove(filePath)
            except:
                print("There was an issue deleting files in src/helpers/.cache")
                exit()


def fontSelector(font):
    match lower(font):
        case 'rubik':
            return 'src/fonts/Rubik.ttf'
        case 'signature':
            return 'src/fonts/Photograph Signature.ttf'
        case 'creamcake':
            return 'src/fonts/CreamCake.otf'
        case _:
            "Font provided: " + str(font) + " is not currently supported defaulting to Rubik"
            return 'src/fonts/Rubik.ttf'





    
