####################################################################################################

# 将此文件放进待处理.jpg和.json文件夹中运行
# 将会在当前文件夹自动生成一个train.json文件
# 并且新建一个名为resized的文件夹放置压缩大小后的图片

####################################################################################################

#压缩图片函数
def resize(file,dim_resized):
    img = cv2.imread('./'+file,cv2.IMREAD_UNCHANGED)
    img_resized = cv2.resize(img,dim_resized,interpolation = cv2.INTER_AREA)
    cv2.imwrite('./resized/'+file,img_resized)

#计算bbox函数
def bbox(points):
    a = np.array(points)
    [x,y] = a.min(0)
    [u,v] = a.max(0)
    return list(map(int,[x,y,u-x,v-y]))

#判断category是否在categories里
def is_in(label,categories):
    for category in categories:
        if label == category['name']:
            return category['id']
    return False


import os
from unicodedata import category
import cv2
import json
import numpy as np

#压缩后大小
dim_resized = (1680,1405)

#读取文件列表
filenames=os.listdir(r'.')

#创建存放压缩后照片的文件夹
if not(os.path.exists('./resized')):
    os.mkdir('./resized')

#压缩后存入resized文件夹
for file in filenames:
    if file.endswith('.jpg'):
        resize(file,dim_resized)

#创建最终的字典train
train = {'images':[],'categories':[],'annotations':[]}

#首先填完images
id = 1
for file in filenames:
    if file.endswith('.json') and not(file == 'train.json'):
        image_info = {
            'height' : dim_resized[1],
            'width' : dim_resized[0],
            'id' : id,
            'file_name' : os.path.splitext(file)[0] + '.jpg'
        }
        train['images'].append(image_info)
        id = id + 1

#完成annotations
id = 0
image_id = 0
for file in filenames:
    if file.endswith('json') and not file == 'train.json':
        #图号加1
        image_id = image_id + 1
        #读取文件内容
        with open(file) as f:
            file_data = json.load(f)
        #遍历一个一个圈
        scale_height = dim_resized[1]/file_data['imageHeight']
        scale_width = dim_resized[0]/file_data['imageWidth']
        for shape in file_data['shapes']:
            #建立每一个圈在train.json文件中的annotation
            annotation = {
                'segmentation' : [[]],
                'iscrowd' : 0,
                'image_id' : 0,
                'bbox' : [],
                'area' : 0,
                'category_id' : 0,
                'id' : 0
            }

            #填写segmentation
            for point in shape['points']:
                annotation['segmentation'][0].append(int(point[0]*scale_width))
                annotation['segmentation'][0].append(int(point[1]*scale_height))
            
            points = []
            p = 0
            while p < len(annotation['segmentation'][0]):
                points.append([annotation['segmentation'][0][p], annotation['segmentation'][0][p+1]])
                p = p + 2
                
            
            #填写iscrowd
            annotation['iscrowd'] = 0

            #填写image_id
            annotation['image_id'] = image_id

            #填写bbox
            annotation['bbox'] = bbox(points)

            #填写area
            annotation['area'] = annotation['bbox'][2]*annotation['bbox'][3]

            #填写category_id
            if is_in(shape['label'], train['categories']):
                annotation['category_id'] = is_in(shape['label'], train['categories'])
            else :
                new_category = {
                    "supercategory": "material",
                    "id": len(train['categories']) + 1,
                    "name": shape['label']
                }
                train['categories'].append(new_category)
                annotation['category_id'] = new_category['id']
            
            #填写id
            id = id +1
            annotation['id'] = id

            #把annotation加到train['annotations']里
            train['annotations'].append(annotation)



#大功告成，保存train
with open("./train.json", "w") as t:
    t.write(json.dumps(train, ensure_ascii=False, indent=4, separators=(',', ':')))















