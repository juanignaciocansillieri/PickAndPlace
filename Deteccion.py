import cv2
import numpy as np
puntos = []
def dibujar(mask,color):    
  contornos,hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 700:
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      nuevoContorno = cv2.convexHull(c)
      puntos.insert(0,(x,y))
      if len(puntos) > 4:
        puntos.pop()
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      if len(puntos) == 4:
      #List coordinates of vertices as an array
        pts = np.array([[puntos[1]],[puntos[0]],[puntos[2]],[puntos[3]]], np.int32)
        pts = pts.reshape((-1,1,2))
        #Draw lines from vertex to vertex
        cv2.polylines(frame, [pts], True, (255,0,0))
      cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
      cv2.drawContours(frame, [nuevoContorno], 0, color, 3)


cap = cv2.VideoCapture(0)

azulBajo = np.array([38,100,100],np.uint8)
azulAlto = np.array([159,255,255],np.uint8)

amarilloBajo = np.array([15,100,20],np.uint8)
amarilloAlto = np.array([45,255,255],np.uint8)

redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

redBajo2 = np.array([175,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX
while True:

  ret,frame = cap.read()

  if ret == True:
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
    maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
    maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
    maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
    maskRed = cv2.add(maskRed1,maskRed2)
    dibujar(maskAzul,(255,0,0))
    dibujar(maskAmarillo,(0,255,255))
    dibujar(maskRed,(0,0,255))
    frame = cv2.resize(frame, (640, 480)) # RESIZE IMAGE

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      break
cap.release()
cv2.destroyAllWindows()