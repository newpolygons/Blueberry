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