import glob
import os


files = glob.glob('Rob*.mp4') #Shop
print(len(files))

i = 150
# Shoplifting111_x264

for file in files:
  i = i + 1
  os.rename(file, 'Robbery' + str(i).zfill(3) +  '_x264.mp4')
  #print('Shoplifting' + str(i).zfill(3) +  '_x264.mp4')
