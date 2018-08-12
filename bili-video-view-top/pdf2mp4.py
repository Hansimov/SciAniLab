import os
import time

# if os.path.exists('frames'):
#     os.rmdir('frames')

if not os.path.exists('frames'): 
    os.mkdir('frames')

t2 = time.time()

# os.system('F:/Technology/ImageMagick/convert.exe -monitor -density 72 ani_view.pdf -resize 1280x720! ./frames/ani_view_%06d.png')
# os.system('F:/Technology/ImageMagick/convert.exe -monitor -density 72 ani_view.pdf ./frames/ani_view_%06d.png')
# os.system('gswin64c -sDEVICE=jpeg -r72 -o ./frames/ani_view_%06d.jpg ani_view.pdf')
# os.system('gswin64c -sDEVICE=pngalpha -r288 -dDownScaleFactor=4 -o ./frames/ani_view_%06d.png ani_view.pdf')
os.system('gswin64c -sDEVICE=pngalpha -r216 -dDownScaleFactor=2 -o ./frames/ani_view_%06d.png ani_view.pdf')
# os.system('gswin64c -sDEVICE=pngalpha -r144 -dDownScaleFactor=2 -o ./frames/ani_view_%06d.png ani_view.pdf')

if os.path.exists('ani_view.mp4'):
    os.remove('ani_view.mp4')
# ffmpeg_path = 'C:/MySoftwares/ffmpeg/bin/ffmpeg.exe'
ffmpeg_path = 'D:/ffmpeg/bin/ffmpeg.exe'
os.system(f'{ffmpeg_path} -framerate 60 -i ./frames/ani_view_%06d.png -pix_fmt yuv420p ani_view.mp4')

t3 = time.time()
dt2 = t3 - t2
print('Elapsed time 2: {:.7} s'.format(dt2))