import cv2
camera = cv2.VideoCapture(0)
while(camera.isOpened() == False):
    print "not opened yet"
return_value, image = camera.read()
cv2.imwrite('opencv.png', image)
del(camera)
