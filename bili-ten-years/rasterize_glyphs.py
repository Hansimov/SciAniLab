import os

cmd_pdf2png = 'gswin64c -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -r72 -sOutputFile="glyphs/glyphs_%05d.png" "glyphs.pdf"'

os.system(cmd_pdf2png)