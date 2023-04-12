import cv2
img = cv2.imread('sqx.jpg')

x, y = img.shape[0:2]

img = cv2.resize(img, (int(y / 2), int(x / 2)))
cv2.imwrite('img2.jpg',img)