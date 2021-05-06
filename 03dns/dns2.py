import binascii
import socket

def split(word):
    return [char for char in word]

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

def parser(msg):
    arr = split(msg)
    # ---- header ----
    header = [""] * 12
    for i in range(24):
        if(i%2==0):
            header[i//2]=arr[i]
        else:
            header[i//2]+=arr[i]
    # data = [""] * (len(arr)-24)
    
    # Aca se puede agregar el header del request ...
    # 0-3   -> ID
    # 4-7   -> QR, OPcode, ...
    # 8-11  -> num consultas
    # 12-15 -> num respuestas
    # 16-19 -> authority records
    # 20-23 -> additional records

    i = 24 # header
    dominio = ""
    while (arr[i] != '0' or arr[i+1] != '0'):
        num = int(arr[i]+arr[i+1],16)
        i+=2
        for j in range(num):
            dominio += chr(int(arr[i+j*2]+arr[i+j*2+1],16))
        dominio+= "."
        i+=num*2
    print("dominio: " + dominio)
    i+=2 # 00
    qtype = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3])
    i+=4 # qtype
    qclass = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3])
    i+=4 # qclass
    #print("QTYPE = " + str(qtype))
    #print("QCLASS = " + str(qclass))

    # agregar data answer
    print("Server Answer:")
    arr2 = [] # aca vamos a guardar las ips
    # agregar ciclo while aca para ver el resto de las ips
    while(i < len(arr)):
        i+=4 # name
        tipo = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3],16)
        i+=4 # type
        i+=4 # class
        i+=8 # TTL
        RdLENGTH = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3],16)
        i+=4 #RDlength
        if tipo == 1:
            ip = ""
            for val in range(RdLENGTH):
                ip += str(int(arr[i+2*val]+arr[i+2*val+1],16))
                ip+="."
            arr2.append(ip)
            #print(ip)
        #else:
        #    print("----")
        i+=2*RdLENGTH
        #print("----------------")
    return arr2

# ---- dns ----
def send_dns_message(dir, ip):
    address = ip
    port = 53
    # Encabezado con ID 0 (00 00 en hexadecimal)
    header = "00 00 00 00 00 01 00 00 00 00 00 00 ".replace(" ","")
    data = tohex(dir).upper()
    message = header + data
    server_address = (address, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # usamos binascii para pasar el mensaje al formato apropiado
        binascii_msg = binascii.unhexlify(message)
        # y lo enviamos
        sock.sendto(binascii_msg, server_address)
        # En data quedara la respuesta a nuestra consulta
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    msg = binascii.hexlify(data).decode("utf-8")
    arr = parser(msg)
    return arr

def dns(dir):
    arr = dir.split(".")
    arr2 = send_dns_message(arr[-2]+".","192.33.4.12")
    #print(arr2)
    #i = len(arr) -2
    arr4 = []
    for i in range(len(arr)-2):
        arr3 = arr[(len(arr)-3)-i:-1]
        #print(arr3)
        dir2 = ""
        for j in range(len(arr3)):
            dir2 += arr3[j]
            dir2 += "."
        for k in range(len(arr2)):
            arr4.append(send_dns_message(dir2,arr2[k][:-1]))
        #print("arrs:")
        #print(arr2)
        print(arr4)
        print("-------------------------")
        arr2 = arr4[0]
        arr4 = []
        

    '''
    while i >= 0:
        arr3 = arr[i:-1]
        dir2 = ""
        for j in range(len(arr3)):
            dir2 += arr3[j]
            dir2 += "."
        print("dominio: " + dir2)
        for k in range(len(arr2)):
            print(dir2 + " " + arr2[k][:-1])
            arr4.append(send_dns_message(dir2, arr2[k][:-1]))
        i -= 1'''

dns("eol.uchile.cl.")
#print(send_dns_message("eol.uchile.cl.","146.83.63.70"))