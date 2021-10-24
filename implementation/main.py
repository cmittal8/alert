
import ultrasonic
import playaudio
from detectPerson import *
import detectPerson
import usbCamera
from sendText import *
from poseDetector import checkDanger

if __name__ == "__main__":
    ultrasonic.getDist()
    # usbcamera funcunality goes here - imgArr = usbCam()
    imgArr = usbCamera.takeFive()
    count = 0
    print("accessing google vision api")
    for img in imgArr:
        if (detect_faces(img) == 'Person detected') :
            #alex
            if checkDanger(img):
                count += 1
    if count >= 3:
        print('Help is/may be needed. Please respond immediately.')
        playaudio.playmessage()
        sendMessage()
    else:
        print('There is no danger detected from the current behavior')


