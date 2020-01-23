from socket import *

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
    print (reply.decode())


# Comunicacion
while True:
    reciver()

# Cerrar coneccion
sock.close()
