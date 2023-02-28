import cv2
import numpy as np


def nothing(x):
    pass


image = cv2.imread('blue_ochre.jpeg')

# Creating a window for later use
cv2.namedWindow('result', cv2.WINDOW_NORMAL)

# Starting with 100's to prevent error while masking
h, s, v = 100, 100, 100

# Creating track bar
cv2.createTrackbar('h', 'result', 0, 179, nothing)
cv2.createTrackbar('s', 'result', 0, 255, nothing)
cv2.createTrackbar('v', 'result', 0, 255, nothing)

while(1):

    # converting to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h', 'result')
    s = cv2.getTrackbarPos('s', 'result')
    v = cv2.getTrackbarPos('v', 'result')

    # Normal masking algorithm
    lower_blue = np.array([h, s, v])
    upper_blue = np.array([280, 70, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(image, image, mask=mask)

    cv2.imshow('result', result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
