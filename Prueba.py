import cv2
import numpy as np
puntos = []
i = 0
imgWarpColored = ""
maskAmarillo = ""

def findCountours(mask, i):
    global puntos
    contornos, hierachy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 400:
              M = cv2.moments(c)
              if (M["m00"] == 0):
                    M["m00"] = 1
                    x = int(M["m10"]/M["m00"])
                    y = int(M['m01']/M['m00'])
                    nuevoContorno = cv2.convexHull(c)
                    puntos.insert(i, (x, y))


def dibujar(frame):
    global imgWarpColored
    global puntos
    if len(puntos) == 0:
        print("oal")
        findCountours(maskAmarillo, 0)
    if len(puntos) == 1:
        findCountours(maskAzul, 1)

    if len(puntos) == 2:
        findCountours(maskRed, 2)

    if len(puntos) == 3:
        findCountours(maskVerde, 3)

    if len(puntos) == 4:
        pts = np.array([[puntos[0]], [puntos[1]], [
                       puntos[3]], [puntos[2]]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        # Draw lines from vertex to vertex
        cv2.polylines(frame, [pts], True, (255, 0, 0))
        pts1 = np.float32(puntos)  # PREPARE POINTS FOR WARP
        # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0], [480, 0], [0, 640], [480, 640]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(frame, matrix, (480, 640))

        # REMOVE 20 PIXELS FORM EACH SIDE
        imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] -
                                        20, 20:imgWarpColored.shape[1] - 20]
        imgWarpColored = cv2.resize(imgWarpColored, (480, 640))

        # APPLY ADAPTIVE THRESHOLD
        cv2.imshow("", imgWarpColored)
        if imgWarpColored.any():
            buscarObjeto(imgWarpColored)


def buscarObjeto(img):

    frameHSV2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    amarilloBajo2 = np.array([20, 100, 20], np.uint8)
    amarilloAlto2 = np.array([30, 255, 255], np.uint8)
    maskVerde2 = cv2.inRange(frameHSV2, amarilloBajo2, amarilloAlto2)

    countors, hierachy = cv2.findContours(
        maskVerde2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in countors:
        area2 = cv2.contourArea(c)
        if area2 > 400:
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            print("Puntos x,y: "+str((x, y)))
            newContour = cv2.convexHull(c)
            cv2.circle(img, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(img, '{},{}'.format(x, y), (x+10, y), font, 0.75, (0, 255, 0),1,cv2.LINE_AA)
            cv2.drawContours(img, [newContour], 0, (255, 255, 255), 3)


def dibujarVerde(mask, color):
    contornos, hierachy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 400:
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            nuevoContorno = cv2.convexHull(c)
            if len(puntos) == 3:
                puntos.insert(3, (x, y))
                print("verde", puntos)
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(frame, '{},{}'.format(x, y), (x+10, y), font, 0.75, (0, 255, 0),1,cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)


def dibujarRojo(mask, color):
    contornos, hierachy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 400:
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            nuevoContorno = cv2.convexHull(c)
            if len(puntos) == 2:
                puntos.insert(2, (x, y))
                print("rojo", puntos)

            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(frame, '{},{}'.format(x, y), (x+10, y), font, 0.75, (0, 255, 0),1,cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)


def dibujarAzul(mask):
    contornos, hierachy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 400:
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            nuevoContorno = cv2.convexHull(c)
            if len(puntos) == 1:
                puntos.insert(1, (x, y))
                print("azul", puntos)

            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(frame, '{},{}'.format(x, y), (x+10, y), font, 0.75, (0, 255, 0),1,cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, (0, 0, 0), 3)


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

verdeBajo = np.array([38, 100, 100], np.uint8)
verdeAlto = np.array([159, 255, 255], np.uint8)

azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

amarilloBajo = np.array([20, 100, 20], np.uint8)
amarilloAlto = np.array([30, 255, 255], np.uint8)

redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([5, 255, 255], np.uint8)

redBajo2 = np.array([175, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX
while True:

    ret, frame = cap.read()

    if ret == True:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
        maskVerde = cv2.inRange(frameHSV, verdeBajo, verdeAlto)
        maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
        maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
        maskRed = cv2.add(maskRed1, maskRed2)
        dibujar(frame)
        # dibujarAzul(maskAzul)
        # dibujarRojo(maskRed,(0,0,255))
        # dibujarVerde(maskVerde,(0,0,255))
        frame = cv2.resize(frame, (640, 480))  # RESIZE IMAGE

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
cap.release()
cv2.destroyAllWindows()
