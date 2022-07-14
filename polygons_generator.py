import os
import json
from unicodedata import category

#################################################################################

#将此文件与COCO格式的train.json文件放入一个文件夹中执行，可生成cityscapes数据集格式的polygons.json文件

#################################################################################


#二分查找train.json中对应图号的annotation的序号范围
def find_anno(data, imgid):

    #二分查找出一个对应图号的annotation
    front = 0
    rear = len(data['annotations'])-1
    while (front <= rear):
        mid = int((front + rear)/2)
        if (data['annotations'][mid]['image_id'] == imgid):
            break
        elif (data['annotations'][mid]['image_id'] < imgid):
            front = mid + 1
        else :
            rear = mid - 1
    
    #每个图中annotation应该不是很多，直接顺序查找，找到范围
    front = mid
    rear = mid
    try:#try防止front=0时角标越界报错
        while (data['annotations'][front-1]['image_id'] == imgid):
            front -= 1
    except:
        pass
    
    try:
        while (data['annotations'][rear+1]['image_id'] == imgid):
            rear += 1
    except:
        pass

    return [front,rear]


with open('./train.json') as f:
    data = json.load(f)

for image in data['images']:
    img = {
        'imgHeight' : image['height'],
        'imgWidth' : image['width'],
        'objects' : [] 
    }

    #填写objects中的每一个物体
    [front,rear] = find_anno(data,image['id'])
    for anno_id in range(front, rear + 1):
        object = {
            'label' : '',
            'polygon' : []
        }
        category_id = data['annotations'][anno_id]['category_id']
        #填写每一个物体的轮廓点
        object['label'] = data['categories'][category_id-1]['name']
        p = 0
        while p < len(data['annotations'][anno_id]['segmentation'][0]):
            object['polygon'].append([data['annotations'][anno_id]['segmentation'][0][p],data['annotations'][anno_id]['segmentation'][0][p+1]])
            p += 2
        #将此物体保存进objects中
        img['objects'].append(object)
    
    #将img保存为图片的polygons文件
    with open('./'+os.path.splitext(image['file_name'])[0]+'_polygons.json','w') as t:
        t.write(json.dumps(img, ensure_ascii=False, indent=4, separators=(',', ':')))
    
