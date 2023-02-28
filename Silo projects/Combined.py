# import the necessary packages
from scipy.interpolate import interp1d
from skimage.util import random_noise
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import numpy as np
import cv2

# load the image and convert it from BGR to RGB so that
# we can dispaly it with matplotlib
image = cv2.imread("C:/Users/Axiomatize/Desktop/Maps/0112_i2.png")
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
image =cv2.imread('Uniform1.jpg')
#image=cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
cv2.imwrite("i.jpg",image)
H=[]
q=0
m=[0,0]
r=np.array([[[0,99,145],[30,255,204]],[[8,56,205],[40,255,255]],[[96,25,85],
          [140,255,255]],[[36,84,76],[100,255,255]]],dtype='uint8')
ranges=np.array(r,dtype='uint8')
#Brown, yellow, blue, green

Cmap=np.array([Colours],dtype='uint8')
Cmap=cv2.cvtColor(Cmap,cv2.COLOR_RGB2HSV)  #Not an image
print('hsv:',Cmap)
q,f=0,0
yorb=[]
colours_used=[]
#yorb=np.array([0],dtype='uint8')

while(q<4):
    
    k=0     #Brown or Yellow
    if Cmap[0][q][0]>ranges[k][0][0] and Cmap[0][q][0]<ranges[k+1][1][0]:
        yorb.append(Cmap[0][q])
        colours_used.append(q+1)
        m[f]=q
        #print(yorb)
        f=f+1
        if f==2:
            print("Yellow,brown:")
            
            if(yorb[0][2]<yorb[1][2]):   #Lower Value of V is brown
    
                print("Brown",yorb[0])
                print("Yellow/ochre",yorb[1])
                #Brown
                L=np.array(Colours[m[1]][::-1], dtype = "uint8")
                print("L:",L)
                Sigma=np.array([7, 7, 7][::-1], dtype = "uint8")
                print(L)
                z=np.zeros(image.shape[:2])
                
                colour_mask = cv2.inRange(image,L-Sigma,L+Sigma)
                z[colour_mask==255] = 255
                
                kernel = np.ones((20, 20), np.uint8)
                closing = cv2.morphologyEx(z, cv2.MORPH_CLOSE, kernel,iterations = 1)
                #closing=cv2.bitwise_not(closing)
                
                closing=np.array(closing,dtype='uint8')
                #_,closing = cv2.threshold(closing,0.,255.,cv2.THRESH_OTSU)
                
                cv2.imwrite("Mask Brown.jpg",closing)
                print("Works")
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
                     cv2.imwrite("ContourBrown.jpg",closing)
                    
                     # find smaller contours
                     for j in range(1,101):         #For a contour at a particular r 
                        scalingFactor = j/100.0
                        color = 255 - (2.25*j)
                        contourClone = c.copy()
                        for i in contourClone:     #For every pt in that contour
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
                noise_img = random_noise(closing, mode='gaussian', var=0.05**2)
                closing = (255*noise_img).astype(np.uint8)
                FB=cv2.bitwise_and(closing,con)
                FB=cv2.bitwise_and(FB,con)
                cv2.imwrite("Brown.jpg",FB)
                
                
                #Yellow/Ochre
                
                L=np.array(Colours[m[0]][::-1], dtype = "uint8")
                print("L:",L)
                Sigma=np.array([7, 7, 7][::-1], dtype = "uint8")
                print(L)
                z=np.zeros(image.shape[:2])
                
                colour_mask = cv2.inRange(image,L-Sigma,L+Sigma)
                z[colour_mask==255] = 255
                
                kernel = np.ones((20, 20), np.uint8)
                closing = cv2.morphologyEx(z, cv2.MORPH_CLOSE, kernel,iterations = 1)
                #closing=cv2.bitwise_not(closing)
                
                closing=np.array(closing,dtype='uint8')
                #_,closing = cv2.threshold(closing,0.,255.,cv2.THRESH_OTSU)
                
                cv2.imwrite("Mask Yellow.jpg",closing)
                print("Works")
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
                     cv2.imwrite("CYellow.jpg",closing)
                    
                     # find smaller contours
                     for j in range(1,101):         #For a contour at a particular r 
                        m = interp1d([1,101],[40,80])
                        j2=int(m(j))
                        scalingFactor = j/100.0
                        color = 255 - (2.25*j2)
                        contourClone = c.copy()
                        for i in contourClone:     #For every pt in that contour
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
                
                FY=cv2.bitwise_and(final,con)
                cv2.imwrite("ContourYellow.jpg",FY)
                
                
                
            else:
                #This colour is yellow/ochre. Lower Contouring Loop
                print("Brown",yorb[1])
                print("Yellow/ochre",yorb[0])
                #Brown
                L=np.array(Colours[m[0]][::-1], dtype = "uint8")
                print("L:",L)
                Sigma=np.array([7, 7, 7][::-1], dtype = "uint8")
                print(L)
                z=np.zeros(image.shape[:2])
                
                colour_mask = cv2.inRange(image,L-Sigma,L+Sigma)
                z[colour_mask==255] = 255
                
                kernel = np.ones((20, 20), np.uint8)
                closing = cv2.morphologyEx(z, cv2.MORPH_CLOSE, kernel,iterations = 1)
                #closing=cv2.bitwise_not(closing)
                
                closing=np.array(closing,dtype='uint8')
                #_,closing = cv2.threshold(closing,0.,255.,cv2.THRESH_OTSU)
                
                cv2.imwrite("Mask Brown.jpg",closing)
                print("Works")
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
                     cv2.imwrite("ContourBrown.jpg",closing)
                    
                     # find smaller contours
                     for j in range(1,101):         #For a contour at a particular r 
                        scalingFactor = j/100.0
                        color = 255 - (2.25*j)
                        contourClone = c.copy()
                        for i in contourClone:     #For every pt in that contour
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
                noise_img = random_noise(closing, mode='gaussian', var=0.05**2)
                closing = (255*noise_img).astype(np.uint8)
                FB=cv2.bitwise_and(closing,con)
                FB=cv2.bitwise_and(FB,con)
                cv2.imwrite("Brown.jpg",FB)
                
                
                #Yellow/Ochre
                
                L=np.array(Colours[m[1]][::-1], dtype = "uint8")
                print("L:",L)
                Sigma=np.array([7, 7, 7][::-1], dtype = "uint8")
                print(L)
                z=np.zeros(image.shape[:2])
                
                colour_mask = cv2.inRange(image,L-Sigma,L+Sigma)
                z[colour_mask==255] = 255
                
                kernel = np.ones((20, 20), np.uint8)
                closing = cv2.morphologyEx(z, cv2.MORPH_CLOSE, kernel,iterations = 1)
                #closing=cv2.bitwise_not(closing)
                
                closing=np.array(closing,dtype='uint8')
                #_,closing = cv2.threshold(closing,0.,255.,cv2.THRESH_OTSU)
                
                cv2.imwrite("Mask Yellow.jpg",closing)
                print("Works")
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
                     cv2.imwrite("CYellow.jpg",closing)
                    
                     # find smaller contours
                     for j in range(1,101):         #For a contour at a particular r 
                        m = interp1d([1,101],[40,80])
                        j2=int(m(j))
                        scalingFactor = j/100.0
                        color = 255 - (2.25*j2)
                        contourClone = c.copy()
                        for i in contourClone:     #For every pt in that contour
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
                
                FY=cv2.bitwise_and(final,con)
                cv2.imwrite("ContourYellow.jpg",FY)
                
    k=2     #Blue
    #Upper
    a=np.less_equal(Cmap[0][q][0],ranges[k][1][0])
    #print(a)
    high=np.all(a)
    #Lower
    b=np.greater(Cmap[0][q][0],ranges[k][0][0])
    low=np.all(b)
    if high and low:
       print("Blue",Cmap[0][q])  #No Operation so not needed
       colours_used.append(q+1)
    k=3    #Green
    #Upper
    a=np.less_equal(Cmap[0][q][0],ranges[k][1][0])
    #print(a)
    high=np.all(a)
    #Lower
    b=np.greater(Cmap[0][q],ranges[k][0][0])
    low=np.all(b)
    if high and low:
        print("Green",Cmap[0][q])  #Increase height by 10  
        colours_used.append(q+1)
        #Green
        
        L=np.array(Colours[q][::-1], dtype = "uint8")
        print("L:",L)
        Sigma=np.array([7, 7, 7][::-1], dtype = "uint8")
        print(L)
        z=np.zeros(image.shape[:2])
        
        colour_mask = cv2.inRange(image,L-Sigma,L+Sigma)
        z[colour_mask==255] = 50
        
        kernel = np.ones((20, 20), np.uint8)
        closing = cv2.morphologyEx(z, cv2.MORPH_CLOSE, kernel,iterations = 1)
        #closing=cv2.bitwise_not(closing)
        
        
        closing=np.array(closing,dtype='uint8')
        clcopy=closing.copy()
        #_,closing = cv2.threshold(closing,0.,255.,cv2.THRESH_OTSU)
        noise_img = random_noise(closing, mode='gaussian', var=0.05**2)
        closing = (255*noise_img).astype(np.uint8)
        closing=np.array(closing,dtype='uint8')
        cv2.imwrite("Green.jpg",closing)
        gre=cv2.imread("Green.jpg",0)
        FG=cv2.bitwise_and(gre,clcopy)
        cv2.imwrite("Greengrass.jpg",FG)
        print("Works")
       
    q=q+1
final2=cv2.bitwise_or(FG,FY)
final2=cv2.bitwise_or(final2,FB)
cv2.imwrite("final2.jpg",final2)