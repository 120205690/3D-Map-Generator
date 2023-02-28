import cv2 as cv
import numpy as np

src = cv.imread('heightmap.jpg')
# Convert image to gray and blur it
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3, 3))
source_window = 'Source'
cv.namedWindow(source_window)

v = np.median(src_gray)
sigma = 0.33
# ---- Apply automatic Canny edge detection using the computed median----
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))
edged = cv.Canny(src_gray, lower, upper)
cv.imshow('Edges', edged)
cv.waitKey()
x, y, w, h = cv.boundingRect(edged)
maxVal = max(h, w)
roi = src_gray[y:y+maxVal, x:x+maxVal]
print(roi.shape)
cv.imshow(source_window, roi)
#cv.imwrite('bounding.jpg', roi)
cv.waitKey()
