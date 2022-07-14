import os
import json
from this import d
import numpy as np
import cv2

#################################################################################

#将此文件与COCO格式的train.json文件放入一个文件夹中执行，可生成每张图片的mask图

#################################################################################

with open('./train.json') as f:
    data = json.load(f)


image_id = 1
points = []
#建立一张空mask图
mask = np.zeros([data['images'][image_id]['height'], data['images'][image_id]['width'], 3], np.uint8)
#遍历每一个圈
for annotation in data['annotations']:
    #如果这张是新图片，保存之前的mask
    if annotation['image_id'] > image_id:
        #保存为新图片        
        cv2.imwrite('./'+os.path.splitext(data['images'][image_id-1]['file_name'])[0]+'_mask.jpg', mask)
        #生成空白的新mask
        mask = np.zeros([data['images'][image_id]['height'], data['images'][image_id]['width'], 3], np.uint8)
        image_id += 1
    #用points装每一个圈
    p = 0
    while p < len(annotation['segmentation'][0]):
        points.append([annotation['segmentation'][0][p],annotation['segmentation'][0][p+1]])
        p += 2
    #将圈的区域着色到mask上
    points = np.array(points,dtype = np.int32)
    cv2.fillPoly(mask, [points], [255, 255, 255])
    points = []
    

'''
#这段是从每张图片的json文件生成mask的代码
#读取文件列表
filenames = os.listdir('.')

for file in filenames:

    if file.endswith('.json') and not file == ('train.json'):
            
        # 打开文件
        with open(file) as f:
            data = json.load(f)
        
        #生成空白图片
        mask = np.zeros([data['imageHeight'],data['imageWidth'],3], np.uint8)

        for shape in data['shapes']:
            points = np.array(shape['points'], dtype = np.int32)
            cv2.fillPoly(mask, [points], [255,255,255])
      
        # 保存
        cv2.imwrite('./'+os.path.splitext(file)[0]+'_mask.jpg',mask)
'''

