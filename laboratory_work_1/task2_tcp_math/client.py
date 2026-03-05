import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9002))

a = input("Enter a: ")
b = input("Enter b: ")

client.send((a + " " + b).encode())

result = client.recv(1024).decode()
print("Hypotenuse c =", result)

client.close()