from serial.tools import list_ports
import pydobot;
import time;

def agarrarObjeto(xfinal,yfinal):
    available_ports = list_ports.comports()
    #print(f'available ports: {[x.device for x in available_ports]}')
    port = available_ports[0].device

    device = pydobot.Dobot(port=port, verbose=True)

    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    #print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
    #print(f'r:{r} ')

    device.move_to(xfinal, yfinal, 80 , r, wait=True)
    device.move_to(xfinal, yfinal, 55 , r, wait=True)

    device.grip(True)

    device.move_to(202, -262, 107 , -23, wait=True)

    device.grip(False)

    device.close()