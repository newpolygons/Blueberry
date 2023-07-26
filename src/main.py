from types import ClassMethodDescriptorType
import requests, colorgram, os, platform
import time as t
import spotipy.util as util
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from spotipy.oauth2 import SpotifyOAuth
import random, json
from cachetools import TTLCache
import math

# Get creds please enter your creds in creds.txt

global spotify_token, client_id, client_secret, username, display, original_wallpaper, command, mode
client_id = ""
client_secret = ""
spotify_token = ""
username = ""
scope = "user-read-currently-playing"
display = ""
cacheOn = True
#set 'cacheOn = False' in the previous line if you don't want to use cache

cache = TTLCache(maxsize=100, ttl=3600)


#check if gnome is in dark mode or light mode
mode = 'dark' if 'dark' in (os.popen("gsettings get org.gnome.desktop.interface gtk-theme").read()) else 'light'

#set the command to change the wallpaper: it changes depending on the mode
command = 'gsettings set org.gnome.desktop.background picture-uri ' if mode == 'light' else 'gsettings set org.gnome.desktop.background picture-uri-dark '

#get the path of the original wallpaper
original_wallpaper = os.popen("gsettings get org.gnome.desktop.background picture-uri-dark").read()


def  init():
    # Get variables from the credentials file
    datadict = get_variables()

    #check if 'src/songCheck.txt' exists, if not create it
    if not os.path.exists("src/songCheck.txt"):
        f = open("src/songCheck.txt", "w")
        f.write("")
        f.close()

    #check if 'ImageCache' directory exists, if not create it
    if not os.path.exists("ImageCache"):
        os.mkdir("ImageCache")

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
    global cacheOn

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

        if not name or not artistName or not imageUrl:
            t.sleep(2)
            get_song_id()

        #save the id of the album which contains the song
        albumID = song_content['item']['album']['id']
        # save the image of the song using the album ID as ID, so songs from the same album will have the same image
        if albumID not in cache and cacheOn:
            cache[albumID] = imageUrl
            image = requests.get(imageUrl)
            with open('ImageCache/albumImage.png', 'wb') as file:
                file.write(image.content)
        else:
            image = requests.get(cache[albumID])
            
            with open('ImageCache/albumImage.png', 'wb') as file:
                file.write(image.content)


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
    header = {
        "Authorization": "Bearer {}".format(spotify_token)
    }
    get_id = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=header)

    song_content = get_id.json()

    #check if the song is paused
    if not song_content['is_playing']:
        status = "paused"
    else:
        status = "playing"
    
    id = song_content['item']['id']
    # If the ID is not available, wait for 2 seconds and retry getting the song ID
    if not id:
        t.sleep(2)
        get_song_id()
    name = song_content['item']['name']
    artistName = song_content['item']['album']['artists'][0]['name']
    imageUrl = song_content['item']['album']['images'][1]['url']
    if not name:
        t.sleep(2)
        get_song_name()
    return name, status




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
    image = Image.open("ImageCache/albumImage.png")
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
     
    colorImageOne = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[0].rgb))
    titleArtist = ImageDraw.Draw(colorImageOne)

    myFont = ImageFont.truetype("./fonts/Rubik.ttf", 40)
    titleArtist.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (textColor[0],textColor[1],textColor[2]))

    colorImageTwo = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[1].rgb))


    #Combine Images

    background = Image.new('RGB', (colorImageOne.width, colorImageOne.height + colorImageTwo.height))
    background.paste(colorImageOne, (0, 0))
    background.paste(colorImageTwo, (0, colorImageOne.height))

    
    finalImage = Image.new('RGB', (width, height))
    background.paste(image, ((int(background.width/2) - int(image.width / 2)), int((background.height/2) - int(image.height / 2))))
    background.save("ImageCache/finalImage.png")


