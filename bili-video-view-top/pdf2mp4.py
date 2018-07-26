import os

if not os.path.exists('frames'): 
    os.mkdir('frames')

os.system('F:/Technology/ImageMagick/convert.exe -monitor -density 50 ani_view.pdf -resize 1280x720! ./frames/ani_view_%06d.png')
os.system('C:/MySoftwares/ffmpeg/bin/ffmpeg.exe -framerate 60 -i ./frames/ani_view_%06d.png -s:v 1280x720 -pix_fmt yuv420p ani_view.mp4')