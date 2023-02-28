import cv2
import numpy as np
import imutils

# read the map
image = cv2.imread('all_color_2.jpeg')
# convert map to hsv color space
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

boundaries = np.array(
    (
        (
            (30, 70, 0),
            (180, 255, 255),
            (40, 40, 40),
        ),
        (
            (0, 100, 0),
            (10, 255, 255),
            (120, 120, 120),
        ),

        (
        	(67,0,43),
        	(280,255,255),
        	(10,10,10) 
        ),

        (
        		(6,0,0),
        		(30,255,255),
        		(80,80,80)
        )
    ),
    dtype="uint8",
)

(width, height, colors) = image.shape
newImg = np.zeros(shape=(width, height, 1))
for lower, upper, colour in boundaries:
    colour_mask = cv2.inRange(image, lower, upper)
    image[colour_mask == 255] = colour
    newImg[colour_mask == 255] = (colour[0]/255)
kernel = np.ones((20, 20), np.uint8)
closing = cv2.morphologyEx(newImg, cv2.MORPH_CLOSE, kernel)
savedImg = closing * 255
cv2.imwrite('heightmap.jpg', savedImg)

src = cv2.imread('heightmap.jpg')
# Convert image to gray and blur it
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
src_gray = cv2.blur(src_gray, (3, 3))

v = np.median(src_gray)
sigma = 0.33
# ---- Apply automatic Canny edge detection using the computed median----
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))
edged = cv2.Canny(src_gray, lower, upper)
x, y, w, h = cv2.boundingRect(edged)
maxVal = max(h, w)
roi = src_gray[y:y+maxVal, x:x+maxVal]
cv2.imwrite('bounding.jpg', roi)

cv2.namedWindow("images", cv2.WINDOW_NORMAL)
image = cv2.imread('bounding.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 20, (255, 255, 255), -1)

    # find smaller contours
    for j in range(1, 101):
        scalingFactor = j/100.0
        color = 255 - (2.25*j) + 40
        contourClone = c.copy()
        for i in contourClone:
            x = i[0][0] - cX
            y = i[0][1] - cY
            x = x*scalingFactor
            y = y*scalingFactor
            x += cX
            y += cY
            i[0][0] = x
            i[0][1] = y
        # change thickness and color(color for every loop)
        cv2.drawContours(image, [contourClone], -1, (color, color, color), 2)
final = cv2.GaussianBlur(image, (15, 15), cv2.BORDER_DEFAULT)
cv2.imshow("images", final)
cv2.waitKey(0)
cv2.imwrite('final2.jpg', final)
