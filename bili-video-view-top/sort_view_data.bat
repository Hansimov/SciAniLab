@echo off
C:/MySoftwares/GnuWin32/bin/sort.exe --field-separator=, --key=2,2nr --buffer-size=100M "./data/video_dynamic_180723.csv" -o "./data/sorted.csv"
rem pause