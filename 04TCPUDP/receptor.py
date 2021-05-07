# -*- coding: utf-8 -*-
import socket

server_address = 'localhost'
server_port = 5000
buffsize = 64

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
    ## client mensaje 1
    # imprimimos el mensaje recibido
    mensaje1 = payload.decode()
    respsms = mensaje1[:3]
    try:
        respsms = int(respsms) + 1
        respsms = str(respsms)
    except:
        print("error")
    #respint = (int)respsms + 1
    print("Mensaje = <<" + mensaje1 + ">>")

    # ---------------------------------------------
    ## server response 1
    print("Echoing data back to " + str(client_address))
    sms2 = "200"
    response = respsms + sms2
    sent = server_socket.sendto(response.encode(), client_address)
    '''
    # ---------------------------------------------
    ## client mensaje 2
    payload, client_address = server_socket.recvfrom(buffsize)
    mensaje2 = payload.decode()
    respsms2 = (str)(((int)mensaje2[:3])+1)
    
    # ---------------------------------------------
    ## server response 2
    sent = server_socket.sendto(response.encode(),client_address)'''
