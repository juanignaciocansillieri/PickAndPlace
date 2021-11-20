import cv2
import numpy as np
import time
from time import gmtime, strftime
import datetime
import Transformaciones as t
import FinalDobot as d

"""
    * @author Cansillieri Juan Ignacio, Laboratorio de Robótica - 2021.
"""

###############GLOBALES############

arrayPuntos = [] # array donde se guardan los x,y de las MARCAS fiduciarias
arrayPosicionesObjeto = [] # array donde se guardan los x,y con su respectivo tiempo del OBJETO identificado
frameRectificado = "" 
velocidad=0
tiempo_recorrido=0

#################### LEEMOS POSICIONES ARCHIVO DE TEXTOS ##############
ruta = "posiciones.txt"
archivo = open(ruta,'r')
arrayPosiciones = archivo.readlines()

####### ASIGNAMOS LOS VALORES #######  *¡MUY IMPORTANTE EL ORDEN EN EL ARCHIVO!*

c1cx = int(arrayPosiciones[0])
c1cy = int(arrayPosiciones[1]) 
c2cx = int(arrayPosiciones[2]) 
c2cy = int(arrayPosiciones[3]) 
c1rx = int(arrayPosiciones[4]) 
c1ry = int(arrayPosiciones[5]) 
c2rx = int(arrayPosiciones[6]) 
c2ry = int(arrayPosiciones[7]) 

### FORMAMOS LA MATRIZ #######
matrizTransformacion = t.armaMatriz(c1cx, c1cy, c2cx, c2cy, c1rx, c1ry, c2rx, c2ry)


"""
     * Busca las 4 marcas representadas en colores y las guarda en un array

     * @param frame (video)

     * IMPORTANTE: Si se desea cambiar el color de las marcas se deberá buscar los rangos de dichos colores(bajo-alto) en el formato HSV
     * y realizar las máscaras con los mismos.
 """
 
def buscarMarcas(frame):

  global arrayPuntos
  
  ######## PREPARAR MÁSCARAS PARA LA DETECCIÓN DE COLORES  ######
  frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  # *IMPORTANTE* Convertir el frame a HSV con el parámetro cv2.BGR2HSV

  maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
  maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
  maskVerde = cv2.inRange(frameHSV,verdeBajo,verdeAlto)
  maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
  maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
  maskRed = cv2.add(maskRed1,maskRed2)
  maskRed = cv2.add(maskRed1,maskRed2)

  # Encuentra el amarillo y lo guarda
  if len(arrayPuntos) ==0:
    detectarColor(maskAmarillo,0)

  # Una vez que esta el amarillo, busca el azul
  if len(arrayPuntos)==1:
    detectarColor(maskAzul,1)

  # Busca rojo    
  if len(arrayPuntos)==2:
    detectarColor(maskRed,2)

  # Buscar verde
  if len(arrayPuntos)==3:
    detectarColor(maskVerde,3)

      # Si ya tenemos los 4 puntos guardados  
  if len(arrayPuntos) == 4:
        # Hacemos una matriz con los puntos que detectamos
       realizarPerspectiva(frame)
      
"""
     * Realiza el rectificado de la imagen: forma 2 matrices, una con los puntos x,y de cada marca encontrada
     * y otro con los bordes de la nueva imagen
     *
     * @param frame (video)
 """

def realizarPerspectiva(frame):

        global frameRectificado
        global arrayPuntos

        pts = np.array([[arrayPuntos[0]],[arrayPuntos[1]],[arrayPuntos[3]],[arrayPuntos[2]]], np.int32) #Matriz de posiciones de marcas
        pts = pts.reshape((-1,1,2))

        cv2.polylines(frame, [pts], True, (255,0,0)) # forma polinomio con los untos de las marcas (solo visual)

        pts1 = np.float32(arrayPuntos) # PREPARAMOS PUNTOS PARA EL WARP #Imagen que detectamos
        pts2 = np.float32([[0, 0],[480, 0], [0, 640],[480, 640]]) # Matriz 4 bordes de la nueva imagen

        matrizPerspectiva = cv2.getPerspectiveTransform(pts1, pts2) # Realizamos la perspectiva (nueva matriz)

        frameRectificado = cv2.warpPerspective(frame, matrizPerspectiva, (480, 640)) # Frame final rectificado, se debe especificar ancho y largo.
        frameRectificado=frameRectificado[20:frameRectificado.shape[0] - 20, 20:frameRectificado.shape[1] - 20] # Recortar bordes
        cv2.imshow("Imagen Rectificada",frameRectificado) # Mostrar ventana rectificada
        
        if frameRectificado.any(): # Verificación si existe el nuevo frame rectificado, si es así busca el objeto
          buscarObjeto(frameRectificado)

"""
     * Buscamos el objeto por color especificado en la pantalla rectificada 
     * y guardamos su posición(x,y) y tiempo (ms) *
     * @param  frame (video)
 """
       
