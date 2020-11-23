import socket
import struct
import sys

eq = ''
while eq is '':
    eq = input("Insira uma expressão: ")
    if eq is '':
        print("Expressão vazia inserida")
message = bytes(eq, encoding="ascii")    
multicast_group = ('224.2.2.3', 8888)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.2)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
try:
    sent = sock.sendto(message, multicast_group)
    while True:
        print('Esperando para receber a resposta do servidor')
        try:
            data, server = sock.recvfrom(1024)
        except socket.timeout:
            print('Nenhuma resposta recebida')
            break
        else:
            print('Resultado da expressão: {}'.format(
                data.decode("utf-8")))
            break
finally:
    print('Encerrando a operação')
    sock.close()