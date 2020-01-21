from socket import *
from _thread import *
# Creating a clientsocket

# Variables
HOST = 'localhost'  # Direccion IP del servidor
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
    file = open('D:\PyChram\ProyectoDistribuidas\Data.txt','a')
    if(len(data) != 0):
        file.write(data)
    file.close()
    
# MAIN
while True:
    reciver()

# Cerrar coneccion
sock.close()
