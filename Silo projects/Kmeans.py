import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans as KMeans

image = cv2.imread('map.jpeg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

km = KMeans(n_clusters=3)
km.fit(image.reshape((image.shape[0] * image.shape[1], image.shape[2])))

out = np.empty_like(image)
cluster_labels = km.labels_.reshape(image.shape[:2])
for i, colour in enumerate(km.cluster_centers_):
    out[cluster_labels == i] = colour

# image_colours = km.cluster_centers_.astype(np.uint8)
# out = np.asarray([image_colours[i] for i in km.labels_]).reshape(image.shape)

cv2.namedWindow("images", cv2.WINDOW_NORMAL)

cv2.imshow("images", out)
cv2.waitKey(0)

# for lower,upper,colour in boundaries:
#     colour_mask = cv2.inRange(image,lower,upper)
#     image[colour_mask == 255] = colour
#     cv2.imshow("images", image)

#     # colour_mask = cv2.inRange(image,lower,upper)
#     # x = cv2.bitwise_or(image, (1,1,1), mask = colour_mask)
#     # cv2.imshow("images", x)

#     cv2.waitKey(0)