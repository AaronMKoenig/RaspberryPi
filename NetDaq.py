import socket
import time

HOST = '192.168.2.190'  # Server-IP
PORT = 12345

block_size = 10 * 1024 * 1024  # 10 MB
total_size = 1 * 1024 * 1024 * 1024  # 1 GB
blocks = total_size // block_size

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Verbunden zum Server")
    msg = b'X' * block_size
    start = time.time()
    for i in range(blocks):
        s.sendall(msg)
        print(f"Block {i+1}/{blocks} gesendet")
    end = time.time()
    duration = end - start
    print(f"Gesamtzeit: {duration:.2f} Sekunden")
    print(f"Durchsatz: {total_size * 8 / duration / 1_000_000:.2f} Mbit/s")
