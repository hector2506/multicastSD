import socket
import struct
import sys

multicast_group = '224.2.2.3'
server_address = ('', 8888)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
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
    print(data.decode("utf-8"))     #Recebe o dado em bytes e converte para string
    result = round(eval(data),3) #Recebe o resultado da expressão armazenada na string e arrendonda para 3 casas decimais
    print(f"O resultado da expressão é {result}\n" )
    print(f'Enviando o resultado {result} para {address}')
    message = bytes(str(result), encoding="ascii") 
    sock.sendto(message, address)

    break
