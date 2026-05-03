import json
import socket


HOST = "127.0.0.1"
PORT = 9877


payload = json.dumps({"type": "get_scene_info", "params": {}}).encode("utf-8")
chunks = []

with socket.create_connection((HOST, PORT), timeout=10) as sock:
    sock.settimeout(30)
    sock.sendall(payload)
    while True:
        chunk = sock.recv(65536)
        if not chunk:
            break
        chunks.append(chunk)

print(json.dumps(json.loads(b"".join(chunks).decode("utf-8")), indent=2))
