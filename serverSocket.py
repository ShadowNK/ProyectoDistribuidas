from socket import *
from _thread import *
from decimal import Decimal
import datetime

HOST = '172.31.108.23'  # Direccion IP del seridor
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
            #print('pr: ' + str(data[0]))
            resend_to_BD(aux[1].encode())

    clientsocket.close()


## Devices GPS

def on_new_gps(clientsocket,addr):
    global data, GPSCon
    print ("Conectado con GPS: ", addr)
    while True:
        msg = clientsocket.recv(1024)
        if send == 1:
            aux = msg.decode().split('/')
            data[1] += Decimal(aux[0])
            data[2] += Decimal(aux[1])
            GPSCon += 2
            #print('pr: ' + str(data[1]) + 'pr: ' + str(data[2]))
            resend_to_BD(aux[2].encode())
    clientsocket.close()


## DB device

def on_new_BD(clientsocket,addr):
    print ("Conectado con BD: ", addr)
    global bd, send
    bd = (clientsocket, addr)

def resend_to_BD(ms):
    (clientsocket,addr) = bd
    #print(ms.decode())
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
    global data, AltCon, GPSCon
    if(AltCon >= 40 | GPSCon >= 20):
        al = data[0]/AltCon
        la = data[1]/GPSCon
        lo = data[2]/GPSCon
        resend_to_p(al, la, lo)
        data = [0, 0, 0]
        AltCon = 0
        GPSCon = 0

def resend_to_p(al, la, lo):
    (clientsocket,addr) = pilot
    msg = 'ALTURA: ' + str(al) + '\nGPS: Lat: ' + str(la) + ' Lon: ' + str(lo)
    print(msg)
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
