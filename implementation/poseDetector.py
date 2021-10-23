import cv2 as cv
import matplotlib.pyplot as plt

# weights
net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

def checkRaisedKnee():
    in_width = 368
    in_height = 368
    thr = 0.2