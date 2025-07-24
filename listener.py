import socket
import time

HOST = '0.0.0.0'  # Lauscht auf allen Netzwerk-Interfaces
PORT = 12345      # Port, auf dem der Server hören soll
OUTPUT_FILE = 'empfangene_daten.txt'  # Datei zum Speichern der Daten

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server läuft und hört auf Port {PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"Verbindung von {addr} akzeptiert.")
        received = 0
        start = time.time()
        with open(OUTPUT_FILE, 'wb') as f:  # Datei im Binärmodus öffnen
            while True:
                data = conn.recv(1024*1024)  # 1 MB Buffer
                if not data:  # Verbindung beendet
                    print("Verbindung geschlossen.")
                    break
                f.write(data)  # Daten in Datei schreiben
                received += len(data)
        end = time.time()
        print(f"Daten wurden in '{OUTPUT_FILE}' gespeichert.")
        print(f"Empfangen: {received / 1024 / 1024:.2f} MB in {end-start:.2f} Sekunden")
        print(f"Durchsatz: {received * 8 / (end-start):.2f} bit/s")
        print(f"Durchsatz: {received * 8 / (end-start) / 1_000_000:.2f} Mbit/s")
