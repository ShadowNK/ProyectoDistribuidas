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
    print (repr(reply.decode()))


# Comunicacion
while True:
    start_new_thread(reciver,())

# Cerrar coneccion
sock.close()
