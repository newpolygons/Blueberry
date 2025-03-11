#functions for downloading current song
import subprocess
import os
downloadDir = os.path.join('.', 'downloads')
formatType = 'wav' # {mp3,flac,ogg,opus,m4a,wav}


#downloads the song you are currently listening to. To be saved in /downloads dir.
def downloadCurrentSong(link):
    print("Attempting to download: " + str(link) + ' to ' + str(downloadDir))
    try:
        subprocess.check_output(['spotdl', 'download', link, '--output', downloadDir, '--format', formatType])
    except Exception as e:
        print(e)
    

if __name__ == __main__():
    '''
    from ../main import spotify_authenticate(), get_song_id()
    spotify_authenticate()
    get_song_id()
    downloadCurrentSong(link)
    '''
    print("Ill work one day!")

# https://open.spotify.com/track/1Es7AUAhQvapIcoh3qMKDL
