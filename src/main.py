import io
from types import ClassMethodDescriptorType
import requests, colorgram, os, platform
import time
import spotipy.util as util
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from spotipy.oauth2 import SpotifyOAuth
import random, json
from cachetools import TTLCache
import math
from urllib.parse import urlencode

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


cache = TTLCache(maxsize=100, ttl=3600)


#check if gnome is in dark mode or light mode

#set the command to change the wallpaper: it changes depending on the mode

#get the path of the original wallpaper
original_wallpaper = os.popen("gsettings get org.gnome.desktop.background picture-uri-dark").read()

def getEnvironment():
    """
    Get the environment of the user, and the command to change the wallpaper
    
    Returns:
        None: the environment and the command are stored in global variables"""
    global environment, command

    for env in availableEnvironment:
        result = os.popen(env['testCommand']).read().strip()
        if not result:
            environment, command = env['envName'], env['command']
            break

def get_token_refresh():
    """
    Get the Spotify refresh token from the cache file

    Returns:
        str: The Spotify refresh token
    """
    filename = f".cache-{username}"
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data['refresh_token']
    except:
        return None
    

def write_token_refresh(refresh_token):
    """
    Write the Spotify refresh token to the cache file

    Args:
        refresh_token (str): The Spotify refresh token to write to the cache file

    Returns:
        None: The Spotify refresh token is written to the cache file
    """
    filename = f".cache-{username}"
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            data['refresh_token'] = refresh_token
            with open(filename, 'w') as file:
                json.dump(data, file)
    except:
        return None
    

def write_token(spotify_token):
    """
    Write the Spotify token to the cache
    
    Args:
        spotify_token (str): The Spotify token to write to the cache file
        
    Returns:
        None: The Spotify token is written to the cache file"""
    filename = f".cache-{username}"
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            data['access_token'] = spotify_token
            with open(filename, 'w') as file:
                json.dump(data, file)
    except:
        return None


def token_refresh():
    """
    Refresh the Spotify token using the refresh token

    Returns:
        str: The new Spotify token
    """
    refresh_token = get_token_refresh()
    url = "https://accounts.spotify.com/api/token"

    if refresh_token:
        payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, headers=headers, data=urlencode(payload))

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the new access and refresh tokens from the response
            response_data = response.json()
            spotify_token = response_data.get('access_token')
            new_refresh_token = response_data.get('refresh_token', refresh_token)  # Use the same refresh token if a new one isn't provided

            # Here you would update your storage mechanism with the new tokens
            # Since Python scripts don't have direct access to browser's localStorage,
            # you need to adapt this part to your application's environment.
            print("New access token:", spotify_token)
            print("New refresh token:", new_refresh_token)

            # Write the new tokens to the cache
            write_token(spotify_token)
            write_token_refresh(new_refresh_token)

            return spotify_token

            
        else:
            print("Failed to refresh the token, status code:", response.status_code)
            print("Trying to authenticate again")
            spotify_authenticate()
            return 
    else:
        print("No refresh token found, trying to authenticate again")
        spotify_authenticate()
        return


def  init():
    """
    Initialize the program, by getting the credentials, the environment, and the original wallpaper

    Returns:
        None: the credentials, the environment, and the original wallpaper are stored in global variables"""
    
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




def spotify_authenticate():
    """
    Authenticate with the Spotify API using the credentials from the creds.txt file.
    The authentication token is stored in the global variable spotify_token.
    """
    # Get the Spotify access token for authentication
    global spotify_token
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, "https://www.google.com/")

    if token:
        spotify_token = token
    else:
        print("Couldn't get proper Spotify authentication")
        exit()



def get_variables():
    """
    Get the variables from the creds.txt file.

    Returns:
        dict: A dictionary containing the variables from the creds.txt file.

    """
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






