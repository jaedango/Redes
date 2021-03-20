# -*- coding: utf-8 -*-
import socket
print('Creando socket - Cliente')

# armamos el socket los parametros que recibe el socket indican el tipo de conexion
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# lo conectamos al puerto acordado
client_socket.connect(('localhost', 5000))

# mandamos un mensaje
print("Conectando ...")
send_message = 's'.encode()

# enviamos el mensaje a traves del socket
client_socket.send(send_message)
print("... Mensaje enviado")

# esperamos respuesta
message = client_socket.recvfrom(16)
print(' -> Respuesta del servidor: <<' + message[0].decode() + '>>')

# cerramos la conexion
client_socket.close()