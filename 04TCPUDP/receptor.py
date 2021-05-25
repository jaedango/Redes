# -*- coding: utf-8 -*-
from os import access
import socket

# ---------------------------------------------
def toDecode(message):
    msg = message.decode()
    list = msg.split(".")
    return list[0], list[1], list[2]

# ---------------------------------------------
def toEncode(ACK, SYN, msg):
    ACK1 = checkOne(ACK)
    resp = "{}.{}.{}".format(ACK1, SYN, msg)
    return resp.encode()

# ---------------------------------------------
def checkOne(msg):
    try:
        msg1 = int(msg) + 1
    except:
        msg1 = ""
    return msg1

# ---------------------------------------------
def tripleHandShakeServer():
    payload, client_address = server_socket.recvfrom(buffsize)

    # ---------------------------------------------
    # ## Client Message
    ACK, SYN, msg = toDecode(payload)
    print("Mensaje recibido : <<{}>>", format(msg))

    # ---------------------------------------------
    # ## Server Response
    SYN = "200"
    Server_Resp = toEncode(ACK, SYN, msg)
    sent = server_socket.sendto(Server_Resp, client_address)

    # ---------------------------------------------
    # ## Client Response
    while True:
        server_socket.settimeout(timeout)
        try:
            payload, client_address = server_socket.recvfrom(buffsize)
            ACK, SYN1, msg = toDecode(payload)
            if SYN1 == checkOne(SYN):
                print("Coneccion establecida correctamente.")
                break
            else:
                print("Ocurrio un transmitiendo el mensaje")
                break

        except socket.timeout:
            print("No se recibio mensaje alguno")
            server_socket.settimeout(None)
            break

    



# ---------------------------------------------
# ---------------------------------------------
# ## direccion
server_address = 'localhost'
server_port = 5000
buffsize = 64
timeout = 1

address = (server_address, server_port)

# ---------------------------------------------
# Creando servidor
print('Crando Socket - Servidor')
# Socket no orientado a conexion
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(address)
listening = "Listening on {} : {}".format(server_address, server_port)
print(listening)
while True:
    tripleHandShakeServer()