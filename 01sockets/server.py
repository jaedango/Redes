# -*- coding: utf-8 -*-
import socket

server_address = 'localhost'
server_port = 5000
buffsize = 16

address = (server_address, server_port)

print('Creando socket - Servidor')
# Socket no orientado a conexion
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(address)

print("Listening on " + server_address + " : " + str(server_port))

while True:
    # recibir mensajes. Este metodo nos entrega el mensaje
    # junto a la direccion de origen del mensaje
    payload, client_address = server_socket.recvfrom(buffsize)

    # imprimimos el mensaje recibido
    print("Mensaje = <<" + payload.decode() + ">>")

    print("Echoing data back to " + str(client_address))

    sent = server_socket.sendto(payload, client_address)