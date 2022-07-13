import json
import os
import cv2
import numpy as np
def resize(file,height,width):
    with open(file,'r') as f:
        file_data = json.load(f)
    scale_height = height/file_data['imageHeight']
    scale_width = width/file_data['imageWidth']
    data_resized = file_data
    dim_resize = (width,height)
    img = file_data['imageData']
    data_resized['imageData'] = cv2.resize(img,dim_resize,interpolation = cv2.INTER_AREA)
    for shape in data_resized['shapes']:
        for point in shape['points']:
            point[0]=point[0]*scale_width
            point[1]=point[1]*scale_height
    with open('./resized/'+file,'w') as file_save:
        json.dump(data_resized,file_save)

