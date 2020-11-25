import socket
import struct
import sys
import threading
import time
import random
def Heartbeat(inicializado=False):
    while True:
        if inicializado is False:
            time.sleep(0.1)
        global id
        global listServers
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.2)
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        message = b'HEARTBEAT'
        multicast_group_servers = ('224.2.2.3', 8888)
        try:
            sent = sock.sendto(message, multicast_group_servers)
            listServers = []
            while True:
                try:
                    data, server = sock.recvfrom(1024)
                    listServers.append(int(data.decode("utf-8")))
                except socket.timeout:
                    if inicializado is True:        
                        i = 0
                        while i in listServers:
                            i += 1
                        id = i
                    break        
        finally:
            if inicializado is True:
                print("ID do servidor é {}".format(id))
                sock.close()
                break                
            sock.close()

def Server():
    global listServers
    multicast_group = '224.2.2.3'
    server_address = ('', 8888)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        mreq)
    print('Esperando receber mensagem') 
    while True:    
        if (listServers.count(id) > 1):
            print("Erro! Servidor com o mesmo id encontrado!")
            print("Gerando um id novo")
            time.sleep(random.randrange(0, 10, 2)*0.1)
            Heartbeat(True)
            print('Esperando receber mensagem')
        data, address = sock.recvfrom(1024)
        if(data.decode("utf-8") == "HEARTBEAT"):
            message = bytes(str(id),encoding="ascii")
            sock.sendto(message, address)
        else:
            print('Recebido a expressão {} de {}'.format(
                data.decode("utf-8"), address[0]))
            listServers.sort()
            if id == listServers[0]:
                try:
                    result = round(eval(data),2) 
                    print('Enviando o resultado {} para {}'.format(result, address[0]))
                except:
                    result = "Expressao Invalida"
                    print("Expressão Inválida recebida!")
                message = bytes(str(result), encoding="ascii") 
                sock.sendto(message, address)
Heartbeat(True)
threads = []
Serv = threading.Thread(target=Server)
Serv.start()
threads.append(Serv)
Verif = threading.Thread(target=Heartbeat)
Verif.start()
threads.append(Verif)
for thread in threads:
    thread.join()