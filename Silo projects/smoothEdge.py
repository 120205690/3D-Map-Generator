import cv2
import numpy as np
import imutils


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
    # show the image
    #cv2.imshow("images", image)
    # cv2.waitKey(0)

    # find smaller contours
    for j in range(1,11):
    	for i in c:
    		x = i[0][0] - cX
    		y = i[0][1] - cY
    		x = x*(j/10.0)        # Change the scaling factor
    		y = y*(j/10.0)
    		x += cX
    		y += cY
    		i[0][0] = x
    		i[0][1] = y
    		 # change thickness and color(color for every loop)
    	cv2.drawContours(image, [c], -1, (30.0+(22.5*j), 30.0+(22.5*j), 30.0+(22.5*j)), 2)
        	
 
cv2.imshow("images", image)
#cv2.imwrite('centroid.jpg', image)
cv2.waitKey(0)
