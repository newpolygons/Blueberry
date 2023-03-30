from types import ClassMethodDescriptorType
import requests, colorgram, os, platform
import time as t
import spotipy.util as util
from PIL import Image, ImageDraw, ImageFont
from spotipy.oauth2 import SpotifyOAuth
import mac, linux
# Get creds please enter your creds in creds.txt

global spotify_token, client_id, client_secret, username, display
client_id = ""
client_secret = ""
spotify_token = ""
username = ""
scope = "user-read-currently-playing"
display = ""
counter = 0

def main():
    if (platform.system() == "Darwin"):
        mac.backupWallpaper()
    datadict = get_variables()
    global client_secret, colors, client_id, username, display
    client_id = datadict["client_id"]
    client_secret = datadict["client_secret"]
    username = datadict["spot_username"]
    display = datadict["display_size"]
    display = display.split("x")
    
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
        imageUrl = song_content['item']['album']['images'][1]['url']         
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


def albumImage():
    try:
        songInformation = get_song_id()
        songTitle = songInformation[1]
        songArtist = songInformation[2]
    except:
        return
     # Setup Album Image
    width = int(int(display[0]) / 5)
    height = int(int(display[1]) / 2)
    
    baseWidth = int(display[0])
    baseHeight = int(display[1])
    image = Image.open("../ImageCache/newCover.png")
    wpercent = (width/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((width,hsize), Image.LANCZOS)
    image.save('../ImageCache/albumImage.png')

    colors = getColors()

    colorImageOne = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[0].rgb))
    titleArtist = ImageDraw.Draw(colorImageOne)

    myFont = ImageFont.truetype("../fonts/Rubik.ttf", 40)
    titleArtist.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (255,255,255))
    colorImageOne.save('../ImageCache/firstColor.png')

    colorImageTwo = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[1].rgb))
    colorImageTwo.save('../ImageCache/secondColor.png')


    #Combine Images

    background = Image.new('RGB', (colorImageOne.width, colorImageOne.height + colorImageTwo.height))
    background.paste(colorImageOne, (0, 0))
    background.paste(colorImageTwo, (0, colorImageOne.height))
    background.save('../ImageCache/background.png')

    
    finalImage = Image.new('RGB', (width, height))
    background.paste(image, ((int(background.width/2) - int(image.width / 2)), int((background.height/2) - int(image.height / 2))))
    background.save("../ImageCache/finalImage.png")

    return songTitle

def getColors():
    #Setup Background Colors
    colors = colorgram.extract('../ImageCache/albumImage.png', 2)
    if len(colors) < 2:
        firstColor = colors[0]
        secondColor = colors[0]
    else:
        firstColor = colors[0]
        secondColor = colors[1]
    
    return([firstColor, secondColor])

def checkSong():
    f = open("songCheck.txt", "r")
    song = f.read()
    f.close()
    return song


main()

while 1:
    
    songTitle = albumImage()

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

