# -*- coding: utf-8 -*-
import socket
import time
server_address = 'localhost'
server_port = 5000
buffsize = 64
address = (server_address, server_port)
print('Crando socket - Cliente')

# armamos el socket
# los parametros que recibe el socket indican el tipo de coneccion
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# lo conectamos al port acordado
client_socket.connect(address)

# ---------------------------------------------
# ## client message 1

# ## mandamos el mensaje
print("Conectando ...")
msg1a = "100"
msg1b = input("Inserte su mensaje: ")
msg = msg1a + msg1b
msg = msg.encode()

# ## enviamos el mensaje a traves del socket
client_socket.send(msg)
print("... Mensaje enviado")
time.sleep(1)

# ---------------------------------------------
