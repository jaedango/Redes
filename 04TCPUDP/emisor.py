# -*- coding: utf-8 -*-
import socket
import time
print('Creando socket - Cliente')

# armamos el socket los parametros que recibe el socket indican el tipo de conexion
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# lo conectamos al puerto acordado
client_socket.connect(('localhost', 5000))

# ---------------------------------------------
## client mensaje 1
# header : port1 port2 seq(16bit)        expected ans      header length reserved
# header : 5000  5000  00000000000000001 00000000000000002 00001         000000
send_mensaje = "100"

# mandamos un mensaje
print("Conectando ...")
send_message += input()
send_message = send_message.encode()

# enviamos el mensaje a traves del socket
client_socket.send(send_message)
print("... Mensaje enviado")

# esperamos respuesta
message = client_socket.recvfrom(64)
print(' -> Respuesta del servidor: <<' + message[0].decode() + '>>')

# ---------------------------------------------
## server response 1

# ---------------------------------------------
## client mensaje 2

# ---------------------------------------------
## server response 2


# cerramos la conexion
client_socket.close()