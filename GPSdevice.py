from socket import *
from _thread import *
import random
import time
# Creating a GPS devices

# Variables
HOST = 'localhost'  # Direccion IP del servidor
PORT = 50010
server = (HOST, PORT)

cord1 = [1.0,1.0]
cord2 = [1.0,1.0]
cordR = [1.0,1.0]
inc = [1.0,1.0]
mov = [1.0,1.0]

lat = random.random()* 180 - 90
lon = random.random()* 360 - 180
cord1[0] = lat
cord1[1] = lon
cord2 = cord1
cordR = cord1
inc = [lat*0.0005, lon*0.0005]
mov = [lat*0.005, lon*0.005]

state = 1

# Crear el socket
sock = socket(AF_INET, SOCK_STREAM)

# Establecer coneccion
sock.connect(server)

def sender():
    message = 'GPS1: \n\tLAT: ' + str(cord1[0]) +' LON: ' + str(cord1[1]) + '\n'
    if(state == 1):
        message += 'GPS2: \n\tLAT: ' + str(cord2[0]) +' LON: ' + str(cord2[1]) + '\n'
        msg = str(cord1[0]+cord2[0]) + '/' + str(cord1[1]+cord2[1]) + '/' + message
    else:
        message += 'GPS Respuesto: \n\tLAT: ' + str(cordR[0]) +'LON: ' + str(cordR[1]) + '\n' +'ERROR EN GPS2\n'
        msg = str(cord1[0]+cordR[0]) + '/' + str(cord1[1]+cordR[1]) + '/' + message
    #print(message)
    sock.send(msg.encode())

def validador():
    plat = (cord2[0] - cord1[0])/cord1[0]
    plon = (cord2[1] - cord1[1])/cord1[1]
    if (plat > 0.5):
        state = 0
    elif (plon > 0.5):
        state = 0

# MAIN
while True:
    cord1[0] += mov[0]
    cord2[0] += mov[0]+inc[0]
    cordR[0] += mov[0]
    cord1[1] += mov[1]
    cord2[1] += mov[1]+inc[1]
    cordR[1] += mov[1]
    validador()
    sender()
    time.sleep(0.2)
    

# Cerrar coneccion
sock.close()