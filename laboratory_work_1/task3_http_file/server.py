import socket

HOST = "127.0.0.1"
PORT = 9003

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Open in browser: http://{HOST}:{PORT}")

conn, addr = server.accept()
_ = conn.recv(1024)  # принимаем запрос (не разбираем)

with open("index.html", "r", encoding="utf-8") as f:
    html_text = f.read()

body = html_text.encode("utf-8")

headers = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    f"Content-Length: {len(body)}\r\n"
    "Connection: close\r\n"
    "\r\n"
).encode("utf-8")

conn.sendall(headers + body)
conn.close()
server.close()