# from ultrasonic import *
# from playaudio import *

import ultrasonic
import playaudio
import detectPerson

if __name__ == "__main__":
    ultrasonic.getDist()
    #imgarr = [] -- arrray of image names with all the images located in the images/ folder
    # usbcamera funcunality goes here - imgArr = usbCam()
    imgArr = ["jump.jpg", "stand.jpg"]
    count = 0
    for img in imgArr:
        if (detectPerson.detect_faces("images/" + img) == 'Person detected') :
            count = count + 1
    print(count)