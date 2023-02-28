
import cv2
import numpy as np
#Final:
#Brown
B=(4,99,145),(20,255,204)
#Yellow/Ochre
Y=(12.5,56,205),(20,255,255)
#Blue
BL=(91,25,85),(130,255,255)
#Green
G=(36,84,76),(80,255,255)    

r=np.array([[[0,99,145],[30,255,204]],[[8,56,205],[30,255,255]],[[96,25,85],
          [130,255,255]],[[36,84,76],[95,255,255]]],dtype='uint8')
range=np.array(r,dtype='uint8')
#Brown, yellow, blue, green

Colour=[[173, 157, 105], [54, 154, 210], [208, 213, 197], [87, 79, 34]]
Cmap=np.array([Colour],dtype='uint8')
Cmap=cv2.cvtColor(Cmap,cv2.COLOR_RGB2HSV)  
print(Cmap)
"""a=np.greater(Cmap[0][3],range[1][0])
print(a)
low=np.any(a)
high=np.all(a)
print(low,high)"""
q,f=0,0
yorb=[]
#yorb=np.array([0],dtype='uint8')
while(q<4):
    """pixel=Cmap[0][q]
    upper=range[k][1]
    lower=range[k][0]
    pixel=Cmap[0][q][0]
    upper=range[k][1][0]
    lower=range[k][0][0]"""
    k=2     #Blue
    #Upper
    a=np.less_equal(Cmap[0][q][0],range[k][1][0])
    #print(a)
    high=np.all(a)
    #Lower
    b=np.greater(Cmap[0][q][0],range[k][0][0])
    low=np.all(b)
    if high and low:
       print("Blue",Cmap[0][q])  #No Operation so not needed
    k=3    #Green
    #Upper
    a=np.less_equal(Cmap[0][q][0],range[k][1][0])
    #print(a)
    high=np.all(a)
    #Lower
    b=np.greater(Cmap[0][q],range[k][0][0])
    low=np.all(b)
    if high and low:
       print("Green",Cmap[0][q])  #Increase height by 10  
    k=0     #Brown or Yellow
    if Cmap[0][q][0]>range[k][0][0] and Cmap[0][q][0]<range[k+1][1][0]:
        yorb.append(Cmap[0][q])
        #print(yorb)
        f=f+1
        if f==2:
            print("Yellow,brown:")
            
            if(yorb[0][2]<yorb[1][2]):   #Lower Value of V is brown
                #This colour is brown. Contouring Loop
                print("Brown",yorb[0])
                print("Yellow/ochre",yorb[1])

            else:
                #This colour is yellow/ochre. Lower Contouring Loop
                print("Brown",yorb[1])

                print("Yellow/ochre",yorb[0])
    q=q+1