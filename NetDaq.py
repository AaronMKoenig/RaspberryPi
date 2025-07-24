import socket
import time

HOST = '192.168.2.190'  # IP-Adresse des Servers (Kali Laptop)
PORT = 12345       #  Port 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Verbindung zum Server aufbauen
    print("Verbunden zum Server")
    for i in range(100):
        msg = b'X' * 1024 * 1024  # 1 MB Daten in Bytes
        s.sendall(msg)             # Sende die Daten komplett an den Server
        print(f"Gesendet: {len(msg)} Bytes")
        time.sleep(0.01)            # Kurze Pause zwischen den Sendungen 
