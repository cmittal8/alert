
import ultrasonic
import playaudio
import detectPerson
import usbCamera

if __name__ == "__main__":
    ultrasonic.getDist()
    # usbcamera funcunality goes here - imgArr = usbCam()
    imgArr = usbCamera.takeFive()
    count = 0
    for img in imgArr:
        if (detectPerson.detect_faces(img) == 'Person detected') :
            #alex
    print(count)
