#Setup Background Colors
import colorgram
import math
from itertools import combinations

def getColors():
    colors = colorgram.extract('src/helpers/.cache/newCover.png', 15)
    if len(colors) < 2:
        return ((1, 1, 1), (255, 255, 255))
    else:
        rgbColors = [(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors]
        vibrantColor = max(rgbColors, key=calculateVibrancy)
        maxDistance = 0
        mostDissimilarColors = (None, None)
        for color in rgbColors:
            if color != vibrantColor:
                distance = rgbDistance(vibrantColor, color)
                if distance > maxDistance:
                    maxDistance = distance
                    mostDissimilarColors = (color, vibrantColor)
        return(mostDissimilarColors)
    

def rgbDistance(color1, color2):
    return math.sqrt((color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2)

def calculateVibrancy(color):
    r, g, b = color
    total = r + g + b
    if total == 0:
        return 0
    saturation = ((max(r, g, b) - min(r, g, b)) / total) * 100
    brightness = (total / 3)
    return saturation * brightness