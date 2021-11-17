import math
import numpy as np
import matplotlib.pyplot as plt

"""
    *
    * @author Gustavo Sbrugnera, para UNSTA-FI, Laboratorio de Robótica - 2021.
"""
"""
     * Calcula la distancia entre dos puntos "a" y "b" en el plano
     *
     * @param ax
     * @param ay
     * @param bx
     * @param by
     * @return
 """
def distanciaEntrePuntos(ax, ay, bx, by) :
        # Hipotenusa del triángulo rectángulo
        return math.hypot((bx - ax), (by - ay))
    

"""
     * Devuelve la orientación (en radianes) de un segmento que va desde el
     * origen hasta "a", respecto del semieje positivo X. El rango devuelto está
     * entre -PI, PI Ver:
     * https:#docs.oracle.com/en/java/javase/11/docs/api/java.base/java/lang/math.html#atan2(double,double)
     *
     * @param ax
     * @param ay
     * @return
 """
def orientacion1(ax, ay) :
        return math.atan2(ay, ax)
    

"""
     * Devuelve la orientación (en radianes) de un segmento que va desde "a"
     * hasta "b", respecto del semieje positivo X. El rango devuelto está entre
     * -PI, PI
     *
     * @param ax
     * @param ay
     * @return
 """
def orientacion(ax, ay, bx, by):
        return orientacion1(bx - ax, by - ay)
    

"""
     * Devuelve el ángulo (en radianes, contra-reloj) que habría que girar el
     * segmento "a-b" para que se oriente como el segmento "c-d"
     *
     * @param ax
     * @param ay
     * @param bx
     * @param by
     * @param cx
     * @param cy
     * @param dx
     * @param dy
     * @return
 """
def rotacion(ax, ay, bx, by,cx, cy, dx, dy):

        abOrientacion = orientacion(ax, ay, bx, by)
        cdOientacion = orientacion(cx, cy, dx, dy)

        return cdOientacion - abOrientacion
    

"""
     * Devuelve el factor de escala que hay que aplicar al segmento "a-b" para
     * convertirlo en el segmento "c-d"
     *
     * @param ax
     * @param ay
     * @param bx
     * @param by
     * @param cx
     * @param cy
     * @param dx
     * @param dy
     * @return
 """

def escala(ax, ay, bx, by,cx, cy, dx, dy):

        ab = distanciaEntrePuntos(ax, ay, bx, by)
        cd = distanciaEntrePuntos(cx, cy, dx, dy)

        if (ab == 0.0) :
           raise Exception("Longitud del segmento a-b es cero")
         # end if
        return cd / ab
    

"""
     * Arma la matriz de transformación lineal para convertir linealmente el
     * segmento "a-b" en "c-d"
     *
     * @param ax
     * @param ay
     * @param bx
     * @param by
     * @param cx
     * @param cy
     * @param dx
     * @param dy
     * @return
 """

def armaMatriz(ax, ay, bx,by, cx, cy, dx, dy):
        # Paso 1: calcula la escala
        escala1 = escala(ax, ay, bx, by, cx, cy, dx, dy)
        mEscala = armaMatrizEscala(escala1)

        # Paso 2: calcula la rotación
        angulo = rotacion(ax,ay, bx, by, cx, cy, dx, dy)
        mRotacion = armaMatrizRotacion(angulo)

        # Paso 3: arma la matriz intermedia de rotacion-escala
        mRotEsc = productoMatricial3x3(mEscala, mRotacion)
        
        # Paso 4: con la matriz intermedia, despaza el origen
        desp = transforma(mRotEsc, ax, ay)
        
        despX = cx - desp[0]
        despY = cy - desp[1]
        
        # Paso 5: calcula la matriz de desplazamiento
        mDesp = armaMatrizDesplazamiento(despX, despY)
        
        # Paso 6: consolida las tres matrices intermedias
        m = productoMatricial3x3(mDesp, mRotEsc)
                
        
        return m
    

"""
     * Aplica la matriz de transformación "m" al punto "p" y devuelve el punto
     * transformado "q", en un vector de dos elementos
     *
     * @param m
     * @param px
     * @param py
     * @return
 """

