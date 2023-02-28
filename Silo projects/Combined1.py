
# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import numpy as np
import cv2

# load the image and convert it from BGR to RGB so that
# we can dispaly it with matplotlib
image = cv2.imread("C:/Users/Axiomatize/Desktop/Africa/median 91.jpg")
#median=cv2.medianBlur(image,25)
image=cv2.bilateralFilter(image, 5, 21, 21)
#gauss=cv2.GaussianBlur(image,(5,5),0)
i2=image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# reshape the image to be a list of pixels
image = image.reshape((image.shape[0] * image.shape[1], 3))
bins=4
# cluster the pixel intensities
clt = KMeans(n_clusters = bins)
clt.fit(image)

cluster_labels = clt.labels_.reshape(i2.shape[:2])
out = np.empty_like(i2)

Colours=[]
for color in clt.cluster_centers_:
    Colours.append(color.astype("uint8").tolist())
print(Colours)

for i, colour in enumerate(clt.cluster_centers_):
        out[cluster_labels == i] = Colours[i]
        
        
out=cv2.cvtColor(out, cv2.COLOR_RGB2BGR)
out=cv2.bilateralFilter(out, 5, 21, 21)

cv2.imwrite('Uniform1.jpg',out)
#C2=cv2.cvtColor(C,cv2.COLOR_RGB2HSV)


# read the map
image = cv2.imread('Uniform1.jpg')
H=[]
q=0
while(q<bins):

    L=np.array(Colours[q][::-1], dtype = "uint8")
    Sigma=np.array([1, 1, 1][::-1], dtype = "uint8")
    print(L)
    z=np.zeros(image.shape[:2])
    
    colour_mask = cv2.inRange(image,L-Sigma,L+Sigma)
    z[colour_mask==255] = 255
    
    kernel = np.ones((20, 20), np.uint8)
    closing = cv2.morphologyEx(z, cv2.MORPH_CLOSE, kernel,iterations = 1)
    #closing=cv2.bitwise_not(closing)
    
    closing=np.array(closing,dtype='uint8')
    #_,closing = cv2.threshold(closing,0.,255.,cv2.THRESH_OTSU)
    
    cv2.imwrite("Mask{}.jpg".format(q),closing)
    cnts,_ = cv2.findContours(closing, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    con=closing.copy()
    print(len(cnts))
    for c in cnts:                 #For First contour(Mountain)
        # compute the center of the contour
        M = cv2.moments(c)
        if M['m00']!=0:
         cX = int(M["m10"] / M["m00"])
         cY = int(M["m01"] / M["m00"])
         #print(cX,cY)
         # draw the contour and center of the shape on the image
         #cv2.drawContours(closing, [c], -1, 150,6)
         #cv2.circle(closing, (cX, cY), 20, (0, 0, 0), -1)
         cv2.imwrite("Contour{}.jpg".format(q),closing)
        
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
    final = cv2.GaussianBlur(closing, (15, 15), cv2.BORDER_DEFAULT)
    
    F=cv2.bitwise_and(final,con)
    cv2.imwrite("{}.jpg".format(q),F)
    H.append(F)
    q+=1
a=cv2.bitwise_or(H[0],H[1])
b=cv2.bitwise_or(H[2],H[3])
c=cv2.bitwise_or(a,b)

#a=cv2.bitwise_or(a,H[4],H[5])
cv2.imwrite("F.jpg",c)