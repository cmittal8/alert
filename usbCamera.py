import cv2
import imutils
import time


def takePicture(currPic):
    cap = cv2.VideoCapture(0)
    (grabbed, frame) = cap.read()
    image = 'images/' + str((currPic) % 5) + '.jpg'
    cv2.imwrite(image, frame)
    return image


def takeFive():
    arr = []
    currPic = 0
    for x in range(5):
        arr.append(takePicture(currPic))
        currPic += 1
    return arr
print(takeFive())
