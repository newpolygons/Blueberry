from types import ClassMethodDescriptorType
from spotipy.oauth2 import SpotifyOAuth
import requests, os, platform
import time as t
import spotipy.util as util
import eel, pickle, json, requests
import imageManip

if (platform.system() == "Darwin"):
    import mac

if (platform.system() == 'Linux'):
    import linux
# Get creds please enter your creds in creds.txt at path /Blueberry/creds.txt

global spotify_token, client_id, client_secret, username, display
client_id = ""
client_secret = ""
spotify_token = ""
username = ""
scope = "user-read-currently-playing"
display = ""
mode = ""
counter = 0

def main():
    if (platform.system() == "Darwin"):
        mac.backupWallpaper()
        resolution = mac.getScreenResolution()
    datadict = get_variables()
    global client_secret, colors, client_id, username, display, mode
    client_id = datadict["client_id"]
    client_secret = datadict["client_secret"]
    username = datadict["spot_username"]
    mode = datadict["mode"]
    
    # Begin work to auto collect display resolution will be perminitly changed after Linux Testing
    if (platform.system() == "Darwin"):
        display = resolution
        display = display.split("x")
    else:
        display = datadict["display_size"]
        display = display.split("x")
    
    #eel.init('web')
    #eel.start('main.html', size=(int(display[0])/3, int(display[0])/3), mode='chrome')

    spotify_authenticate()

    get_song_id()


def spotify_authenticate():
    global spotify_token
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, "https://www.google.com/")
    if token:
        spotify_token = token
    else:
        print("Couldn't get proper Spotify authentication")
        exit()


def get_song_id():
    header = {
        "Authorization": "Bearer {}".format(spotify_token)
    }
    get_id = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=header)
    try:
        song_content = get_id.json()
        id = song_content['item']['id']
        if not id:
            t.sleep(2)
            get_song_id()
        
        
        
        name = song_content['item']['name']    
        artistName = song_content['item']['album']['artists'][0]['name']
        imageUrl = song_content['item']['album']['images'][0]['url']         
        imageRequest = requests.get(str(imageUrl))
        file = open("../ImageCache/newCover.png", "wb")
        file.write(imageRequest.content)
        file.close()
        return [id, name, artistName]
    except KeyError:
        spotify_authenticate()
        get_song_id()
    except TypeError:
        print("Spotify Error: make sure valid song is playing")
        print("Waiting for valid song to be played.")
        t.sleep(5)
        get_song_id()
    except ValueError:
        print("Error: looks like no song is playing")
        print("Waiting for song to be played.")
        t.sleep(5)
        get_song_id()



def get_variables():
    dicti = {}
    with open('../creds.txt', 'r') as file:
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
    f = open("songCheck.txt", "r")
    song = f.read()
    f.close()
    return song


main()



while 1:
    songInformation = get_song_id()
    songTitle = imageManip.albumImage(mode, songInformation, display)

    if songTitle != checkSong():
        f = open("songCheck.txt", "w")
        f.write(songTitle)
        f.close()
        if (platform.system() == 'Linux'):
            linux.applyWallpaperLinux()
        elif (platform.system() == 'Darwin'):
            mac.applyWallpaperMac()
        

    counter = counter + 1
    t.sleep(5)

