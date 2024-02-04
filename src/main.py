from types import ClassMethodDescriptorType
import requests, colorgram, os, platform
import time
import spotipy.util as util
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from spotipy.oauth2 import SpotifyOAuth
import random, json
from cachetools import TTLCache
import math

# Get creds please enter your creds in creds.txt

global spotify_token, client_id, client_secret, username, display, original_wallpaper, command, mode, environment
client_id = ""
client_secret = ""
spotify_token = ""
username = ""
scope = "user-read-currently-playing"
display = ""
cacheOn = True
environment = ''
#set up an array of available environments and commando to test
availableEnvironment = [
    {'envName': 'gnome',
     'testCommand' : 'gnome-session',
     'command' : 'gsettings set org.gnome.desktop.background picture-uri ' if ('dark' if 'dark' in (os.popen("gsettings get org.gnome.desktop.interface gtk-theme").read()) else 'light') == 'light' else 'gsettings set org.gnome.desktop.background picture-uri-dark '
     }]

#set 'cacheOn = False' in the previous line if you don't want to use cache

cache = TTLCache(maxsize=100, ttl=3600)


#check if gnome is in dark mode or light mode

#set the command to change the wallpaper: it changes depending on the mode

#get the path of the original wallpaper
original_wallpaper = os.popen("gsettings get org.gnome.desktop.background picture-uri-dark").read()

def getEnvironment():
    global environment, command

    for env in availableEnvironment:
        result = os.popen(env['testCommand']).read().strip()
        if not result:
            environment, command = env['envName'], env['command']
            break

def  init():
    # Get variables from the credentials file
    datadict = get_variables()
    #check if the environment is available
    getEnvironment()

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
    display = os.popen("xrandr").read().split("\n")[2].split()[0].split("x")
    #display = ['yourWidth', 'yourHeight']
    # DON'T REMOVE THE ''

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
            time.sleep(2)
            get_song_id()

        name = song_content['item']['name']

        artistName = song_content['item']['album']['artists'][0]['name']
        imageUrl = song_content['item']['album']['images'][1]['url']

        if not name or not artistName or not imageUrl:
            time.sleep(2)
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
        time.sleep(5)
        get_song_id()
    except ValueError:
        print("Error: looks like no song is playing")
        print("Waiting for song to be played.")
        time.sleep(5)
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



from cachetools import TTLCache
import requests
import time
import os

# Assuming the image cache is defined globally
image_cache = TTLCache(maxsize=100, ttl=3600)  # Adjust size and ttl as needed

def download_image(image_url):
    """
    Downloads an image from the given URL and stores its data in the cache.
    The image data is cached using the image URL as the key.
    
    Args:
        image_url (str): URL of the image to download.
    
    Returns:
        bytes: The image data, or None if the download fails.
    """
    if image_url in image_cache:
        print("Image found in cache. Returning cached image data.")
        return image_cache[image_url]
    
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check if the request was successful

        # Cache the image data
        image_data = response.content
        image_cache[image_url] = image_data
        
        return image_data
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")
        return None


def get_song_details(spotify_token, retry_delay=2, max_retries=3):
    """
    Fetches and downloads details of the currently playing song from Spotify, including downloading the cover image.
    
    Args:
        spotify_token (str): Spotify API token.
        retry_delay (int): Time in seconds to wait before retries.
        max_retries (int): Maximum number of retries for the request.
    
    Returns:
        tuple or None: Returns a tuple with song details (name, status, local image path, artistName, songId)
                       or None if the request fails or data is incomplete.
    """
    header = {"Authorization": f"Bearer {spotify_token}"}
    url = "https://api.spotify.com/v1/me/player/currently-playing"

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=header)
            response.raise_for_status()  # This will raise an error for HTTP error responses

            song_content = response.json()

            # Check if the response has the necessary information
            if 'item' not in song_content or not song_content['item']:
                print("No song information found. Retrying...")
                time.sleep(retry_delay)
                continue

            status = "paused" if 'is_playing' not in song_content or not song_content['is_playing'] else "playing"
            item = song_content['item']
            name = item.get('name')
            artistName = item['album']['artists'][0].get('name')
            imageUrl = item['album']['images'][0].get('url')  # Using the first image (usually the largest)
            songId = item.get('id')

            # Download the image and get its local path
            image_path = download_image(imageUrl)

            if not all([name, artistName, imageUrl, songId, image_path]):
                print("Incomplete song information or failed to download image. Retrying...")
                time.sleep(retry_delay)
                continue

            return name, status, image_path, artistName, songId

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except KeyError as e:
            print(f"Missing expected data: {e}. Retrying...")
            time.sleep(retry_delay)

    print("Maximum retries reached. Exiting function.")
    return None


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


def calculate_relative_luminance(color):
    r, g, b = color.rgb

    # Calculate relative luminance using the specified formula
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance

