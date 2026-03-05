import socket
import math

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9002))
server.listen(1)

print("TCP server started on 127.0.0.1:9002")
print("Waiting for client...")

conn, addr = server.accept()
print("Client connected:", addr)

data = conn.recv(1024).decode().strip()   # ожидаем "a b"
a_str, b_str = data.split()

a = float(a_str)
b = float(b_str)

c = math.sqrt(a * a + b * b)

conn.send(str(c).encode())
conn.close()
server.close()