# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 03:16:21 2021

@author: Axiomatize
"""

import cv2
import numpy as np
# read the map
image = cv2.imread('My Map 2.jpg')
L=np.array([107, 54, 44][::-1], dtype = "uint8")
Sigma=np.array([7, 7, 7][::-1], dtype = "uint8")
print(L+Sigma)

z=np.zeros(image.shape[:2])

colour_mask = cv2.inRange(image,L-Sigma,L+Sigma)
z[colour_mask==255] = 255

kernel = np.ones((20, 20), np.uint8)
closing = cv2.morphologyEx(z, cv2.MORPH_CLOSE, kernel)
#closing=cv2.bitwise_not(closing)
closing=np.array(closing,dtype='uint8')
cv2.imwrite("Mask.jpg",closing)
cnts,_ = cv2.findContours(closing, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
con=closing.copy()

for c in cnts:                 #For First contour(Mountain)
    # compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    # draw the contour and center of the shape on the image
    #cv2.drawContours(closing, [c], -1, 150,6)
    #cv2.circle(closing, (cX, cY), 20, (0, 0, 0), -1)
    cv2.imwrite("Contour.jpg",closing)
    
    # find smaller contours
    for j in range(1, 101):             #For a contour at a particular r 
        scalingFactor = j/100.0
        color = 255 - (2.25*j)
        contourClone = c.copy()
        for i in contourClone:           #For every pt in that contour
            x = i[0][0] - cX
            y = i[0][1] - cY
            x = x*scalingFactor
            y = y*scalingFactor
            x += cX
            y += cY
            i[0][0] = x
            i[0][1] = y
        # change thickness and color(color for every loop)
        cv2.drawContours(closing, [contourClone], -1, color, 2) #Draw contours for every r
#Can the above line be taken out of the loop by summing each tuple?
final = cv2.GaussianBlur(closing, (25, 25), cv2.BORDER_DEFAULT)

F=cv2.bitwise_and(final,con)
cv2.imwrite("final2.jpg",F)