def download_image(image_url):
    """
    Downloads an image from the given URL and stores its data in the cache.
    The image data is cached using the image URL as the key.
    
    Args:
        image_url (str): URL of the image to download.
    
    Returns:
        bytes: The image data, or None if the download fails.
    """
    
    if image_url in cache:
        return cache[image_url]
    
    try: 
        response = requests.get(image_url)
        response.raise_for_status()  # Check if the request was successful

        # Cache the image data
        image_data = response.content
        cache[image_url] = image_data

        #save the image in the ImageCache directory
        with open('ImageCache/albumImage.png', 'wb') as file:
            file.write(image_data)

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
            status = int(response.status_code)
            song_content = response.json()

            if status == 401:
                # Token has expired, reauthenticate
                spotify_token = token_refresh()
                print("Token refreshed")
                
                continue
            
            if status == 429:
                retry_after = int(response.headers.get('Retry-After', retry_delay))
                print(f"Rate limited. Retrying in {retry_after} seconds...")
                time.sleep(retry_after)
                continue

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


            if not all([name, artistName, imageUrl, songId]):
                print("Incomplete song information. Retrying...")
                time.sleep(retry_delay)
                continue

            return name, status, imageUrl, artistName, songId

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying in {retry_delay} seconds...")
             
            time.sleep(retry_delay)
        except KeyError as e:
            print(f"Missing expected data: {e}. Retrying...")
            time.sleep(retry_delay)  

    print("Maximum retries reached. Exiting function.")
    return None




def create_color_background(baseWidth, baseHeight, colors):
    """
    Create a background image with two colors.
    
    Args:
        baseWidth (int): The width of the background image.
        baseHeight (int): The height of the background image.
        colors (list): A list of two colors to use for the background.
        
    Returns:
        Image: A new background image with two colors."""
    colorImageOne = Image.new('RGB', (baseWidth, int(baseHeight / 2)), colors[0].rgb)
    colorImageTwo = Image.new('RGB', (baseWidth, int(baseHeight / 2)), colors[1].rgb)

    background = Image.new('RGB', (colorImageOne.width, colorImageOne.height + colorImageTwo.height))
    background.paste(colorImageOne, (0, 0))
    background.paste(colorImageTwo, (0, colorImageOne.height))

    return background

def albumImage(display, songTitle, songArtist, imageUrl):
    """
    Generate a wallpaper based on the album image and song details.
    
    Args:
        display (tuple): The dimensions of the display.
        songTitle (str): The title of the currently playing song.
        artistName (str): The name of the artist of the currently playing song.
        imageUrl (str): The URL of the song's cover image.
        
    Returns:
        None: The generated wallpaper is saved to the 'ImageCache' directory."""
    image = setup_album_image(display, imageUrl)
    text = generate_text_image(songTitle, artistName, getColors(imageUrl), display)

    background = create_color_background(int(display[0]), int(display[1]), getColors(imageUrl))

    paste_and_save_album_image(background, image, display, text)
    


def calculate_relative_luminance(color):
    """
    Calculate the relative luminance of a color using the formula:
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    
    Args:
        color (Color): A color object.
        
    Returns:
        float: The relative luminance of the color."""
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

def getColors(imageUrl):
    """
    Get the two most prominent colors from the album image.
    
    Returns:
        list: A list of two color objects extracted from the album image.
        """
    
    #retrieve the image from the cache
    image = get_image_from_cache(imageUrl)
    image = Image.open(io.BytesIO(image))
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
    
def get_image_from_cache(imageUrl):
    try:
        image =  cache[imageUrl]
        return image
    except KeyError:
        download_image(imageUrl)
        return cache[imageUrl]
    except:
        print("Error: couldn't get image from cache")
        return None
    
def resetSong():
    """
    Reset the song title in the file 'src/songCheck.txt'
    
    Returns:
        None: The file 'src/songCheck.txt' is reset.
    """
    with open("src/songCheck.txt", "w") as f:
        f.write("")
        f.close()



