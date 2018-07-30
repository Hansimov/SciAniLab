import os

if not os.path.exists('frames'): 
    os.mkdir('frames')

# os.system('F:/Technology/ImageMagick/convert.exe -monitor -density 72 ani_view.pdf -resize 1280x720! ./frames/ani_view_%06d.png')
# os.system('F:/Technology/ImageMagick/convert.exe -monitor -density 72 ani_view.pdf ./frames/ani_view_%06d.png')
# os.system('gswin64c -sDEVICE=jpeg -r72 -o ./frames/ani_view_%06d.jpg ani_view.pdf')
# os.system('gswin64c -sDEVICE=pngalpha -r288 -dDownScaleFactor=4 -o ./frames/ani_view_%06d.png ani_view.pdf')
os.system('gswin64c -sDEVICE=pngalpha -r216 -dDownScaleFactor=3 -o ./frames/ani_view_%06d.png ani_view.pdf')
# os.system('gswin64c -sDEVICE=pngalpha -r144 -dDownScaleFactor=2 -o ./frames/ani_view_%06d.png ani_view.pdf')

os.system('C:/MySoftwares/ffmpeg/bin/ffmpeg.exe -framerate 60 -i ./frames/ani_view_%06d.png -pix_fmt yuv420p ani_view.mp4')