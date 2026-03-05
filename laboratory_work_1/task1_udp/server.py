import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 9001))

print("UDP server started on 127.0.0.1:9001")

data, addr = server.recvfrom(1024)
print("Client said:", data.decode())

server.sendto("Hello, client".encode(), addr)
print("Sent: Hello, client")