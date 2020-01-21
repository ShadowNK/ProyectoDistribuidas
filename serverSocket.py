from socket import *
from _thread import *
from decimal import Decimal
import datetime

HOST = 'localhost'  # Direccion IP del seridor
PORT = 50010
bd = (socket(),'')
pilot = (socket(),'')
send = 0
data = [0, 0, 0]
AltCon = 0
GPSCon = 0

# VARIABLES ALT
server = (HOST, PORT)

# SOCKET ALT
sock = socket()                 # Create a socket object
sock.bind(server)               # Bind to the port
sock.listen(5)                  # Number of connections


## Devices Altitud

def on_new_alt(clientsocket,addr):
    global data, AltCon
    print ("Conectado con ALT: ", addr)
    while True:
        msg = clientsocket.recv(1024)
        if send == 1:
            aux = msg.decode().split('/')
            data[0] += Decimal(aux[0])
            AltCon += 2
            resend_to_BD(aux[1].encode())

    clientsocket.close()


## Devices GPS

def on_new_gps(clientsocket,addr):
    print ("Conectado con GPS: ", addr)
    while True:
        msg = clientsocket.recv(1024)
        if send == 1:
            aux = msg.decode().split('/')
            data[1] += Decimal(aux[0])
            data[2] += Decimal(aux[1])
            GPSCon += 2
            resend_to_BD(aux[2].encode())
    clientsocket.close()


## DB device

def on_new_BD(clientsocket,addr):
    print ("Conectado con BD: ", addr)
    global bd, send
    bd = (clientsocket, addr)

def resend_to_BD(ms):
    (clientsocket,addr) = bd
    print(ms.decode())
    clientsocket.send(ms)


## PILOT device
            
def on_new_p(clientsocket,addr):
    print ("Conectado con Pilot: ", addr)
    global pilot, send
    pilot = (clientsocket,addr)
    send = 1
    while True:
        pilot_calc()

def pilot_calc():
    time = datetime.datetime.now()
    timeaux = 1
    aux = time[5]%10
    if(time[5]%2 == 0 & timeaux != aux):
        timeaux = aux
        resend_to_p()
        data = [0, 0, 0]

def resend_to_p():
    (clientsocket,addr) = pilot
    msg = 'ALTURA: ' + (data[0]/AltCon) + '\nGPS: Lat: ' + (data[1]/GPSCon) + ' Lon: ' + (data[2]/GPSCon)
    clientsocket.send(msg.encode())



input("Conectar el altimetro...")
conn, addr = sock.accept()
start_new_thread(on_new_alt,(conn,addr))

input("Conectar el gps...")
conn, addr = sock.accept()
start_new_thread(on_new_gps,(conn,addr))

input("Conectar la bd...")
conn, addr = sock.accept()
start_new_thread(on_new_BD,(conn,addr))

input("Conectar el piloto...")
conn, addr = sock.accept()
start_new_thread(on_new_p,(conn,addr))


input("press enter to finish")

sock.close()