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
    i+=20 # aca nos saltamos toda la info entre
    RdLENGTH = int(arr[i]+arr[i+1]+arr[i+2]+arr[i+3],16)
    i+=4
    ip = ""
    for j in range(RdLENGTH):
        ip += str(int(arr[i+2*j]+arr[i+2*j+1],16))
        ip +="."
    print("ip = " + ip)

    

parser("000080800001000100000000076578616d706c6503636f6d0000010001c00c000100010000493200045db8d822")
    
        