import cv2
import imutils
import time


def takePicture(currPic):
    cap = cv2.VideoCapture(0)
    (grabbed, frame) = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    image = '../static/images/' + str((currPic) % 5) + '.jpg'
    cv2.imwrite(image, frame)
    return image


def takeFive():
    arr = []
    currPic = 0
    for x in range(5):
        print("taking image " + str(x))
        arr.append(takePicture(currPic))
        currPic += 1
    return arr
if __name__ == '__main__':
    print(takeFive())
