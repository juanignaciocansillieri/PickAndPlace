from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np
import Perspectiva as p
from Perspectiva import imgWarpColored
cap = None

root = Tk()

#root.geometry("1350x700+0+0")

def visualizar():
    global cap
    global maskAmarillo
    #cap = cv2.VideoCapture(0)
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
    
            lblVideo2.configure(image=img)
            lblVideo2.image = img
            p.buscarMarcas(frame)
            
            lblVideo2.after(15, visualizar)
            
        else:
            
            lblVideo2.image = ""
            cap.release()

def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    visualizar()


lblTitulo = Label(root,text="PICK & PLACE")
btnIniciar = Button(root, text="Calibrar",width=45,command=iniciar)
btnIniciar.grid(column=0,row=1,padx=10,pady=5)
lblTitulo.grid(column=0,row=0,padx=5,pady=5)


lblVideo2 = Label(root)
lblVideo2.grid(column=0,row=2,columnspan=2)

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

font = cv2.FONT_HERSHEY_SIMPLEX

root.mainloop()


