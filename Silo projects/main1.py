import cv2
import numpy as np

image = cv2.imread('map.jpeg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

boundaries = np.array(
    (
        (
            (30, 70, 0),
            (180, 255, 255),
            (40, 40, 40),
        ),
        (
            (0, 40, 0),
            (20, 255, 255),
            (120, 120, 120),
        ),
    ),
    dtype="uint8",
)

cv2.namedWindow("images", cv2.WINDOW_NORMAL)

cv2.imshow("images", image)
cv2.waitKey(0)

(width, height, colors) = image.shape
newImg = np.zeros(shape=(width, height, 1))
print(newImg.shape)
for lower, upper, colour in boundaries:
    colour_mask = cv2.inRange(image, lower, upper)
    image[colour_mask == 255] = colour
    print(colour[0])
    newImg[colour_mask == 255] = (colour[0]/255)
    #cv2.imshow("images", newImg)

    # colour_mask = cv2.inRange(image,lower,upper)
    # x = cv2.bitwise_or(image, (1,1,1), mask = colour_mask)
    # cv2.imshow("images", x)

    # cv2.waitKey(0)
cv2.imshow("images", newImg)
cv2.waitKey(0)
kernel = np.ones((20, 20), np.uint8)
closing = cv2.morphologyEx(newImg, cv2.MORPH_CLOSE, kernel)
cv2.imshow("images", closing)
savedImg = closing * 255
cv2.imwrite('heightmap.jpg', savedImg)
cv2.waitKey(0)
