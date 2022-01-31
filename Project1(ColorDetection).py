import cv2
import numpy as np

# video=cv2.VideoCapture(0)
# # 3 4 10 are id numbers for different specifications
# video.set(3,640) #width
# video.set(4,480) #height
# video.set(10,100) #brightness

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

myColors= [[141,103,159,172,255,255], 
           [73,154,77,93,255,255],
           [114,136,115,128,254,255]] 
#hue min,hue max,sat min,sat max,value min,value max  141,172,103,255,159,255

myColorValues=[[153,51,255],
               [0,102,0],   #BGR
               [102,0,102]]

myPoints=[ ] #x,y,colorId
def findColor(img,myColors,myColorValues):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower=np.array(color[0:3])
        upper=np.array(color[3:6])
        mask=cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgresult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
        # cv2.imshow(str(color[0]),mask) 
    return newPoints

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgresult,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgresult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)

while True:
    success,img=cap.read()
    imgresult=img.copy()
    newPoints=findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newp in newPoints:
            myPoints.append(newp)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("output",imgresult)
    if cv2.waitKey(1) & 0xFF==ord('q'): #press q to end
        break