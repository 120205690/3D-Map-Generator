import cv2
import numpy as np

image = cv2.imread('map.jpeg')

# define the list of boundaries
boundaries = [
    ([30, 70, 0], [180, 255, 255]),  # green
    ([0, 40, 0], [20, 255, 255]),   # brown
]

cv2.namedWindow("images", cv2.WINDOW_NORMAL)
masks = []

count = 0  # Current color

# converting to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    tempMask = cv2.inRange(hsv, lower, upper)
    print(tempMask[530][550])
    cv2.imshow("images", tempMask)
    cv2.waitKey(0)
    if count == 0:
        print(tempMask)
        # error this line is giving error
        tempMask = tempMask * (30/255)  # change height of green color
    masks.append(tempMask)
    count += 1  # next color

mask = cv2.bitwise_or(masks[0], masks[1])
t = cv2.add(masks[0], masks[1])
#output = cv2.bitwise_and(image, image, mask=mask)
# show the images
cv2.imshow("images", t)
cv2.waitKey(0)
