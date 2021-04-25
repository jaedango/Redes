import binascii
import socket

def split(word):
    return [char for char in word]

def parser(msg):
    arr = split(msg)
    # ---- header ----
    header = [""] * 12
    for i in range(24):
        if(i%2==0):
            header[i//2]=arr[i]
        else:
            header[i//2]+=arr[i]
    data = [""] * (len(arr) - 24)

    # Aca se puede agregar el header del request ...
    # 0-3   -> ID
    # 4-7   -> QR, OPcode, ...
    # 8-11  -> num consultas
    # 12-15 -> num respuestas
    # 16-19 -> authority records
    # 20-23 -> additional records

    # ---- response data question ----
    i = 24
    dominio=""
    
    while (arr[i] != '0' or arr[i+1] != '0'):
        num = int(arr[i]+arr[i+1],16)
        i+=2
        for j in range(num):
            dominio += chr(int(arr[i+j*2]+arr[i+j*2+1],16))
        dominio+= "."
        i+=num*2
    print("dominio: " + dominio)
    i+=2
    qtype = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3])
    i+=4
    qclass = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3])
    i+=4
    print("QTYPE = " + str(qtype))
    print("QCLASS = " + str(qclass))

    # agregar data answer
    print("Server Answer:")
    # agregar ciclo while aca para ver el resto de las ips
    '''while(i < len(arr)):
        i+=4 # name
        tipo = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3],16)
        i+=4 # type
        i+=4 # class
        i+=8 # TTL
        RdLENGTH = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3],16)
        i+=4 #RDlength
        if tipo == 1:
            # agregar el largo que falta

        i+=2*RdLENGTH
        #ciclo while ....
    '''


    i+=20 # aca nos saltamos toda la info entre
    RdLENGTH = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3],16)
    i+=4
    ip = ""
    for j in range(RdLENGTH):
        ip += str(int(arr[i+2*j]+arr[i+2*j+1],16))
        ip +="."
    print("ip = " + ip)

def tohex(dir):
    arr = dir.split(".")
    dir2 = ""
    for num in range(len(arr)-1):
        val = len(arr[num])
        val2 = hex(val)
        val2 = val2.strip("0x")
        if len(str(val2)) < 2:
            dir2+="0"
        dir2+=val2
        for j in range(len(arr[num])):
            val3 = hex(ord(arr[num][j]))
            val3 = val3[2:]
            dir2+=val3
    dir2+="00"

    dir2+="0001" # QTYPE
    dir2+="0001" # QCLASS
    return dir2    
        

# ---- comienzo del dns ----
def send_dns_message(dir):
    #address = "192.33.4.12"
    #port = 5353
    
    # Encabezado con ID 0 (00 00 en hexadecimal), preguntamos por example.com
    header = "00 00 00 00 00 01 00 00 00 00 00 00 ".replace(" ","")
    #data = "07 65 78 61 6D 70 6C 65 03 63 6F 6D 00 00 01 00 01".replace(" ","")
    data = tohex(dir).upper()
    message = header + data
    # Lo escribimos así para que se entendiera, lo concatenamos para hacer la cadena de hexadecimales
    server_address = ("192.33.4.12", 53)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("a")
    try:
        print("b")
        # usamos binascii para pasar el mensaje al formato apropiado
        binascii_msg = binascii.unhexlify(message)
        # y lo enviamos
        sock.sendto(binascii_msg, server_address)
        # En data quedará la respuesta a nuestra consulta
        data, _ = sock.recvfrom(4096)
        print("c")
    finally:
        sock.close()
    # Ojo que los datos de la respuesta van en hexadecimal, no en binario
    print("hola")
    msg = binascii.hexlify(data).decode("utf-8")
    parser(msg)
    return msg

print(send_dns_message("cl."))



#tohex("example.com.")

# root: 192.33.4.12
# subred: 192.5.6.30

    

#parser("000080800001000100000000076578616d706c6503636f6d0000010001c00c000100010000493200045db8d822")
    
        
