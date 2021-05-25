# -*- coding: utf-8 -*-
import socket
import time

server_address = 'localhost'
server_port = 5000
buffsize = 64
timeout = 1

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

    # ---------------------------------------------
    # ## client message 
    # ## imprimimos el mensaje recibido
    mensaje1 = payload.decode()
    msg1a = mensaje1[:3]    # 1s 3 char     -> mensaje de verificacion (SYN)
    msg1b = mensaje1[3:]    # resto de char -> contenido del mensaje
    try:
        resp1 = str(int(msg1a) + 1)
    except:
        print("error\n")
        break
    print("Mensaje 1 = <<" + msg1b + ">>")

    # ---------------------------------------------
    # ## server response 
    print("Echoing data back to " + str(client_address))
    resp1a = "200"          # nuevo mensaje de verificacion (ACK)
    resp1b = resp1          # verificacion del mensaje anterior (SYN+1)
    resp1c = msg1b          # contenido del mensaje
    resp = resp1a + resp1b + resp1c
    sent = server_socket.sendto(resp.encode(),client_address)

    # ---------------------------------------------
    # ## client response 
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            payload, client_address = server_socket.recvfrom(buffsize)
            mensaje2 = payload.decode()
            msg2a = mensaje2[:3]    # respuesta de la verificacion anterior (ACK+1)
            msg2b = mensaje1[3:]    # contenido del mensaje
            if msg2a == str(int(resp1a) + 1):
                print("Coneccion establecida correctamente")
                print("Mensaje 2 = <<" + msg2b + ">>")
                break
            else:
                print("Hubo problemas en la coneccion")
                break
        except:
            print('There was an error, try again.')