def buscarObjeto(frame):

        global arrayPuntos
        global arrayPosicionesObjeto
        global velocidad
        global tiempo_recorrido
        ### COLOR DEL OBJETO ###
        frameHSV2 = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        redBajo1 = np.array([0,100,20],np.uint8)
        redAlto1 = np.array([5,255,255],np.uint8)
        redBajo2 = np.array([175,100,20],np.uint8)
        redAlto2 = np.array([179,255,255],np.uint8)
        
        maskRed1 = cv2.inRange(frameHSV2,redBajo1,redAlto1)
        maskRed2 = cv2.inRange(frameHSV2,redBajo2,redAlto2)
        maskRed = cv2.add(maskRed1,maskRed2)

        """
        # Se busca  objetos del color de la máscara, en este caso rojo.
        #*** Si se desea cambiar el color, modificar la máscara y los rangos de colores***  
        """
        countors,hierachy = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        for c in countors:
          area = cv2.contourArea(c)
          if area > 100:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1  # PUNTO CENTRAL DEL OBJETO Y SUS RESPECTIVOS (x,y)
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])

            tiempo = int(round(time.time() * 1000)) #tiempo en milisegundos

            arrayPosicionesObjeto.append((x,y,tiempo)) # Agregamos al array: la posición x,y seguido del tiempo (ms) 
            # Se guarda sólo las últimas 20 posiciones. *FIFO*
            if len(arrayPosicionesObjeto) > 13:
              arrayPosicionesObjeto.pop(0)

              ## Cálculo de distancia y tiempo para calcular la velocidad # abs es valor absoluto
              distancia = abs(arrayPosicionesObjeto[12][1]) - abs(arrayPosicionesObjeto[0][1]) # distancia entre la última y primera posición
              tiempo_recorrido = abs(arrayPosicionesObjeto[12][2]) - abs(arrayPosicionesObjeto[0][2]) # idem pero con tiempo
              velocidad = distancia/tiempo_recorrido 
              
        

"""
     * Realiza la transformación del último punto del objeto a atrapar.
     * @return posición x,y transformada
 """
 
def agarrarObjeto():
  
  global arrayPosicionesObjeto
  global matrizTransformacion
  global c1cx
  global velocidad
  global tiempo_recorrido

  retardoRobot = 5950
  # (x,y) de la última posición encontrada antes de hacer click en SPACE
  x = arrayPosicionesObjeto[0][0]    
  y = arrayPosicionesObjeto[0][1]
  #Cuando esta en movimiento, se predice su posición en y, ya que sólo esta varía.
  # Se multiplica la velocidad por el retardo promedio del robot, desde que hacemos click hasta que agarra el objeto, y al resultado del producto
  # se le suma la posición en la que estaba.
  yfinal=(velocidad*retardoRobot)+y 


  xyRobot = t.transforma(matrizTransformacion,x,yfinal) # Realizar transformación con los puntos x,y del objeto
    


  ### Se realizan ajustes a la presición x resultante de la transformación 
  if c1rx - 10 <xyRobot[0]< c1rx+10 : # verifica el objeto está en las marcas iniciales
   xyRobot[0]= xyRobot[0]
  else:
    xyRobot[0] = c1rx * 2 - xyRobot[0] + 20
  ## PASAMOS LAS COORDENADAS AL DOBOT PARA QUE AGARRE EL OBJETO.
  d.agarrarObjeto(xyRobot[0],xyRobot[1])



"""
     *Funcion para encontrar contornos del color de la máscara, 
     * recibimos la máscara, y el id para  ubicarlo en el array de forma ordenada por color*
     * @param mask (máscara de color)
     * @param frame (video)
     * @param id (int)
 """
def detectarColor(mask,id):  
  contornos,hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for c in contornos:
    area = cv2.contourArea(c)
    if area > 400: # ÁREA MÍNIMA DEL OBJETO A BUSCAR # IMPORTANTE SI EL OBJETO ESTA MUY LEJOS, DISMINUIR #
      M = cv2.moments(c)
      if (M["m00"]==0): M["m00"]=1  ##    PUNTO CENTRAL DEL OBJETO DETECTADO
      x = int(M["m10"]/M["m00"])    ## X    ""         ""    ""
      y = int(M['m01']/M['m00'])    ## Y     ""        ""    ""
      nuevoContorno = cv2.convexHull(c)
      if len(arrayPuntos) == id:  # ID: 0 - AMARILLO | 1 - AZUL | 2 - ROJO | 3 - VERDE 
        arrayPuntos.insert(id,(x,y)) # AGREGAMOS AL ARRAY EN LA POSICIÓN DEL ID, LA POSICIÓN X,Y

      

######### RANGO DE COLORES HSV #######################
# RANGOS HSV: https://omes-va.com/wp-content/uploads/2019/09/gyuw4.png

amarilloBajo = np.array([20,100,20],np.uint8)
amarilloAlto = np.array([30,255,255],np.uint8)

#verdeBajo = np.array([40, 40,40],np.uint8)
#verdeAlto = np.array([70, 255,255],np.uint8)

verdeBajo = np.array([38,100,100],np.uint8)
verdeAlto = np.array([159,255,255],np.uint8)

azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

amarilloBajo = np.array([20,100,20],np.uint8)
amarilloAlto = np.array([30,255,255],np.uint8)

redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

redBajo2 = np.array([175,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)

##############################################

### Empezar captura (webcam), el primer parámetro es el ID de la cámara; si no se reconoce cambiarlo a 1##
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
  ret,frame = cap.read()
  if ret == True:
    frame = cv2.resize(frame, (640, 480)) # CAMBIAR EL TAMAÑO DE LA IMAGEN
    buscarMarcas(frame)  #BUSCAR MARCAS FIDUCIARIAS
    cv2.imshow('Imagen Original',frame) # MOSTRAR VIDEO
    k = cv2.waitKey(1)  
    if k & 0xFF == ord('s'):
      break  # CERRAR AL PRESIONAR TECLA 'S'
    elif k == 32:
      if frameRectificado.any(): # VERIFICAR QUE IMAGEN RECTIFICADA EXISTE
          agarrarObjeto() # AGARRAR OBJETO SI PRECIONAMOS TECLA 'SPACE'
        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

