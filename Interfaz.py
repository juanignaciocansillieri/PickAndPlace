from tkinter import *
from PIL import ImageTk, Image
import os


def next_frame(nframe):
    nframe.tkraise()

## Ejecuta el programa al hacer click en el botón
def ejecutar_programa():
    os.system('python Perspectiva.py')


root = Tk()
root.title("Pick&Place")
# 1920x1080 es el tamaño de la ventana empezando en (0,0)
root.geometry("1350x700+0+0")
# root.configure(bg="#0b3954")

main_frame = Frame(root, bg="#0b3954")
pyp_frame = Frame(root)

for frame in (main_frame, pyp_frame):
    frame.place(x=0, y=0, relheight=1, relwidth=1)

pyp_frame.tkraise()

# P&P GUI
pyp_frame.configure(bg="#0b3954")

infcframe = Frame(pyp_frame)
infcframe.place(x=250, y=100, height=500, width=800)

load = Image.open("Images/descarga.jpeg")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.place(x=653, y=112, height=398, width=395)
fcLabel3 = Label(infcframe, text="\n\nEn este proyecto,\nse calibrará la cámara,se identificará el objeto\nsu posición y velocidad para que\nDobot lo atrape.\n\nA tener en cuenta:\n\n1.Cámara conectada\n2. Una vez que aparezca la imagen rectificada\n y se ubique el objeto, presionar SPACE\n para ordenar atraparlo.\n3.Presiona S para salir del programa.", justify=LEFT, font=("Times", 15))
fcLabel3.place(x=20, y=0.1, height=400, width=370)
fcLabel1 = Label(infcframe, text="Pick & Place", relief=SUNKEN,
                 justify=CENTER, font=("Arial Bold", 25))
fcLabel1.place(x=25, y=25, height=50, width=350)
fcLabel2 = Label(infcframe, relief=SUNKEN)
fcLabel2.place(x=400, y=10, height=400, width=415)


fcStatus_label = Label(infcframe, relief=SUNKEN)
fcStatus_label.place(x=15, y=420, height=90, width=800)
fcstatus_Button = Button(infcframe, text="Ejecutar Programa", command=ejecutar_programa)
fcstatus_Button.place(height=70, width=200,  x=500, y=425)

fcback_Button = Button(infcframe, text="Back",
                       command=lambda: next_frame(main_frame))
fcback_Button.place(height=70, width=250,  x=100, y=425)


# INTERFAZ PRINCIPAL
TitleHead = Label(main_frame, text="Seminario Robótica",
                  font=("Roboto", 75), bg='#0b3954', fg='#ffffff')
TitleHead.place(x=200, y=50)


Button1 = Button(main_frame, text="Pick&Place",
                 command=lambda: next_frame(pyp_frame))
Button1.place(x=590, y=220, height=25, width=200)


root.mainloop()
