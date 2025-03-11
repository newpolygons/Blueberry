import requests
import os 
import platform 
import glob
import spotipy
import time as t
from src import image
from src import download

setupPlatform(currentOS):
    if (currentOS == "Darwin"):
        from src import mac
        mac.backupWallpaper()
        display = mac.getScreenResolution()
        print("Display Resolution: " + display)

    elif (currentOS == 'Linux'):
        from src import linux
        # Begin work to auto collect display resolution will be perminitly changed after Linux Testing
        datadict = get_variables()
        display = datadict["display_size"]
        print("Display Resolution: " + display)
    else:
        print("Your current Operating System:("+ str(currentOS)+") is currently unsupported!")
        exit()

# Get creds please enter your creds in creds.txt at path /Blueberry/creds.txt
display = ""


def main(style, download, font, currentOS):
    if download = True:
        spotify_authenticate()
        download.downloadCurrentSong(link)
        exit()
    
    style = style
    print("Selected Mode: " + mode)
    display = display.split("x")
    spotify_authenticate()
    
    while 1:
        songInformation = get_song_id()
        songTitle = imageManip.albumImage(mode, songInformation, display)

        if songTitle != checkSong():
            #update to just hold in var
            f = open("src/songCheck.txt", "w")
            f.write(songTitle)
            f.close()
            if (currentOS == 'Linux'):
                linux.applyWallpaperLinux()
                t.sleep(1)
            elif (currentOS == 'Darwin'):
                mac.applyWallpaperMac()
            print("Current Song: " + songInformation[1] + " - "  + songInformation[2])
        else:
            print("Song hasnt changed yet going to sleep...")
            t.sleep(5)
    

def get_song_id():
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

        #turn image.content into var
        file = open("src/ImageCache/newCover.png", "wb")
        file.write(imageRequest.content)
        file.close()
        return [id, name, artistName]
    except KeyError:
        print("KEY ERROR, attempting to reauthenticate!")
        spotify_authenticate()
        
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


def checkSong():
    f = open("src/songCheck.txt", "r")
    song = f.read()
    f.close()
    return song


def removeImageCache():
    files = glob.glob('ImageCache/*')
    for f in files:
        try:
            os.remove(f)
        except:
            pass







    
