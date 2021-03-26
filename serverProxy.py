# -*- coding: utf-8 -*-

"""
    Implements a simple HTTP/1.0 Server
"""


import socket
import json

# abrimos el archivo
with open("config.json") as file:
    #usamos json para manejar los datos
    data = json.load(file)
    

def receive_full_mesage(connection_socket, buff_size):
    # esta función se encarga de recibir el mensaje completo desde el cliente
    # en caso de que el mensaje sea más grande que el tamaño del buffer 'buff_size', esta función va esperar a que
    # llegue el resto

    # recibimos la primera parte del mensaje
    buffer = connection_socket.recv(buff_size)
    full_message = buffer
    # entramos a un while para recibir el resto y seguimos esperando información mientras el buffer llegue "lleno"
    while len(buffer) >= buff_size:
        # recibimos un nuevo trozo del mensaje
        buffer = connection_socket.recv(buff_size)
        # y lo añadimos al mensaje "completo"
        full_message += buffer
    # si recibimos un buffer que no está lleno, entonces llegamos al final del mensaje y salimos del while
    return full_message


# definimos el tamaño del buffer de recepción ¿Cómo se ven los trozos de mensaje recibidos si usamos 'buff_size = 2' ?
buff_size = 1024
address = ('localhost', 8888)

print('Creando socket - Servidor')
# armamos el socket
# los parámetros que recibe el socket indican el tipo de conexión
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# lo conectamos al server, en este caso espera mensajes localmente en el puerto 8888
server_socket.bind(address)

# hacemos que sea un server socket y le decimos que tenga a lo mas 3 peticiones de conexión encoladas
# si recibiera una 4ta petición de conexión la va a rechazar
server_socket.listen(3)

# nos quedamos esperando, como buen server, a que llegue una petición de conexión
print('... Esperando clientes')
while True:
    # abrimos el archivo
    with open("config.json") as file:
    #usamos json para manejar los datos
        data = json.load(file)

    # cuando llega una petición de conexión la aceptamos
    # y sacamos los datos de la conexión entrante (objeto, dirección)
    connection, address = server_socket.accept()

    # luego recibimos el mensaje usando la función que programamos
    #received_message = receive_full_mesage(connection, buff_size)

    #print(' -> Se ha recibido el siguiente mensaje: ' + received_message.decode())

    # respondemos
    request = connection.recv(1024).decode()
    print(request)

    # Send HTTP response
    headers = 'HTTP/1.0 200 OK\r\nServer:Javier Andrews\r\n\r\n'
    body = '''<html>
<head>
<title>hola</title> 
</head> 
<body>
    <h1> Hello World!</h1>
    <input type="text">
<body>
</html>'''

    response = headers+body
    connection.sendall(response.encode())

    # cerramos la conexión
    # notar que la dirección que se imprime indica un número de puerto distinto al 8888
    connection.close()
    print("conexión con " + str(address) + " ha sido cerrada")

    # seguimos esperando por si llegan otras conexiones