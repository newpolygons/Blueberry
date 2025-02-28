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