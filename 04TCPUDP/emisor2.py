# -*- coding: utf-8 -*-
import socket
import time
server_address = 'localhost'
server_port = 5000
buffsize = 64
timeout = 2
address = (server_address, server_port)
print('Crando socket - Cliente')

# armamos el socket
# los parametros que recibe el socket indican el tipo de coneccion
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# lo conectamos al port acordado
client_socket.connect(address)

# ---------------------------------------------
# ## client message 1
val = True
while val:
    # ## mandamos el mensaje
    print("Conectando ...")
    msg1a = "100" # (SYN)
    msg1b = input("Inserte su mensaje: ")
    msg = msg1a + msg1b
    msg = msg.encode()

    # ## enviamos el mensaje a traves del socket
    client_socket.send(msg)
    print("... Mensaje enviado")

    # ---------------------------------------------
    # ## server response 1
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            message = client_socket.recvfrom(buffsize)
            resp1 = message[0].decode()
            print(' -> Respuesta del servidor: <<' + resp1 + '>>')
            val = False
            resp1a = resp1[:3]  # (ACK)
            resp1b = resp1[3:6] # (SYN+1)
            resp1c = resp1[6:]
            if (resp1b != str(int(msg1a) + 1)):
                print("Error en la coneccion")
                val = True
            else:
                print("Respuesta del servidor: <<" + resp1c + ">>")
                
            # ---------------------------------------------
            # ## client response
            try:
                resp2a = str(int(resp1a) + 1)
            except:
                print('Recibido mensaje incorrecto')
            resp2 = resp2a + resp1c
            resp2 = resp2.encode()
            client_socket.send(resp2)
            print("Coneccion finalizada :)")
            break


        except:
            val = True