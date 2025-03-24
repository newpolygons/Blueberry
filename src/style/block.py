from PIL import Image, ImageDraw, ImageFont
from src.helpers.color import getColors
# Block Style, find examples at docs/CLI.MD


def blockMode(baseWidth, baseHeight, songTitle, songArtist, width, height, image, fontPath):
    colors = getColors()
    colorImageOne = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[0].rgb))
    titleArtist = ImageDraw.Draw(colorImageOne)
    myFont = ImageFont.truetype(fontPath, 60)#40)
    titleArtist.text((50,50), (songTitle + "\n" + songArtist), font = myFont, fill = (colors[1].rgb))
    colorImageOne.save('src/helpers/.cache/firstColor.png')
    colorImageTwo = Image.new('RGB', (baseWidth, int(baseHeight / 2)), (colors[1].rgb))
    colorImageTwo.save('src/helpers/.cache/secondColor.png')
    background = Image.new('RGB', (colorImageOne.width, colorImageOne.height + colorImageTwo.height))
    background.paste(colorImageOne, (0, 0))
    background.paste(colorImageTwo, (0, colorImageOne.height))
    background.save('src/helpers/.cache/background.png')
    finalImage = Image.new('RGB', (width, height))
    background.paste(image, ((int(background.width/2) - int(image.width / 2)), int((background.height/2) - int(image.height / 2))), image)
    background.save("src/helpers/.cache/finalImage.png")