IO='./input_output'
cd $IO


echo Generating 10-colour palette
time ../colours.py 10 > palette_10.ini
../colours.py palette_10.ini palette_10.png

echo Generating palette from short namesfile
time ../colours.py namesfile_short > palette_short.ini
../colours.py palette_short.ini palette_short.png

echo Generating palette from full namesfile
time ../colours.py namesfile > palette.ini
../colours.py palette.ini palette.png