def calculate_contrast_ratio(color1, color2):
    # Calculate relative luminance for both colors
    luminance1 = calculate_relative_luminance(color1)
    luminance2 = calculate_relative_luminance(color2)

    # Ensure that the lighter color's luminance is in luminance1
    if luminance2 > luminance1:
        luminance1, luminance2 = luminance2, luminance1

    # Calculate contrast ratio with "+ 0.05" for adjustment
    contrast_ratio = (luminance1 + 0.05) / (luminance2 + 0.05)
    return contrast_ratio

def getColors():
    # Setup Background Colors
    colors = colorgram.extract('ImageCache/albumImage.png', 13)

    if len(colors) < 2:
        # In this case, the function will return
        return [colors[0], colors[0]]

    # Check if colors are too similar
    for i in range(1, len(colors)):
        if calculate_contrast_ratio(colors[0], colors[i]) >= 2:
            # Colors are different enough, so return them
            return [colors[0], colors[i]]
    else:
        return [colors[0], colors[1]]
    # For loop will end only if we run out of colors, so return the first two


def checkSong():
    """
    Get the song title from the file 'src/songCheck.txt'
    
    Returns:
        str: The song title from the file.
    """

    with open("src/songCheck.txt", "r") as f:
        return f.read()


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
    gradient.save('ImageCache/gradientime.png')

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
    text.save('ImageCache/textime.png')



    # paste the album image, bigger of 120% of the size, in the center of the gradient image
    gradient.paste(image, ((int(gradient.width/2) - int(image.width / 2)), int((gradient.height/2) - int(image.height / 2))))
    # save the image
    gradient.save("ImageCache/finalImage.png")

    

    # paste the text image in a layer on top of the background image
    background = Image.new('RGB', (width, height))
    background.paste(Image.open("ImageCache/finalImage.png"), (0, 0))
    background.paste(Image.open("ImageCache/textime.png"), (0, 0), mask = Image.open("ImageCache/textime.png"))
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

def map_range(value, from_min, from_max, to_min, to_max):
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min

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
    'loudness': 10 ** (segment['loudness_max'] /10)
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
    
    
    #create a new image with the dimensions of the display
    width = int(display[0])
    height = int(display[1])
    image = Image.new('RGB', (width, height), colors[0].rgb)


    #create the schema for the waveform
    schema = []

    invertedSchema = []

    schema = [(int(i / 100 * width), int((1/2 + levels[i]/2) * height)) for i in range(100)]
    
    invertedSchema = [(int(i / 100 * width), int((1/2 - levels[i]/2) * height)) for i in range(100)]


    #normalize the schema to the height of the screen
    schema = [(x, int(y * (baseHeight / height))) for x, y in schema]
    invertedSchema = [(x, int(y * (baseHeight / height))) for x, y in invertedSchema]

    #create a draw object
    draw = ImageDraw.Draw(image)

    #draw a single line that starts from the y coordinate of the first point of the schema, and ends at the y coordinate of the point of the inverted schema with the same x coordinate

    for i in range(len(schema)):
        #draw.line((schema[i][0], schema[i][1], invertedSchema[i][0], invertedSchema[i][1]), fill = colors[1].rgb, width = 15)
        if (schema[i][1] - invertedSchema[i][1] < 32):
            draw.rounded_rectangle((invertedSchema[i][0], height/2 - 16, schema[i][0]+16, height/2 + 16), fill = colors[1].rgb, radius= 8)
        else:
            draw.rounded_rectangle((invertedSchema[i][0], invertedSchema[i][1], schema[i][0]+16, schema[i][1]), fill = colors[1].rgb, radius= 8)


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
    text.save('ImageCache/textime.png')
    
    #paste the text image vertically centered and lower than the waveform image
    tmp.paste(Image.open("ImageCache/textime.png"), ((int(tmp.width/2) - int(Image.open("ImageCache/textime.png").width / 2), int((tmp.height/2) + int(image.height / 2))))    )

    #save the image
    tmp.save("ImageCache/finalImage.png")

if __name__ == "__main__":

    try:

        #start with initializations
        init()
        prev_status = ''
        while True:

            #check if the song has been paused
            song_details = get_song_details(spotify_token)

            if song_details is None:
                print("Failed to retrieve song details. Trying again...")
                time.sleep(5)  # Wait a bit before retrying
                continue

            songTitle, status, imageUrl, artistName, songId = song_details


            if status == "paused":
                #restore the original wallpaper
                os.system(command + str(original_wallpaper))
                time.sleep(5)
                prev_status = "paused"
                continue

            if status == "playing" and prev_status == "paused":
                #if the song has been paused and then resumed, change the wallpaper
                prev_status = "playing"
                os.system(command + os.getcwd() + "/ImageCache/finalImage.png")
                time.sleep(5)
                continue

            if songTitle != checkSong():
                #change the song title in the file
                with open("src/songCheck.txt", "w") as f:
                    f.write(songTitle)
                    f.close()

                #choose randomly between the different modes, and generate the wallpaper
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

            time.sleep(5)

    except KeyboardInterrupt:
        #when the program is stopped, change the wallpaper back to the original one
        os.system(command + str(original_wallpaper))
        #clear songCheck.txt so that the next time the program is run, it will change the wallpaper
        with open("src/songCheck.txt", "w") as f:
            f.write("")
            f.close()
