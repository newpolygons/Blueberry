import requests
import os 
import time as t
from src.helpers import image, download, authenticate


def main(style, font, currentOS):
    if (currentOS == "Darwin"):
        from src.helpers import mac
        display = mac.getScreenResolution()
        display = display.split("x")
    elif (currentOS == "Linux"):
        from src.helpers import linux
        colorMode, display = linux.getScreenResolution()
    else:
        print("Your Operating System:("+ str(currentOS)+") is currently unsupported!")
        exit()
    
    fontPath = fontSelector(font)
    spotify_token = authenticate.spotify_authenticate()
    oldSong = ''
    
    while 1:
        songInformation = get_song_id(spotify_token)    
        if songInformation is None:
            spotify_token = authenticate.spotify_authenticate()
            songInformation = get_song_id(spotify_token)
        if songInformation[1] != oldSong:
            oldSong = songInformation[1]
            image.albumImage(style, songInformation, display, fontPath) 
            if (currentOS == 'Linux'):
                linux.applyWallpaperLinux(colorMode)
                t.sleep(1)
            elif (currentOS == 'Darwin'):
                mac.applyWallpaperMac()
                t.sleep(1) 
            print("Current Song: " + songInformation[1] + " - "  + songInformation[2])
        else:
            t.sleep(5)
    

def get_song_id(spotify_token):
    spotify_token = spotify_token
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
        t.sleep(5)
        spotify_token = authenticate.spotify_authenticate()
        get_song_id(spotify_token)
        
    except TypeError:
        print("Spotify Error: make sure valid song is playing")
        print("Waiting for valid song to be played.")
        t.sleep(5)
        get_song_id(spotify_token)
    
    except ValueError:
        print("Looks like no song is playing.")
        print("Waiting for valid song to be played.")
        t.sleep(5)
        get_song_id(spotify_token)



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



def init():
    #initialize ... sanity check
    imPath = 'src/helpers/.cache/newCover.png'
    curWal = 'src/helpers/.cache/currentWallpaper.txt'
    finIm = "src/helpers/.cache/finalImage.png"
    if not os.path.isfile(imPath):
        try:
            from PIL import Image
            img = Image.new('RGB', (512, 512), (255, 102, 102))
            img.save(imPath)
        except Exception as e:
            print("No 'newCover.png' in .cache")
            exit()
    if not os.path.isfile(finIm):
        try:
            from PIL import Image
            img = Image.new('RGB', (512, 512), (255, 102, 102))
            img.save(finIm)
        except Exception as e:
            print("No 'finalImage.png' in .cache")
            exit()
    if not os.path.isfile(curWal):
        try:
            os.system('touch src/helpers/.cache/currentWallpaper.txt')
        except:
            print("Issue with 'currentWallpaper.txt in .cache'")
            exit()




    
