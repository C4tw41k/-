import os
import image_resize as imgresize

filenames=os.listdir(r'.')


height = 1405
width = 1680

for file in filenames:
    if file.endswith('.json'):
        imgresize.resize(file,height,width)

