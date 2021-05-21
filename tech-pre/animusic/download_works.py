import os
from multiprocessing.dummy import Pool

urls = [
# Animusic
    # Future Retro - 04:44
    #     Animusic Future Retro 1080p HD with real ending - YouTube 
            "https://www.youtube.com/watch?v=vYQuf_0k3W8",
    # Stick Figures - 05:23
    #     [Animusic] - Stick Figures - YouTube 
            "https://www.youtube.com/watch?v=XkVXNjlh3RY",
    # Aqua Harp - 03:45
    #     Animusic - Aqua Harp [HD] - YouTube 
            "https://www.youtube.com/watch?v=5SI7KK-voVw",
    # Drum Machine - 03:22
    #     Animusic - Drum machine (2001) HD - YouTube 
            "https://www.youtube.com/watch?v=F7tMuUekYQA",
    # Pipe Dream - 03:23
    #     Animusic HD - Pipe Dreams (1080p) - YouTube 
            "https://www.youtube.com/watch?v=HR8Oz8Pp8hI",
    # Acoustic Curves - 05:35
    #     [Animusic] - Acoustic Curves - YouTube 
            "https://www.youtube.com/watch?v=YqP8xMZwCnw",
    # Harmonic Voltage - 05:53
    #     [Animusic] - Harmonic Voltage - YouTube 
            "https://www.youtube.com/watch?v=c34VVVLCmeg",
# Animusic 2
    # Starship Groove - 4:07
    #     Animusic HD - Starship Groove (1080p) - YouTube 
            "https://www.youtube.com/watch?v=rn8Uy4H10zw",
    # Pogo Sticks - 3:20
    #     Animusic HD- Pogo Sticks (1080p) - YouTube 
            "https://www.youtube.com/watch?v=YOQJxRCCpw8",
    # Resonant Chamber - 4:31
    #     Animusic HD - Resonant Chamber (1080p) - YouTube 
            "https://www.youtube.com/watch?v=XlyCLbt3Thk",
    # Cathedral Pictures - 6:08
    #     Animusic HD - Cathedral Pictures (1080p) - YouTube 
            "https://www.youtube.com/watch?v=gmzCDutDOYA",
    # Pipe Dream 2 - 3:45
    #     Animusic HD - Pipe Dream 2 (1080p) - YouTube 
            "https://www.youtube.com/watch?v=41a3DR0sZ-c",
    # Fiber Bundles - 5:16
    #     Animusic HD - Fiber Bundles (1080p) - YouTube 
            "https://www.youtube.com/watch?v=M6r4pAqOBDY",
    # Gyro Drums - 4:13
    #     Animusic HD - Gyro Drums (1080p) - YouTube 
            "https://www.youtube.com/watch?v=j-ATEH4wzrQ",
    # Heavy Light - 6:31
    #     Animusic HD - Heavy Light (1080p) - YouTube 
            "https://www.youtube.com/watch?v=DKUTYxJEB44",
# ANIMUSIC 3
    # ANIMUSIC 3 - Kickstarter Project - YouTube 
            "https://www.youtube.com/watch?v=JIh924CPk_c",
]

# outpath = "E:/_SciAniLab"
# outpath = "."
dl = "D:/youtube-dl.exe "

def downloadUrl(url):
    os.system(dl+url)

if __name__ == '__main__':
    pool = Pool(5)
    pool.map_async(downloadUrl,urls).get(100)
    # downloadUrl(urls[0])