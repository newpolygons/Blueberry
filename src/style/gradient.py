# Gradient Style, find examples at docs/CLI.MD
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from src.helpers.color import getColors

def gradientMode(baseWidth, baseHeight, songTitle, songArtist, width, height, image, fontPath):
    colors = getColors()
    firstColor = colors[0].rgb
    secondColor = colors[1].rgb
    array = get_gradient_3d(baseWidth, baseHeight, firstColor, secondColor, (False, False, False))
    Image.fromarray(np.uint8(array)).save("src/helpers/.cache/gradient.png", quality=100)

    gradient = Image.open("src/helpers/.cache/gradient.png")
    titleArtist = ImageDraw.Draw(gradient)
    myFont = ImageFont.truetype(fontPath, 60)#40)
    titleArtist.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (colors[1].rgb))
    gradient.save('src/helpers/.cache/gradient.png')
    gradient.paste(image, ((int(gradient.width/2) - int(image.width / 2)), int((gradient.height/2) - int(image.height / 2))), image)
    gradient.save("src/helpers/.cache/finalImage.png")



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