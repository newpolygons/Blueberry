import sys
import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from src.helpers.color import getColors

class WebWindow(QMainWindow):
    def __init__(self, baseWidth, baseHeight, songTitle, songArtist, fontPath, firstColor, secondColor, image):
        super().__init__()
        # Set up the window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.baseWidth = baseWidth
        self.baseHeight = baseHeight
        self.songTitle = songTitle
        self.songArtist = songArtist
        self.firstColor = firstColor
        self.secondColor = secondColor
        self.image = image
        self.setGeometry(0, 0, self.baseWidth, self.baseHeight)

        # Create a QWebEngineView widget
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        self.web_view.setGeometry(0, 0, self.baseWidth, self.baseHeight)  # Adjust to your screen size
        # Load HTML with CSS
        self.load_html_with_css()

        self.pixMap = QPixmap(self.image)
        if self.pixMap.isNull():
            print("Failed to load the image.")
            return

        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(self.pixMap)
        self.imageLabel.setGeometry(int((self.web_view.width() - self.pixMap.width())//2), int((self.web_view.height() - self.pixMap.height())//2), self.pixMap.width(), self.pixMap.height())
        
        
        
        # Credit Text 

        creditLabel = QLabel("by: newpolygons", self.web_view)
        creditFontPath = os.path.abspath("src/fonts/Photograph Signature.ttf")
        creditfontID = QFontDatabase.addApplicationFont(creditFontPath)
        creditFontFamilies = QFontDatabase.applicationFontFamilies(creditfontID)
        creditFontFamily = creditFontFamilies[0]

        creditFont = QFont(creditFontFamily)
        creditFont.setPointSize(int(baseWidth/20))
        creditFont.setWeight(QFont.Normal)
        creditLabel.setFont(creditFont)
        creditLabel.setGeometry(int((self.baseWidth - self.baseWidth)) + 80, int(self.baseHeight * 0.85), int(self.web_view.width()), int(self.web_view.height() * 0.1))

        self.overlayText = QLabel(f"{songArtist} - {songTitle}", self.web_view)
        self.fontPath = fontPath
        self.setCustomFont()
        self.overlayText.setAlignment(Qt.AlignCenter)     
        self.overlayText.setGeometry(int((self.baseWidth - self.baseWidth)//2),int(self.baseHeight * 0.1), int(self.web_view.width()),int(self.web_view.height() * 0.1))




        
    def load_html_with_css(self):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
               
                    body {{
                    background: linear-gradient(235deg,{self.firstColor}, {self.secondColor});
                    background-size: 100% 100%;
                    animation: gradient-animation 10s ease infinite;
                    }}

                    @keyframes gradient-animation {{
                    0% {{
                        background-position: 0% 50%;
                    }}
                    50% {{
                        background-position: 100% 50%;
                    }}
                    100% {{
                        background-position: 0% 50%;
                    }}
                    }}
                
                
            </style>
        </head>
        <body> 
            <p></p>
        </body>
        </html>
        """
        # Load the HTML content into the QWebEngineView
        
        self.web_view.setHtml(html_content)

    def setCustomFont(self):
        fontID = QFontDatabase.addApplicationFont(self.fontPath)
        if fontID == -1:
            print("Font Failed To Load.")
            return
        fontFamilies = QFontDatabase.applicationFontFamilies(fontID)
        if not fontFamilies:
            print("No font families found in the font file.")
            return 
        fontFamily = fontFamilies[0]

        font = QFont(fontFamily)
        font.setPointSize(int(self.baseWidth/20))
        font.setWeight(QFont.Bold)

        self.overlayText.setFont(font)

    '''
    def refresh_video(self):
        """Refresh the video element using JavaScript."""
        js_code = """
        const img = document.querySelector('img');
        img.load();
        """
        #self.web_view.page().runJavaScript(js_code)
    
    def update_css(self):
        """Update the CSS dynamically using JavaScript."""
        js_code = """
        const container = document.getElementById('video-container');
        container.style.width = '800px';
        container.style.height = '450px';
        container.style.border = '10px solid #ff6347';
        """
        #self.web_view.page().runJavaScript(js_code)
'''


def videoMode(baseWidth, baseHeight, songTitle, songArtist, width, height, image, fontPath):
    colors = getColors()
    firstColor = rgb_string_to_hex(str(colors[0].rgb))
    secondColor = rgb_string_to_hex(str(colors[1].rgb))

    app = QApplication(sys.argv)

    
    fontPath = os.path.abspath(fontPath)
    image = os.path.abspath(image)
    window = WebWindow(baseWidth, baseHeight, songTitle,  songArtist, fontPath, firstColor, secondColor, image)

    window.show()

    sys.exit(app.exec_())

def rgb_string_to_hex(rgb_string):
    try:
        # Extract the r, g, b values from the string
        r = int(rgb_string.split("r=")[1].split(",")[0])
        g = int(rgb_string.split("g=")[1].split(",")[0])
        b = int(rgb_string.split("b=")[1].split(")")[0])

        # Ensure the RGB values are within the valid range
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        # Convert each component to a 2-digit hexadecimal string
        hex_code = "#{:02X}{:02X}{:02X}".format(r, g, b)
        return hex_code
    except (IndexError, ValueError):
        return "#000000"  # Return black as a default value

