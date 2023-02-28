import cv2 as cv
import numpy as np

noise = cv.imread('diamondsquare.png')
maps = cv.imread('bounding.jpg')
noise_gry = cv.cvtColor(noise, cv.COLOR_BGR2GRAY)
map_gry = cv.cvtColor(maps, cv.COLOR_BGR2GRAY)

cv.namedWindow("images", cv.WINDOW_NORMAL)
cv.imshow('images', map_gry)
cv.waitKey()

newImg = map_gry * (150/255) + noise_gry * (105/255)
newImg = np.rint(newImg).astype(np.uint8)
cv.imshow('images', newImg)
cv.imwrite('combinedImage.jpg', newImg)
cv.waitKey()
