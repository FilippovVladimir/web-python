import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("Hello, server".encode(), ("127.0.0.1", 9001))
print("Sent: Hello, server")

data, _ = client.recvfrom(1024)
print("Server said:", data.decode())