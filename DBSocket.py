from socket import *
from _thread import *
# Creating a clientsocket

# Variables
HOST = '172.31.108.23'  # Direccion IP del servidor
PORT = 50010
server = (HOST, PORT)

# Crear el socket
sock = socket(AF_INET, SOCK_STREAM)

# Establecer coneccion
sock.connect(server)

def reciver():
    reply = sock.recv(1024)
    print(reply.decode())
    writter(reply.decode())

def writter(data):
    file = open('C:/Users/USRBET/Desktop/ProyectoDistribuidas-master/Data.txt','a')
    if(len(data) != 0):
        file.write(data)
    file.close()
    
# MAIN
while True:
    reciver()

# Cerrar coneccion
sock.close()
