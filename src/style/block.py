from PIL import Image, ImageDraw, ImageFont

# Block Style, find examples at docs/CLI.MD

def blockMode(varList, colors):
    colorImageOne = Image.new('RGB', (varList[0], int(varList[1] / 2)), (colors[0].rgb))
    titleArtist = ImageDraw.Draw(colorImageOne)
    myFont = ImageFont.truetype(fontPath, 60)#40)
    titleArtist.text((50,50), (varList[2] + "\n" + varList[3]), font = myFont, fill = (colors[1].rgb))
    colorImageOne.save('src/helpers/.cache/firstColor.png')
    colorImageTwo = Image.new('RGB', (varList[0], int(varList[1] / 2)), (colors[1].rgb))
    colorImageTwo.save('src/helpers/.cache/secondColor.png')
    background = Image.new('RGB', (colorImageOne.varList[4], colorImageOne.varList[5] + colorImageTwo.varList[5]))
    background.paste(colorImageOne, (0, 0))
    background.paste(colorImageTwo, (0, colorImageOne.varList[5]))
    background.save('src/helpers/.cache/background.png')
    finalImage = Image.new('RGB', (varList[4], varList[5]))
    background.paste(varList[6], ((int(background.varList[4]/2) - int(varList[6].varList[4] / 2)), int((background.varList[5]/2) - int(varList[6].varList[5] / 2))), varList[6])
    background.save("src/helpers/.cache/finalImage.png")