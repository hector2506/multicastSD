import socket
import struct
import sys


# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Heartbeat
##############################################################################
sock.settimeout(0.2)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


message = b'HEARTBEAT'
multicast_group_servers = ('224.2.2.3', 8888)
try:
    #print("Enviando HEARTBEAT")
    sent = sock.sendto(message, multicast_group_servers)
    # Look for responses from all recipients
    listServers = []
    cont = 0
    
    while True:
        #print('Encontrando servidores')
        try:
            data, server = sock.recvfrom(1024)
            #print("Servidor Encontrado!")
            cont+=1
            listServers.append(int(data.decode("utf-8")))
        except socket.timeout:
            data, server = None, None
            if cont is 0:
                #print('Nenhum servidor ligado!')
                id = 0
            else:
                #print("Mais nenhum servidor foi encontrado!")
                #if cont is not 0:        
                #print("ID dos servidores encontrados = {}".format(listServers))
                i = 0
                while i in listServers:
                    i += 1
                id = i
            listServers.append(id)
            break
        else:
            print('received {!r} from {}'.format(
                data, server))
finally:
    print("ID do servidor é {}".format(id))
    sock.close()
#############################################################################


# Bind to the server address
multicast_group = '224.2.2.3'
server_address = ('', 8888)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

# Receive/respond loop
while True:
    print('waiting to receive message')
    data, address = sock.recvfrom(1024)

    print('received {} bytes from {}'.format(
        len(data), address))
    #print(data)
    if(data.decode("utf-8") == "HEARTBEAT"):
        message = bytes(str(id),encoding="ascii")
        sock.sendto(message, address)
    else:
        listServers.sort()
        #print(listServers)
        if id == listServers[0]:
            try:
                result = round(eval(data),3) 
                #print("O resultado da expressão é {}\n".format(result))
                print('Enviando o resultado {} para {}'.format(result, address))
            except:
                result = "Expressao Invalida"
                print("Expressão Inválida recebida!")
            message = bytes(str(result), encoding="ascii") 
            sock.sendto(message, address)
