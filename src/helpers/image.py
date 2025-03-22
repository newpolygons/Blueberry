from color import getColors
from style import *
from PIL import Image, ImageDraw

def albumImage(style, songInformation, display, fontPath):
    try:
        songTitle = songInformation[1]
        songArtist = songInformation[2]
    except:
        print("error occured in album image function")
        return
     # Setup Album Image
    width = int(int(display[0]) / 5)
    height = int(int(display[1]) / 2)
    
    baseWidth = int(display[0])
    baseHeight = int(display[1])
    image = Image.open("src/helpers/.cache/newCover.png")
    wpercent = (width/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((width,hsize), Image.LANCZOS)
    #Adding rounded corners and drop shadow to images
    
    image = add_corners(image, 20)
    image.save('src/helpers/.cache/newCover.png')

    colors = getColors(image)
    varList = [baseWidth, baseHeight, songTitle, songArtist, width, height, image, fontPath]
    
    if (style == 'block'):
        block.blockMode(varList, colors)
    elif (style == "gradient"):
        gradient.gradientMode(varList, colors)
    elif (style == "video"):
        video.videoMode(varList, colors)
    else:
        print("Style: " + str(style) + " is not supported please check the spelling of provided style.")
        exit()
    return songTitle



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