def getColors():
    #Setup Background Colors
    colors = colorgram.extract('ImageCache/albumImage.png', 2)
    if len(colors) < 2:
        firstColor = colors[0]
        secondColor = colors[0]
    else:
        firstColor = colors[0]
        secondColor = colors[1]

    #check if colors are too similar
    if abs(firstColor.rgb[0] - secondColor.rgb[0]) < 10 and abs(firstColor.rgb[1] - secondColor.rgb[1]) < 10 and abs(firstColor.rgb[2] - secondColor.rgb[2]) < 10:
        secondColor = getThirdColor()
    
    return([firstColor, secondColor])

def getThirdColor():
    #Setup Background Colors
    colors = colorgram.extract('ImageCache/albumImage.png', 3)
    if len(colors) < 3:
        thirdColor = colors[0]
    else:
        thirdColor = colors[2]
    
    return(thirdColor)

def checkSong():
    f = open("src/songCheck.txt", "r")
    song = f.read()
    f.close()
    return song


def gradient():

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
    image = Image.open("ImageCache/albumImage.png")
    wpercent = (width/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((width,hsize), Image.LANCZOS)
    image.save('ImageCache/albumImage.png')
    
    # Get the colors of the album image
    colors = getColors()

    # Create a gradient image with the colors of the album image

    # use the dimensions of the display

    width = int(display[0])
    height = int(display[1])

    # create a new image with the dimensions of the display
    gradient = Image.new('RGB', (width, height))

    # create a draw object
    draw = ImageDraw.Draw(gradient)

    # the first color will be the first color of the album image
    firstColor = colors[0].rgb
    # the second color will be the second color of the album image
    secondColor = colors[1].rgb

    # draw the gradient
    for i in range(height):
        draw.line((0, i, width, i), fill = (int(firstColor[0] + (secondColor[0] - firstColor[0]) * i / height), int(firstColor[1] + (secondColor[1] - firstColor[1]) * i / height), int(firstColor[2] + (secondColor[2] - firstColor[2]) * i / height)))

    # save the gradient image
    gradient.save('ImageCache/gradient.png')

    #generate the text image
    
    # Setup Text: check if the first color is too light or too dark
    textColor = colors[0].rgb

    #if the color is too light, make the text black, otherwise make it white
    if (textColor[0]*0.299 + textColor[1]*0.587 + textColor[2]*0.114) > 186:
        textColor = (int(0), int(0), int(0))
    else:
        textColor = (int(255), int(255), int(255))

    #create a new image with the name of the song and the artist, and transparent background
    text = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    #create a draw object
    draw = ImageDraw.Draw(text)
    #set the font
    myFont = ImageFont.truetype("./fonts/Rubik.ttf", 40)
    #draw the text
    draw.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (textColor[0],textColor[1],textColor[2]))
    #save the text image
    text.save('ImageCache/text.png')



    # paste the album image, bigger of 120% of the size, in the center of the gradient image
    gradient.paste(image, ((int(gradient.width/2) - int(image.width / 2)), int((gradient.height/2) - int(image.height / 2))))
    # save the image
    gradient.save("ImageCache/finalImage.png")

    

    # paste the text image in a layer on top of the background image
    background = Image.new('RGB', (width, height))
    background.paste(Image.open("ImageCache/finalImage.png"), (0, 0))
    background.paste(Image.open("ImageCache/text.png"), (0, 0), mask = Image.open("ImageCache/text.png"))
    background.save("ImageCache/finalImage.png")


