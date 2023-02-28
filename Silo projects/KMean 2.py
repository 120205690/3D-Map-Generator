
# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import numpy as np
import cv2

# load the image and convert it from BGR to RGB so that
# we can dispaly it with matplotlib
image = cv2.imread("1.jpg")
i2=image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# reshape the image to be a list of pixels
image = image.reshape((image.shape[0] * image.shape[1], 3))
# cluster the pixel intensities
clt = KMeans(n_clusters = 4)
clt.fit(image)

cluster_labels = clt.labels_.reshape(i2.shape[:2])
out = np.empty_like(i2)

C=[]
for color in clt.cluster_centers_:
    C.append(color.astype("uint8").tolist())
print(C)

for i, colour in enumerate(clt.cluster_centers_):
        out[cluster_labels == i] = C[i]
plt.imshow(out)
plt.title("New") 
plt.show()

#C2=cv2.cvtColor(C,cv2.COLOR_RGB2HSV)