def setup_album_image(display, imageUrl):
    """
    Setup the album image for the wallpaper.
    
    Args:
        display (tuple): The dimensions of the display.
        imageUrl (str): The URL of the album image.
        
        Returns:
        Image: The album image, resized and saved to the 'ImageCache' directory.
        """
    width = int(int(display[0]) / 5)
    height = int(int(display[1]) / 2)

    image = get_image_from_cache(imageUrl)
    image = Image.open(io.BytesIO(image))

    wpercent = (width/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((width,hsize), Image.LANCZOS)
    image.save('ImageCache/albumImage.png')
    return image


def generate_gradient_image(colors, display):
    """
    Generate a gradient image based on the colors of the album image.
    
    Args:
        colors (list): A list of two color objects.
        display (tuple): The dimensions of the display.
        
    Returns:
        Image: A gradient image with the colors of the album image."""
    # Create a gradient image with the colors of the album image
    width = int(display[0])
    height = int(display[1])
    gradient = Image.new('RGB', (width, height))

    # Create a draw object
    draw = ImageDraw.Draw(gradient)

    # The first color will be the first color of the album image
    firstColor = colors[0].rgb
    # The second color will be the second color of the album image
    secondColor = colors[1].rgb

    # Draw the gradient
    for i in range(height):
        draw.line((0, i, width, i), fill = (int(firstColor[0] + (secondColor[0] - firstColor[0]) * i / height), int(firstColor[1] + (secondColor[1] - firstColor[1]) * i / height), int(firstColor[2] + (secondColor[2] - firstColor[2]) * i / height)))

    gradient.save('ImageCache/gradient.png')
    return gradient



def generate_text_image(songTitle, artistName, colors, display, positionX = 50, positionY = 50):
    """
    Generate a text image with the song title and artist name.
    
    Args:
        songTitle (str): The title of the currently playing song.
        artistName (str): The name of the artist of the currently playing song.
        colors (list): A list of two color objects.
        display (tuple): The dimensions of the display.
        positionX (int): The x-coordinate of the text.
        positionY (int): The y-coordinate of the text.
        
    Returns:
        Image: A new image with the song title and artist name, and transparent background."""
    width = int(display[0])
    height = int(display[1])
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
    draw.text((positionX,positionY), (songTitle + "\n" + artistName), font = myFont, fill = (textColor[0],textColor[1],textColor[2]))
    #save the text image
    return text

def paste_and_save_album_image(bg, cover, display, text):
    """
    Paste the album image in the center of the background image and save the final image.

    Args:
        bg (Image): The background image.
        cover (Image): The album image.
        display (tuple): The dimensions of the display.
        text (Image): The text image.
    """

    width = int(display[0])
    height = int(display[1])
    # Paste the album image, bigger of 120% of the size, in the center of the gradient image
    bg.paste(cover, ((int(bg.width/2) - int(cover.width / 2)), int((bg.height/2) - int(cover.height / 2))))

    #save the final image

    background = Image.new('RGB', (width, height))
    background.paste(bg, (0, 0))
    background.paste(text, (0, 0), mask = text)
    background.save("ImageCache/finalImage.png")

    return background



def gradient(songTitle, imageUrl, artistName):
    """
    Generate a gradient wallpaper based on the song details.

    Args:
        songTitle (str): The title of the currently playing song.
        status (str): The status of the song (e.g., "playing" or "paused").
        imageUrl (str): The URL of the song's cover image.
        artistName (str): The name of the artist of the currently playing song.
        songId (str): The ID of the currently playing song.

    Returns:
        None: The generated wallpaper is saved to the 'ImageCache' directory.
    """
    # Retrieve and set-up the image from the cache using imageUrl as the key
    image = setup_album_image(display, imageUrl)


    # Create a gradient image with the colors of the album image, using the dimensions of the display
    gradient = generate_gradient_image(getColors(imageUrl), display)

    #generate the text image
    text = generate_text_image(songTitle, artistName, getColors(imageUrl), display)

    paste_and_save_album_image(gradient, image, display, text)


def resize_and_center_image(image, target_width, target_height):
    """
    Resizes an image to a target width, and centers it vertically.

    Args:
        image (Image): The image to resize.
        target_width (int): The target width of the image.
        target_height (int): The target height of the image.

    Returns:
        Image: The resized and centered image.
    """
    # Resize with preserved aspect ratio
    aspect_ratio = image.width / image.height
    new_height = target_height
    new_width = int(int(aspect_ratio) * int(new_height))
    resized_image = image.resize((int(new_width), int(new_height)), Image.LANCZOS)

    target_width = int(target_width)
    # Center the image vertically
    if new_width > target_width:
        x_offset = (new_width - target_width) // 2
        resized_and_centered_image = resized_image.crop((x_offset, 0, x_offset + target_width, new_height))
    else:
        resized_and_centered_image = resized_image

    return resized_and_centered_image


def create_blurred_background(cover_image_data, display_dimensions, blur_radius=20):
    """
    Creates a blurred background image from the cover image data.

    Args:
        cover_image_data (bytes): Image data as bytes.
        display_dimensions (tuple): Dimensions of the display (width, height).
        blur_radius (int): Radius of the Gaussian blur filter.

    Returns:
        Image: A new image with a blurred background and the album cover centered.

    """
    try:
        image = Image.open(io.BytesIO(cover_image_data))


        # Resize, crop, and blur the album image
        base_width, base_height = display_dimensions
        resized_image = resize_and_center_image(image, int(base_width)*2, int(base_height)*2)
        blurred_image = resized_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        # Paste the cover image in the center
        cover_image = Image.open(io.BytesIO(cover_image_data))
        cover_width, cover_height = cover_image.size
        cover_image = cover_image.resize((int(1.2 * cover_width), int(1.2 * cover_height)), Image.LANCZOS)
        x_position = (blurred_image.width - cover_image.width) // 2
        y_position = (blurred_image.height - cover_image.height) // 2
        blurred_image.paste(cover_image, (x_position, y_position))

        return blurred_image
    except Exception as e:
        print(f"Error creating blurred background: {e}")
        return None

def blurred(cover_url, display_dimensions):
    """
    Main function to generate a blurred background with the album cover centered.

    Args:
        cover_url (str): URL of the album cover image.
        display_dimensions (tuple): Dimensions of the display (width, height).

    Returns:
        None: The generated wallpaper is saved to the 'ImageCache' directory.
    """
    cover_image_data = get_image_from_cache(cover_url)  # Make sure this returns image data as bytes
    if cover_image_data is None:
        print("Failed to retrieve cover image.")
        return

    final_image = create_blurred_background(cover_image_data, display_dimensions)
    if final_image:
        final_image_path = "ImageCache/finalImage.png"
        final_image.save(final_image_path)
        return True
    else:
        print("Failed to create blurred background.")
        return False





def get_audio_analysis(song_id):
    """
    Get the audio analysis for a song from the Spotify API.

    Args:
        song_id (str): The ID of the song.

    Returns:
        dict or None: A dictionary with the audio analysis data, or None if the request fails.
    """


    url = f"https://api.spotify.com/v1/audio-analysis/{song_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {spotify_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        #save the audio analysis in a file
        with open("src/audioAnalysis.json", "w") as f:
            f.write(json.dumps(response.json()))
            f.close()
        return response.json()
    else:

        print("Error during request")
        return None

def extract_loudness_data(audio_analysis, duration, sample_points=100):
    """
    Extracts loudness data from the audio analysis.

    Args:
        audio_analysis (dict): Audio analysis data from the Spotify API.
        duration (float): Duration of the song in seconds.
        sample_points (int): Number of sample points for the waveform.

    Returns:
        list: A list of normalized loudness levels for the waveform.
    """
    segments = [{
        'start': segment['start'] / duration,
        'duration': segment['duration'] / duration,
        'loudness': 10 ** (segment['loudness_max'] / 20)  # Adjusted for perceptual loudness
    } for segment in audio_analysis['segments']]

    # Simplify to a fixed number of sample points for the waveform
    loudness_levels = [0] * sample_points
    for segment in segments:
        start_index = int(segment['start'] * sample_points)
        end_index = min(sample_points, int((segment['start'] + segment['duration']) * sample_points))
        for i in range(start_index, end_index):
            loudness_levels[i] = max(loudness_levels[i], segment['loudness'])

    # Normalize loudness levels
    max_loudness = max(loudness_levels, default=1)
    return [level / max_loudness for level in loudness_levels]



def generate_waveform_image(levels, display_dimensions, colors):
    """
    Generates a waveform image based on normalized loudness levels.

    Args:
        levels (list): Normalized loudness levels from audio analysis.
        display_dimensions (tuple): Dimensions of the display (width, height).
        colors (tuple): Tuple containing two RGB colors (background, waveform).

    Returns:
        PIL.Image: An image object with the waveform.
    """
    width, height = display_dimensions
    baseHeight = height  # Assuming baseHeight is used for normalization

    # Create a new image with the dimensions of the display
    image = Image.new('RGB', (width, height), colors[0].rgb)

    # Generate schema for the waveform
    schema = [(int(i / 100 * width), int((1/2 + level/2) * height)) for i, level in enumerate(levels)]
    invertedSchema = [(int(i / 100 * width), int((1/2 - level/2) * height)) for i, level in enumerate(levels)]

    # Normalize the schema to the height of the screen
    schema = [(x, int(y * (baseHeight / height))) for x, y in schema]
    invertedSchema = [(x, int(y * (baseHeight / height))) for x, y in invertedSchema]

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Draw the waveform
    for i in range(len(schema)):
        start_point = schema[i]
        end_point = (invertedSchema[i][0], schema[i][1])  # Adjusted to match start and end y-coordinates

        if abs(start_point[1] - invertedSchema[i][1]) < 32:
            draw.rounded_rectangle([invertedSchema[i][0], height/2 - 16, start_point[0]+16, height/2 + 16], fill=colors[1].rgb, radius=8)
        else:
            draw.rounded_rectangle([invertedSchema[i][0], invertedSchema[i][1], start_point[0]+16, start_point[1]], fill=colors[1].rgb, radius=8)
    # Resize the image to 60% of its size, both horizontally and vertically
    resized_image = image.resize((int(width * 0.6), int(height * 0.6)), Image.LANCZOS)


    return resized_image




def waveform(song_id, display, imageUrl, artistName, songTitle):
    """
    Generate a wallpaper with a waveform based on the audio analysis of the song.

    Args:
        song_id (str): The ID of the song.
        display (tuple): The dimensions of the display.
        imageUrl (str): The URL of the song's cover image.
        artistName (str): The name of the artist of the currently playing song.
        songTitle (str): The title of the currently playing song.

    Returns:
        None: The generated wallpaper is saved to the 'ImageCache' directory.
    """

    # Get audio analysis for the song
    audio_analysis = get_audio_analysis(song_id)
    if audio_analysis is None:
        print("Failed to retrieve audio analysis.")
        return
    
    loudness = extract_loudness_data(audio_analysis, audio_analysis['track']['duration'])
    width, height = display

    loudness = [loud * 0.75 for loud in loudness]
    
    # Generate the waveform image
    waveform_image = generate_waveform_image(loudness, (int(width), int(height)), getColors(imageUrl))
    # Generate the text image in the low-left corner
    text_image = generate_text_image(songTitle, artistName, getColors(imageUrl), display, positionX=50, positionY=int(height) - 150)
    # Create a new image with the first color of the album image as the background
    final_image = Image.new('RGB', (int(width), int(height)), getColors(imageUrl)[0].rgb)
    # Paste the waveform image in the center of the background image, centered vertically and horizontally
    final_image.paste(waveform_image, ((int(final_image.width/2) - int(waveform_image.width / 2)), int((final_image.height/2) - int(waveform_image.height / 2))))
    # Paste the text image 
    final_image.paste(text_image, (0, 0), mask=text_image)

    # Save the image
    final_image.save("ImageCache/finalImage.png")
    


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

            if songId != checkSong():
                # Download the image and get its local path
                download_image(imageUrl)

                #change the song title in the file
                with open("src/songCheck.txt", "w") as f:
                    f.write(songId)
                    f.close()

                #choose randomly between the different modes, and generate the wallpaper
                mode = random.choice(["gradient", "blurred", "waveform", "albumImage"])
                
                if mode == "gradient":
                    gradient(songTitle, imageUrl, artistName)

                elif mode == "blurred":
                    if blurred(imageUrl, display) == False:
                        # If the blurred background fails, retry the entire process
                        resetSong()
                        continue

                elif mode == "waveform":
                    waveform(songId, display, imageUrl, artistName, songTitle)

                    
                elif mode == "albumImage":
                    albumImage(display, songTitle, artistName, imageUrl)
                    
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
    #if the program is stopped with any other method, change the wallpaper back to the original one
    except:
        os.system(command + str(original_wallpaper))
        #clear songCheck.txt so that the next time the program is run, it will change the wallpaper
        resetSong()
        raise