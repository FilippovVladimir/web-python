import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9004))

def receive():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break

thread = threading.Thread(target=receive, daemon=True)
thread.start()

while True:
    text = input()
    client.send(text.encode())