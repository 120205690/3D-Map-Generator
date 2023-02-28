# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:30:10 2021

@author: Axiomatize
"""
import cv2
img = cv2.imread('uniform 4.jpg')
mask = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)[1][:,:,0]
mask = cv2.dilate(mask,(20,20),iterations = 5)

dst = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
cv2.imwrite('Inpainting.jpg',dst)