def transforma(m, px, py) :

        a = m[0][0]
        b = m[0][1]
        c = m[0][2]
        d = m[1][0]
        e = m[1][1]
        f = m[1][2]
        g = m[2][0]
        h = m[2][1]
        i = m[2][2]

        pz = 1

        qx = a * px + b * py + c * pz
        qy = d * px + e * py + f * pz
        qz = g * px + h * py + i * pz

        q = [qx, qy, qz]

        return q
    

        """
            * Arma la matriz de desplazamiento 3x3
            *
            * @param despx
            * @param despy
            * @return
        """
def armaMatrizDesplazamiento(despx, despy) :
        m = np.array([[1,0,despx],[0,1,despy],[0,0,1]])
        """
            m[0][0] = 1
            m[0][1] = 0
            m[0][2] = despx
            m[1][0] = 0
            m[1][1] = 1
            m[1][2] = despy
            m[2][0] = 0
            m[2][1] = 0
            m[2][2] = 1
        """
        return m
    

"""
     * Devuelve la matriz de transformación 3x3 para girar alrededor del origen.
     * Angulo en radianes, sentido anti-horario positivo
     *
     * @param angulo
     * @return
 """
def armaMatrizRotacion(angulo) :
        m = np.array([[math.cos(angulo),-math.sin(angulo),0],[math.sin(angulo),math.cos(angulo),0],[0,0,1]])
        """
            m[0][0] = math.cos(angulo)
            m[0][1] = -math.sin(angulo)
            m[0][2] = 0

            m[1][0] = -m[0][1] # math.sin(angulo)
            m[1][1] = m[0][0] # math.cos(angulo)
            m[1][2] = 0

            m[2][0] = 0
            m[2][1] = 0
            m[2][2] = 1
        """
        return m
    

"""
     * Arma la matriz de escala 3x3 alrededor del origen
     *
     * @param factor
     * @return
 """
def armaMatrizEscala(factor) :
        m = np.array([[factor,0,0],[0,factor,0],[0,0,1]])
        """
            m[0][0] = factor
            m[0][1] = 0
            m[0][2] = 0

            m[1][0] = 0
            m[1][1] = factor
            m[1][2] = 0

            m[2][0] = 0
            m[2][1] = 0
            m[2][2] = 1
        """
        return m
    

"""
     * Calcula el producto matricial entre dos matrices A x B, cada una de 3x3
     *
     * @param mA
     * @param mB
     * @return
 """
def productoMatricial3x3(mA, mB) :

        mP = np.dot(mA,mB)
        """
            aA = mA[0][0]
            bA = mA[0][1]
            cA = mA[0][2]
        dA = mA[1][0]
            eA = mA[1][1]
            fA = mA[1][2]
            gA = mA[2][0]
            hA = mA[2][1]
            iA = mA[2][2]

            aB = mB[0][0]
            bB = mB[0][1]
            cB = mB[0][2]
        dB = mB[1][0]
            eB = mB[1][1]
            fB = mB[1][2]
            gB = mB[2][0]
            hB = mB[2][1]
            iB = mB[2][2]

            mP = [3][3]

            mP[0][0] = aA * aB + bA * dB + cA * gB
            mP[0][1] = aA * bB + bA * eB + cA * hB
            mP[0][2] = aA * cB + bA * fB + cA * iB
            mP[1][0] = dA * aB + eA * dB + fA * gB
            mP[1][1] = dA * bB + eA * eB + fA * hB
            mP[1][2] = dA * cB + eA * fB + fA * iB
            mP[2][0] = gA * aB + hA * dB + iA * gB
            mP[2][1] = gA * bB + hA * eB + iA * hB
            mP[2][2] = gA * cB + hA * fB + iA * iB
        """
        return mP

A=np.array([[1,2,3],[3,4,2],[5,6,1]]) 
B=np.array([[1,2,3],[3,4,5],[1,2,3]])

c1cx = 100
c1cy = 250

c2cx = 400
c2cy = 260

c1rx = 450
c1ry = 420

c2rx = 110
c2ry = 160

plt.plot([c1cx,c1cy],[c2cx,c2cy],color = 'green')
plt.plot([c1rx,c1ry],[c2rx,c2ry],color = 'red')

m = armaMatriz(c1cx, c1cy, c2cx, c2cy, c1rx, c1ry, c2rx, c2ry)

c1r = transforma(m, c1cx, c1cy)
c2r = transforma(m, c2cx, c2cy)

plt.plot([c1r[0], c1r[1]], [c2r[0], c2r[1]],color = 'black')

plt.show()

D = armaMatriz(123,135,263,246,254,237,532,342)
print(D)

