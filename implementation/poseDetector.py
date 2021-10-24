import cv2 as cv
import matplotlib.pyplot as plt
import sys
import time

in_width = 368
in_height = 368
threshold = 0.2

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

# weights
net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

def checkDanger(img_path):
    """
    prints the new image with the generated skeleton
    param img_path: the string path to the image with a person in it to be processed
    """
    frame = cv.imread(img_path)
    cv.imshow('title for pic', frame)

    is_dangerous = poseEstimator(frame)
    if is_dangerous is None:
        print("Not enough visual data to make a conclusion.")
    elif is_dangerous is True:
        print("Somebody is exhibiting dangerous behavior")
    else:
        print("There doesn't appear to be any dangerous behavior")


def poseEstimator(frame):
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    vitals = {0: None, 1: None, 9: None, 12: None, 10: None, 13: None}
    #O = Nose, 1 = Neck, 9 = Right Knee, 12 = Left Knee, 10 = Right Ankle, 13 = Left Ankle
    
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (in_width, in_height), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frame_width * point[0]) / out.shape[3]
        y = (frame_height * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > threshold else None)

        if i in vitals.keys():
            vitals[i] = (int(x), int(y)) if conf > threshold else None

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    # display image with the joints assigned
    cv.imshow('OpenPose using OpenCV', frame)

    cv.waitKey(0) 
    cv.destroyAllWindows()
    
    # return if the leg is up
    return proportionHelper(vitals)


def coordsOf(vitals, body_part):
    """
    Based on the vitals dictionary, return the body part's coordinates
    param vitals: the 
    """
    return vitals.get(BODY_PARTS.get(body_part))


def proportionHelper(vitals):
    # assign coordinates for the top of the person
    top = coordsOf(vitals, "Nose")
    top_nose = True
    if top is None:
        top = coordsOf(vitals, "Neck")
        top_nose = False
    if top is None:
        return None
    
    # assign coordinates for the bottom extremities of the person
    extremities = (coordsOf(vitals, "RAnkle"), coordsOf(vitals, "LAnkle"))
    bottom_ankles = True
    if extremities[0] is None or extremities[1] is None:
        extremities = (coordsOf(vitals, "RKnee"), coordsOf(vitals, "LKnee"))
        bottom_ankles = False
    if extremities[0] is None or extremities[1] is None:
        return None

    proportion_of_body = None
    if top_nose and bottom_ankles:
        proportion_of_body = 1/6
    elif top_nose and not bottom_ankles:
        proportion_of_body = 1/5
    elif not top_nose and bottom_ankles:
        proportion_of_body = 1/5
    else:
        proportion_of_body = 1/4

    y_top = top[1]
    y_right = extremities[0][1]
    y_left = extremities[1][1]
    print("top_nose: " + str(top_nose) + ", top: " + str(top))
    print("bottom_ankles: " + str(bottom_ankles) + ", right: " + str(extremities[0]) + ", left: " + str(extremities[1]))

    height = max(y_right - y_top, y_left - y_top)
    lift = abs(y_right - y_left)

    # check if some of the points have converged to 1 point
    if distance(extremities[0], extremities[1]) < height * 0.05:
        return None

    return lift > height * proportion_of_body

def distance(x, y):
    return ((x[0] - y[0])**2 + (x[1] - y[1])**2)**0.5


def main():
    args = sys.argv[1:]
    checkDanger(args[0])

if __name__ == "__main__":
    main()
