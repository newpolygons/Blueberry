#functions for downloading current song
import subprocess
import os


downloadDir = os.path.join('.', 'downloads')
formatType = 'wav' # {mp3,flac,ogg,opus,m4a,wav}


#downloads the song you are currently listening to. To be saved in /downloads dir.
def downloadCurrentSong(link):
    try:
        #check again when not on vpn
        print("Attempting to download: " + str(link) + ' to ' + str(downloadDir))
        subprocess.check_output(['spotdl', link, '--output', downloadDir, '--format', formatType], stderr=subprocess.STDOUT)
    except Exception as e:
        print(e)
    

if __name__ == '__main__':
    '''
    downloadDir = os.path.join('.', 'downloads')
    link = ""
    downloadCurrentSong(link)
    '''
    

# https://open.spotify.com/track/1Es7AUAhQvapIcoh3qMKDL