def blurred():
    #this function will create a background image with the blurred album image, filling the whole screen, and the cover image in the center
    try:
        # Get the song information including title and artist
        songInformation = get_song_id()
        songTitle = songInformation[1]
        songArtist = songInformation[2]
    except:
        #clean the text file
        with open("src/songCheck.txt", "w") as f:
            f.write("")
            f.close()
        return

    # Setup Album Image
    width = int(display[0]) // 5
    height = int(display[1]) // 2

    baseWidth = int(display[0])
    baseHeight = int(display[1])

    # Resize the album image to the width of the screen
    image = Image.open("ImageCache/albumImage.png")
    wpercent = baseWidth / float(image.size[0])
    hsize = int(float(image.size[1]) * wpercent)
    resized_image = image.resize((baseWidth, hsize), Image.LANCZOS)

    #center the image vertically
    resized_image = resized_image.crop((0, int((resized_image.height / 2) - (baseHeight / 2)), baseWidth, int((resized_image.height / 2) + (baseHeight / 2))))

    # Crop and blur the image
    cropped_image = resized_image.crop((0, 0, baseWidth, baseHeight))
    blurred_image = cropped_image.filter(ImageFilter.GaussianBlur(radius=20))

    # Resize the blurred image to the height of the screen, then center it
    wpercent = baseHeight / float(blurred_image.size[1])
    wsize = int(float(blurred_image.size[0]) * wpercent)
    final_image = blurred_image.resize((wsize, baseHeight), Image.LANCZOS)
    final_image = final_image.crop((int((final_image.width / 2) - (baseWidth / 2)), 0, int((final_image.width / 2) + (baseWidth / 2)), baseHeight))

    # open the cover image, resize it to 120% of the size, and paste it in the center of the blurred image
    cover_image = Image.open("ImageCache/albumImage.png")
    wpercent = 1.2 * width / float(cover_image.size[0])
    hsize = int(float(cover_image.size[1]) * wpercent)
    cover_image = cover_image.resize((int(width * 1.2), hsize), Image.LANCZOS)
    final_image.paste(cover_image, ((int(final_image.width / 2) - int(cover_image.width / 2)), int((final_image.height / 2) - int(cover_image.height / 2))))

    # save the final image
    final_image.save("ImageCache/finalImage.png")


def get_audio_analysis(song_id):
    url = f"https://api.spotify.com/v1/audio-analysis/{song_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {spotify_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open('track.json', 'wb') as file:
            file.write(response.content)
    else:
        print("Error during request")


