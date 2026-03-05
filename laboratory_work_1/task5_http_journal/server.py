import socket
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 9005

grades = []  # [{"discipline": "...", "grade": "..."}]


def make_page():
    items = ""
    for g in grades:
        items += f"<li>{g['discipline']}: <b>{g['grade']}</b></li>"

    return f"""<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>Grades</title></head>
<body>
  <h1>Оценки по дисциплинам</h1>
  <ul>{items}</ul>

  <h2>Добавить оценку</h2>
  <form method="POST" action="/add">
    Дисциплина: <input name="discipline"><br><br>
    Оценка: <input name="grade"><br><br>
    <button type="submit">Сохранить</button>
  </form>
</body>
</html>"""


def get_content_length(headers_text: str) -> int:
    for line in headers_text.split("\r\n"):
        if line.lower().startswith("content-length:"):
            return int(line.split(":", 1)[1].strip())
    return 0


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Open in browser: http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    # 1) Читаем хотя бы заголовки
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk

    if not data:
        conn.close()
        continue

    header_bytes, body_bytes = data.split(b"\r\n\r\n", 1)
    headers_text = header_bytes.decode("utf-8", errors="ignore")

    # 2) Разбираем первую строку: METHOD PATH HTTP/...
    first_line = headers_text.split("\r\n")[0]
    method, path, _ = first_line.split(" ")

    # 3) Если POST — дочитываем тело по Content-Length
    content_length = get_content_length(headers_text)
    while len(body_bytes) < content_length:
        body_bytes += conn.recv(4096)

    body = body_bytes.decode("utf-8", errors="ignore")

    print(method, path)

    if method == "GET" and path == "/":
        html = make_page().encode("utf-8")
        resp = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8") + html
        conn.sendall(resp)

    elif method == "POST" and path == "/add":
        form = parse_qs(body)
        discipline = form.get("discipline", [""])[0].strip()
        grade = form.get("grade", [""])[0].strip()

        print("Parsed:", discipline, grade)

        if discipline and grade:
            grades.append({"discipline": discipline, "grade": grade})

        # redirect to /
        resp = (
            "HTTP/1.1 302 Found\r\n"
            "Location: /\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8")
        conn.sendall(resp)

    else:
        txt = "Not Found".encode("utf-8")
        resp = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            f"Content-Length: {len(txt)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8") + txt
        conn.sendall(resp)

    conn.close()