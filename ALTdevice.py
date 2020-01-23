from socket import *
import random
import time

# Creating a ALT devices

# Variables
HOST = '172.31.108.23'  # Direccion IP del servidor
PORT = 50010
server = (HOST, PORT)

alt1 = 1
alt2 = 1
altR = 1
inc = 0
mov = 0

alt1 = random.random() * 32000
alt2 = alt1
altR = alt1
inc = alt1*0.03
mov = alt1*0.05

state = 1

# Crear el socket
sock = socket(AF_INET, SOCK_STREAM)

# Establecer coneccion
sock.connect(server)

def sender():
    message = 'ALT1: ' + str(alt1) + '\n'
    if(state == 1):
        message += 'ALT2: ' + str(alt2) + '\n'
        msg = str(alt1+alt2) + '/' + message
    else:
        message += 'ALT Respuesto: ' + str(altR) + '\n' +'ERROR EN ALT2\n'
        msg = str(alt1+altR) + '/' + message
    #print(message)
    sock.send(msg.encode())

def validador():
    palt = (alt2 - alt1)/alt1
    if (palt > 0.05):
        state = 0

# MAIN
while True:
    alt1 += mov
    alt2 += mov+inc
    altR += mov
    validador()
    sender()
    time.sleep(0.1)
    

# Cerrar coneccion
sock.close()