def waveform():
    #generate the waveform image, using the track ID and colors of the album image
    try:
        # Get the song information including title and artist
        songInformation = get_song_id()
        songTitle = songInformation[1]
        songArtist = songInformation[2]
        songID = songInformation[0]
    except:
        return

    width = int(display[0]) // 5
    height = int(display[1]) // 2

    baseWidth = int(display[0])
    baseHeight = int(display[1])


    get_audio_analysis(songID)

    #What I want to do is greatly simplify this data to only include an array of loudness levels from 0 to 1. I’ll then use this array of levels to generate a waveform

    #open the json file
    with open('track.json') as f:
        data = json.load(f)

    duration = data['track']['duration']

    #map the the segments data to only include the start, duration ad loudness properties
    segments = lambda data, duration: [{
    'start': segment['start'] / duration,
    'duration': segment['duration'] / duration,
    'loudness': 1 - (min(max(segment['loudness_max'], -35), 0) / -35)
    } for segment in data['segments']]


    #find the maximum loudness
    max_loudness = max([segment['loudness'] for segment in segments(data, duration)])

    #find the minimum loudness
    min_loudness = min([segment['loudness'] for segment in segments(data, duration)])

    #get the colors of the album image
    colors = getColors()

    levels = []
    i = 0
    while i < 100:
        s = 0
        for segment in segments(data, duration):
            if segment['start'] < i / 100 < segment['start'] + segment['duration']:
                s += segment['loudness']
        #if a level is too high or too low, set it to the mean of the previous and the next level
        levels.append((s / max_loudness) / 2)
        i += 1    

    #if a level is too low, set it to the mean of the previous and the next level
    for i in range(99):
        if levels[i] < 0.5 and levels[i + 1] < 0.5 and levels[i -1] < 0.5:
            levels[i] = (levels[i - 1] + levels[i + 1]) / 2

    #if a level is too high, set it to the mean of the previous and the next level
    for i in range(99):
        if levels[i] > 0.33 and levels[i + 1] > 0.33 and levels[i -1 ] > 0.33:
            levels[i] = (levels[i - 1] + levels[i + 1]) / 2


    
    #create a new image with the dimensions of the display
    width = int(display[0])
    height = int(display[1])
    image = Image.new('RGB', (width, height), colors[0].rgb)


    #create the schema for the waveform
    schema = []

    invertedSchema = []

    for i in range(100):
        schema.append((int(i / 100 * width), int((1 - levels[i]) * height)))

    #invert the schema by x-axis
    for i in range(100):
        invertedSchema.append((int(i / 100 * width), int(levels[i] * height)))

    #normalize the schema to the height of the screen
    for i in range(100):
        schema[i] = (schema[i][0], int(schema[i][1] * (baseHeight / height)))
        invertedSchema[i] = (invertedSchema[i][0], int(invertedSchema[i][1] * (baseHeight / height)))

    
    #create a draw object
    draw = ImageDraw.Draw(image)

    #draw a single line that starts from the y coordinate of the first point of the schema, and ends at the y coordinate of the point of the inverted schema with the same x coordinate

    for i in range(100):
        draw.line((schema[i][0], schema[i][1], invertedSchema[i][0], invertedSchema[i][1]), fill = colors[1].rgb, width = 15, joint = 'curve')

    #resize the image to 60% of the size, both horizontally and vertically
    image = image.resize((int(width * 0.6), int(height * 0.6)), Image.LANCZOS)

    #tmp will be the final image, with the background color of the first color of the album image
    tmp = Image.new('RGB', (width, height), colors[0].rgb)

    #paste the waveform image in the center of the background image, centered vertically and horizontally
    tmp.paste(image, ((int(tmp.width/2) - int(image.width / 2)), int((tmp.height/2) - int(image.height / 2))))

    #TEXT
    #create a new image with the name of the song and the artist, and color of the first color of the album image as background
    text = Image.new('RGBA', (width, height), (colors[0].rgb))
    #create a draw object
    draw = ImageDraw.Draw(text)
    #set the font
    myFont = ImageFont.truetype("./fonts/Rubik.ttf", 40)
    #draw the text
    draw.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (colors[1].rgb))
    #save the text image
    text.save('ImageCache/text.png')
    
    #paste the text image vertically centered and lower than the waveform image
    tmp.paste(Image.open("ImageCache/text.png"), ((int(tmp.width/2) - int(Image.open("ImageCache/text.png").width / 2), int((tmp.height/2) + int(image.height / 2))))    )

    #save the image
    tmp.save("ImageCache/finalImage.png")

if __name__ == "__main__":

    try:

        #start with initializations
        init()
        while 1:

            #check if the song has been paused
            songTitle, status = get_song_name()

            if status == "paused":
                #restore the original wallpaper
                os.system(command + str(original_wallpaper))
                t.sleep(5)
                continue

            if songTitle != checkSong():
                #change the song title in the file
                with open("src/songCheck.txt", "w") as f:
                    f.write(songTitle)
                    f.close()

                #choose randomly between tthe different modes, and generate the wallpaper
                mode = random.choice(["gradient", "blurred", "waveform", "albumImage"])
                
                if mode == "gradient":
                    gradient()
                elif mode == "blurred":
                    blurred()
                elif mode == "waveform":
                    waveform()
                elif mode == "albumImage":
                    albumImage()

                #change the wallpaper                           
                os.system(command + os.getcwd() + "/ImageCache/finalImage.png")

            t.sleep(5)

    except KeyboardInterrupt:
        #when the program is stopped, change the wallpaper back to the original one
        os.system(command + str(original_wallpaper))
        #clear songCheck.txt so that the next time the program is run, it will change the wallpaper
        with open("src/songCheck.txt", "w") as f:
            f.write("")
            f.close()