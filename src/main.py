from types import ClassMethodDescriptorType
import requests, colorgram, os, platform
import time as t
import spotipy.util as util
from PIL import Image, ImageDraw, ImageFont
from spotipy.oauth2 import SpotifyOAuth
import linux
# Get creds please enter your creds in creds.txt

global spotify_token, client_id, client_secret, username, display, original_wallpaper, command, mode
client_id = ""
client_secret = ""
spotify_token = ""
username = ""
scope = "user-read-currently-playing"
display = ""


#check if gnome is in dark mode or light mode
mode = 'dark' if 'dark' in (os.popen("gsettings get org.gnome.desktop.interface gtk-theme").read()) else 'light'

#set the command to change the wallpaper: it changes depending on the mode
command = 'gsettings set org.gnome.desktop.background picture-uri ' if mode == 'light' else 'gsettings set org.gnome.desktop.background picture-uri-dark '

#get the path of the original wallpaper
original_wallpaper = os.popen("gsettings get org.gnome.desktop.background picture-uri-dark").read()


def init():
    # Get variables from the credentials file
    datadict = get_variables()

    #check if 'src/songCheck.txt' exists, if not create it
    if not os.path.exists("src/songCheck.txt"):
        f = open("src/songCheck.txt", "w")
        f.write("")
        f.close()

    # Declare global variables to be used in other functions
    global client_secret, colors, client_id, username, display

    # Assign values from the data dictionary to the global variables
    client_id = datadict["client_id"]
    client_secret = datadict["client_secret"]
    username = datadict["spot_username"]
    display = datadict["display_size"]
    display = display.split("x")

    # Authenticate with Spotify API
    spotify_authenticate()

    # Get the ID of the currently playing song
    get_song_id()


def spotify_authenticate():
    # Get the Spotify access token for authentication
    global spotify_token
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, "https://www.google.com/")

    if token:
        spotify_token = token
    else:
        print("Couldn't get proper Spotify authentication")
        exit()


def get_song_id():
    # Get the ID, name, artist, and image URL of the currently playing song from Spotify API
    header = {
        "Authorization": "Bearer {}".format(spotify_token)
    }
    get_id = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=header)

    try:
        song_content = get_id.json()
        id = song_content['item']['id']

        # If the ID is not available, wait for 2 seconds and retry getting the song ID
        if not id:
            t.sleep(2)
            get_song_id()

        name = song_content['item']['name']
        artistName = song_content['item']['album']['artists'][0]['name']
        imageUrl = song_content['item']['album']['images'][1]['url']
        imageRequest = requests.get(str(imageUrl))
        file = open("ImageCache/newCover.png", "wb")
        file.write(imageRequest.content)
        file.close()

        return [id, name, artistName]
    except KeyError:
        # If a KeyError occurs (e.g., song content is not available), re-authenticate and retry getting the song ID
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
    # Read the credentials from the creds.txt file and store them in a dictionary
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

def get_song_name():
    # Get the name of the currently playing song
    songInformation = get_song_id()
    return songInformation[1]

def albumImage():
    try:
        # Get the song information including title and artist
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
    image = Image.open("ImageCache/newCover.png")
    wpercent = (width/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((width,hsize), Image.LANCZOS)
    image.save('ImageCache/albumImage.png')
    
    colors = getColors()

    # Setup Text: check if the first color is too light or too dark
    textColor = colors[0].rgb

    #if the color is too light, make the text black, otherwise make it white
    if (textColor[0]*0.299 + textColor[1]*0.587 + textColor[2]*0.114) > 186:
        textColor = (int(0), int(0), int(0))
    else:
        textColor = (int(255), int(255), int(255))
     

    colors = getColors()

    colorImageOne = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[0].rgb))
    titleArtist = ImageDraw.Draw(colorImageOne)

    myFont = ImageFont.truetype("./fonts/Rubik.ttf", 40)
    titleArtist.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (textColor[0],textColor[1],textColor[2]))
    colorImageOne.save('ImageCache/firstColor.png')

    colorImageTwo = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[1].rgb))
    colorImageTwo.save('ImageCache/secondColor.png')


    #Combine Images

    background = Image.new('RGB', (colorImageOne.width, colorImageOne.height + colorImageTwo.height))
    background.paste(colorImageOne, (0, 0))
    background.paste(colorImageTwo, (0, colorImageOne.height))
    background.save('ImageCache/background.png')

    
    finalImage = Image.new('RGB', (width, height))
    background.paste(image, ((int(background.width/2) - int(image.width / 2)), int((background.height/2) - int(image.height / 2))))
    background.save("ImageCache/finalImage.png")

    return songTitle

def getColors():
    #Setup Background Colors
    colors = colorgram.extract('ImageCache/albumImage.png', 2)
    if len(colors) < 2:
        firstColor = colors[0]
        secondColor = colors[0]
    else:
        firstColor = colors[0]
        secondColor = colors[1]
    
    return([firstColor, secondColor])

def checkSong():
    f = open("src/songCheck.txt", "r")
    song = f.read()
    f.close()
    return song

if __name__ == "__main__":

    try:

        #start with initializations
        init()
        while 1:

            songTitle = get_song_name()

            if songTitle != checkSong():
                #change the song title in the file
                with open("src/songCheck.txt", "w") as f:
                    f.write(songTitle)
                    f.close()

                #generate and change the wallpaper
                albumImage()
                
                os.system(command + os.getcwd() + "/ImageCache/finalImage.png")

            t.sleep(5)

    except KeyboardInterrupt:
        #when the program is stopped, change the wallpaper back to the original one
        os.system(command + str(original_wallpaper))
        #clear songCheck.txt so that the next time the program is run, it will change the wallpaper
        with open("src/songCheck.txt", "w") as f:
            f.write("")
            f.close()