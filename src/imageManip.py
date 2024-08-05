import colorgram
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def albumImage(mode, songInformation, display):
    try:
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
    #Adding rounded corners and drop shadow to images
    
    image = add_corners(image, 20)
    image.save('ImageCache/newCover.png')
    
    if (mode == 'block'):
        blockMode(baseWidth, baseHeight, songTitle, songArtist, width, height, image)
    elif (mode == "gradient"):
        gradientMode(baseWidth, baseHeight, songTitle, songArtist, width, height, image)

    return songTitle



def getColors():
#Setup Background Colors
    colors = colorgram.extract('ImageCache/newCover.png', 2)
    if len(colors) < 2:
        firstColor = colors[0]
        secondColor = colors[0]
    else:
        firstColor = colors[0]
        secondColor = colors[1]
    
    return([firstColor, secondColor])


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def get_gradient_2d(start, stop, width, height, is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
    result = np.zeros((height, width, len(start_list)), dtype=float)

    for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)

    return result


def blockMode(baseWidth, baseHeight, songTitle, songArtist, width, height, image):
    #we could pass all this variables as a list but this is better for understanding what data is going where at a glance.
    colors = getColors()

    colorImageOne = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[0].rgb))
    titleArtist = ImageDraw.Draw(colorImageOne)

    myFont = ImageFont.truetype("fonts/CreamCake.otf", 60)#40)
    titleArtist.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (colors[1].rgb))
    colorImageOne.save('ImageCache/firstColor.png')

    colorImageTwo = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[1].rgb))
    colorImageTwo.save('ImageCache/secondColor.png')


    #Combine Images

    background = Image.new('RGB', (colorImageOne.width, colorImageOne.height + colorImageTwo.height))
    background.paste(colorImageOne, (0, 0))
    background.paste(colorImageTwo, (0, colorImageOne.height))
    background.save('ImageCache/background.png')

    
    
    finalImage = Image.new('RGB', (width, height))
    background.paste(image, ((int(background.width/2) - int(image.width / 2)), int((background.height/2) - int(image.height / 2))), image)
    background.save("ImageCache/finalImage.png")




def gradientMode(baseWidth, baseHeight, songTitle, songArtist, width, height, image):
    colors = getColors()
    firstColor = colors[0].rgb
    secondColor = colors[1].rgb

    array = get_gradient_3d(baseWidth, baseHeight, firstColor, secondColor, (False, False, False))
    Image.fromarray(np.uint8(array)).save("ImageCache/gradient.png", quality=95)

    gradient = Image.open("ImageCache/gradient.png")
    titleArtist = ImageDraw.Draw(gradient)
    myFont = ImageFont.truetype("fonts/CreamCake.otf", 60)#40)
    titleArtist.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (colors[1].rgb))
    gradient.save('ImageCache/gradient.png')
    gradient.paste(image, ((int(gradient.width/2) - int(image.width / 2)), int((gradient.height/2) - int(image.height / 2))), image)
    gradient.save("ImageCache/finalImage.png")

