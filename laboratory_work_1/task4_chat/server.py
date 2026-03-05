import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9004))
server.listen()

clients = []

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            for c in clients:
                if c != client:
                    c.send(msg)
        except:
            break

    if client in clients:
        clients.remove(client)
    client.close()

print("Chat server started on 127.0.0.1:9004")

while True:
    client, addr = server.accept()
    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
    thread.start()