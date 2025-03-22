# Gradient Style, find examples at docs/CLI.MD
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def gradientMode(varList, colors):
    firstColor = colors[0].rgb
    secondColor = colors[1].rgb
    array = get_gradient_3d(varList[0], varList[1], firstColor, secondColor, (False, False, False))
    Image.fromarray(np.uint8(array)).save("src/helpers/.cache/gradient.png", quality=95)
    gradient = Image.open("src/helpers/.cache/gradient.png")
    titleArtist = ImageDraw.Draw(gradient)
    myFont = ImageFont.truetype(varList[7], 60)#40)
    titleArtist.text((50,50), (varList[2] + "\n" + varList[3]), font = myFont, fill = (colors[1].rgb))
    gradient.save('src/helpers/.cache/gradient.png')
    gradient.paste(varList[6], ((int(gradient.varList[4]/2) - int(varList[6].varList[4] / 2)), int((gradient.varList[5]/2) - int(varList[6].varList[5] / 2))), varList[6])
    gradient.save("src/helpers/.cache/finalImage.png")

def get_gradient_2d(start, stop, varList[4], varList[5], is_horizontal):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, varList[4]), (varList[5], 1))
    else:
        return np.tile(np.linspace(start, stop, varList[5]), (varList[4], 1)).T

def get_gradient_3d(varList[4], varList[5], start_list, stop_list, is_horizontal_list):
    result = np.zeros((varList[5], varList[4], len(start_list)), dtype=float)

    for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
        result[:, :, i] = get_gradient_2d(start, stop, varList[4], varList[5], is_horizontal)

    return result