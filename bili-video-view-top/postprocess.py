import os
import time

# Intro
# Corner
# Original
# > opening.tex

def xpdf2png():
    gs_cmd = 'gswin64c -sDEVICE=pngalpha -r216 -dDownScaleFactor=2 -o ./{0}/{0}_%06d.png {0}.pdf'
    # gs_cmd = 'gswin64c -sDEVICE=pngalpha -r864 -dDownScaleFactor=8 -o ./{0}/{0}_%06d.png {0}.pdf'

    pdf2png_list = [
    # Shift global view [To MP4]
    # > 'ending_global_view_shift.tex'
    # Zoom global view [To MP4]
    # > 'ending_global_view_zoom.tex'
        # 'ending_global_view_shift', # ok
        # 'ending_global_view_zoom',  # ok
    # Region seperate
    # Region combination
    # > 'ending_region_view_all.tex'
        # 'ending_region_view_all',   # ok
    # Sum of videos
    # Region charts
    # Level charts
    # > 'ending_charts_all.tex'
        # 'ending_charts_all', # ok
    # Top viedeo pull [To MP4]
    # > 'ending_top_video_pull.tex'
        # 'ending_top_video_pull', # ok
    # Bgm
    # Tool
    # Staff
    # Org
    # > staff.tex
        'staff', # ok
    ]

    t1 = time.time()
    for pdf2png_tmp in pdf2png_list:
        print('pdf2png: {} ...'.format(pdf2png_tmp))
        if not os.path.exists(pdf2png_tmp): 
            os.mkdir(pdf2png_tmp)
        gs_cmd_tmp = gs_cmd.format(pdf2png_tmp)
        os.system(gs_cmd_tmp)
    t2 = time.time()
    dt = t2 - t1
    print('Elapsed time: {} s'.format(round(dt, 2)))

def xpng2mp4():
    ffmpeg_path = 'D:/ffmpeg/bin/ffmpeg.exe'
    ffmpeg_cmd = '{0} -y -framerate 60 -i ./{1}/{1}_%06d.png -pix_fmt yuv420p {1}.mp4'

    png2mp4_list = [
        'ending_global_view_shift', # ok
        'ending_global_view_zoom',  # ok
        'ending_top_video_pull',    # ok
    ]
    for png2mp4_tmp in png2mp4_list:
        print('png2mp4: {} ...'.format(png2mp4_tmp))
        ffmpeg_cmd_tmp = ffmpeg_cmd.format(ffmpeg_path, png2mp4_tmp)
        os.system(ffmpeg_cmd_tmp)

if __name__ == '__main__':
    xpdf2png()
    # xpng2mp4()
    pass

