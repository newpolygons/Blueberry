#functions for downloading spotify song when provided a link
from subprocess import Popen, PIPE, CalledProcessError

downloadDir =  "downloads/"
formatType = "wav"   #{mp3,flac,ogg,opus,m4a,wav}
bitrate = 'disable'  #{auto,disable,8k,16k,24k,32k,40k,48k,64k,80k,96k,112k,128k,160k,192k,224k,256k,320k}

#downloads the song you are currently listening to. To be saved in 'downloads' dir.
def downloadCurrentSong(link):
    cmd = ['spotdl', link, '--output', downloadDir, '--format', formatType,  '--bitrate', bitrate, ]

    with Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='') # process line here
        if p.returncode != 0:
            print(p.returncode, p.args)
