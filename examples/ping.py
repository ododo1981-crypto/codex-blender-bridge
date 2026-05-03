import json
import socket


HOST = "127.0.0.1"
PORT = 9877


def call(command_type, params=None):
    payload = json.dumps({"type": command_type, "params": params or {}}).encode("utf-8")
    chunks = []
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        sock.settimeout(30)
        sock.sendall(payload)
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
    return json.loads(b"".join(chunks).decode("utf-8"))


if __name__ == "__main__":
    print(json.dumps(call("ping"), indent=2))
