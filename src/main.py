import requests
import os 
import time as t
from src.helpers import image, download, authenticate


def main(style, font, currentOS):
    if (currentOS == "Darwin"):
        from src.helpers import mac
        mac.backupWallpaper()
        display = mac.getScreenResolution()
        print("Display Resolution: " + display)
    elif (currentOS == "Linux"):
        from src.helpers import linux
        display = "1920x1080"
        print("Display Resolution: " + display)
    else:
        print("Your Operating System:("+ str(currentOS)+") is currently unsupported!")
        exit()
    display = display.split("x")
    fontPath = fontSelector(font)
    spotify_token = authenticate.spotify_authenticate()
    oldSong = ''
    while 1:
        songInformation = get_song_id(spotify_token)
        if songInformation[1] != oldSong:
            oldSong = songInformation[1]
            image.albumImage(style, songInformation, display, fontPath)
            if (currentOS == 'Linux'):
                linux.applyWallpaperLinux()
                t.sleep(1)
            elif (currentOS == 'Darwin'):
                mac.applyWallpaperMac()
            print("Current Song: " + songInformation[1] + " - "  + songInformation[2])
        else:
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
        spotify_token = authenticate.spotify_authenticate()
        get_song_id()
    except ValueError:
        print("Looks like no song is playing.")
        print("Waiting for valid song to be played.")
        t.sleep(5)
        spotify_token = authenticate.spotify_authenticate()
        get_song_id()





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
    match font.lower():
        case 'rubik':
            return 'src/fonts/Rubik.ttf'
        case 'signature':
            return 'src/fonts/Photograph Signature.ttf'
        case 'creamcake':
            return 'src/fonts/CreamCake.otf'
        case _:
            "Font provided: " + str(font) + " is not currently supported defaulting to Rubik"
            return 'src/fonts/Rubik.ttf'





    
