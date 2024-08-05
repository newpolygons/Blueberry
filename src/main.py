import requests
import os 
import platform 
import glob
import spotipy
import time as t
import imageManip
from rich import print

if (platform.system() == "Darwin"):
    import mac

if (platform.system() == 'Linux'):
    import linux

# Get creds please enter your creds in creds.txt at path /Blueberry/creds.txt
display = ""
mode = ""

def main():
    datadict = get_variables()
    if (platform.system() == "Darwin"):
        mac.backupWallpaper()
        display = mac.getScreenResolution()
        print("[green]Display Resolution: [/green]" + display)
    else:
        display = datadict["display_size"]
        print("[green]Display Resolution: [/green]" + display)
    mode = datadict["mode"]
    print("[green]Selected Mode: [/green]" + mode)

    # Begin work to auto collect display resolution will be perminitly changed after Linux Testing

    display = display.split("x")

    spotify_authenticate()

    while 1:
        songInformation = get_song_id()
        songTitle = imageManip.albumImage(mode, songInformation, display)

        if songTitle != checkSong():
            f = open("src/songCheck.txt", "w")
            f.write(songTitle)
            f.close()
            if (platform.system() == 'Linux'):
                linux.applyWallpaperLinux()
                t.sleep(1)
            elif (platform.system() == 'Darwin'):
                mac.applyWallpaperMac()
            print(":sound:Current Song: " + songInformation[1] + " - "  + songInformation[2])
        else:
            print(":zzz:[blue]Song hasnt changed yet going to sleep...[/blue]")
            t.sleep(5)
    


def spotify_authenticate():
    #If you want to use your own Spotify application change client_id here.
    client_id = "2a487b56eba34dbdb32c7109f6292b9c"
    redirect_uri = "http://127.0.0.1:8080"
    auth_manager = spotipy.oauth2.SpotifyPKCE(scope='user-read-currently-playing', client_id = client_id,
                                               redirect_uri = redirect_uri)
    global spotify_token
    spotify_token = spotipy.Spotify(auth_manager.get_access_token())
    

def get_song_id():
    songINFO = spotify_token.current_user_playing_track()
    try:
        song_content = songINFO
        id = song_content['item']['id']
        if not id:
            t.sleep(2)
            get_song_id()
        
        name = song_content['item']['name']    
        artistName = song_content['item']['album']['artists'][0]['name']
        imageUrl = song_content['item']['album']['images'][0]['url']         
        imageRequest = requests.get(str(imageUrl))
        file = open("ImageCache/newCover.png", "wb")
        file.write(imageRequest.content)
        file.close()
        return [id, name, artistName]
    except KeyError:
        print("[bold red]KEY ERROR, attempting to reauthenticate![/bold red]")
        spotify_authenticate()
        
    except TypeError:
        print("[bold red]Spotify Error: make sure valid song is playing[/bold red]")
        print("[/yellow]:yawning_face:Waiting for valid song to be played.[/yellow]")
        t.sleep(5)
        get_song_id()
    except ValueError:
        print("[bold red]Error: looks like no song is playing[/bold red]")
        print("[/yellow]:yawning_face:Waiting for valid song to be played.[/yellow]")
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









