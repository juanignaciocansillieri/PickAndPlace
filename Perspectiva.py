import cv2
import numpy as np
import time
from time import gmtime, strftime
puntos = []
i = 0
imgWarpColored = ""
xy = []
def buscarMarcas(frame):

  global puntos
  ######## PREPARAR MÁSCARAS PARA LA DETECCIÓN DE COLORES  ######
  frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
  maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
  maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
  maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
  maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
  maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
  maskRed = cv2.add(maskRed1,maskRed2)
  maskRed = cv2.add(maskRed1,maskRed2)

  # Encuentra el amarillo y lo guarda
  if len(puntos) ==0:
    detectarColor(maskAmarillo,frame,0)

  # Una vez que esta el amarillo, busca el azul
  if len(puntos)==1:
    detectarColor(maskAzul,frame,1)

  # Busca rojo    
  if len(puntos)==2:
    detectarColor(maskRed,frame,2)

  # Buscar verde
  if len(puntos)==3:
    detectarColor(maskVerde,frame,3)

      # Si ya tenemos los 4 puntos guardados  
  if len(puntos) == 4:
        # Hacemos una matriz con los puntos que detectamos
       realizarPerspectiva(frame)
      

def realizarPerspectiva(frame):
        global imgWarpColored
        global puntos
        pts = np.array([[puntos[0]],[puntos[1]],[puntos[3]],[puntos[2]]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame, [pts], True, (255,0,0))
        pts1 = np.float32(puntos) # PREPARAMOS PUNTOS PARA EL WARP #Imagen que detectamos
        pts2 = np.float32([[0, 0],[480, 0], [0, 640],[480, 640]]) # PREPARAMOS PUNTOS PARA EL WARP # los 4 bordes
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # Realizamos la perspectiva
        imgWarpColored = cv2.warpPerspective(frame, matrix, (480, 640)) # Frame final rectificado
        imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        cv2.imshow("",imgWarpColored)
        if imgWarpColored.any():
          buscarObjeto(imgWarpColored)

# Función para Buscar el objeto en la pantalla rectificada        
def buscarObjeto(img):

        global puntos
        global xy
        frameHSV2 = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        redBajo1 = np.array([0,100,20],np.uint8)
        redAlto1 = np.array([5,255,255],np.uint8)
        redBajo2 = np.array([175,100,20],np.uint8)
        redAlto2 = np.array([179,255,255],np.uint8)
        
        maskRed1 = cv2.inRange(frameHSV2,redBajo1,redAlto1)
        maskRed2 = cv2.inRange(frameHSV2,redBajo2,redAlto2)
        maskRed = cv2.add(maskRed1,maskRed2)

        countors,hierachy = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in countors:
          area2 = cv2.contourArea(c)
          if area2 > 0:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            xy.append((x,y,strftime("%M:%S", gmtime())))
            if len(xy) > 20:
              xy.pop(0)
        

def agarrarObjeto():
  global xy
  print(xy)
# Funcion para encontrar contornos del color de la máscara # 
#recibimos la máscara, y el id para  ubicarlo en el array
def detectarColor(mask,frame,id):  
  contornos,hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 400:
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1
      x = int(M["m10"]/M["m00"])
      y = int(M['m01']/M['m00'])
      nuevoContorno = cv2.convexHull(c)
      if len(puntos) == id:
        puntos.insert(id,(x,y))
  
      cv2.circle(frame,(x,y),7,(0,255,0),-1)
      cv2.drawContours(frame, [nuevoContorno], 0, (0,0,0), 3)


      

######### RANGO DE COLORES HSV #######################

amarilloBajo = np.array([20,100,20],np.uint8)
amarilloAlto = np.array([30,255,255],np.uint8)

verdeBajo = np.array([40, 40,40],np.uint8)
verdeAlto = np.array([70, 255,255],np.uint8)

azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

amarilloBajo = np.array([20,100,20],np.uint8)
amarilloAlto = np.array([30,255,255],np.uint8)

redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

redBajo2 = np.array([175,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)

##############################################

### Empezar captura (webcam) ##
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
  ret,frame = cap.read()
  if ret == True:
    frame = cv2.resize(frame, (640, 480)) # RESIZE IMAGE
    buscarMarcas(frame)
    cv2.imshow('frame',frame)
    k = cv2.waitKey(1)
    if k & 0xFF == ord('s'):
      break
    elif k == 32:
      if imgWarpColored.any():
          agarrarObjeto()
        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

