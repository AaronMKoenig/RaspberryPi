import socket

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
        with open(OUTPUT_FILE, 'wb') as f:  # Datei im Binärmodus öffnen
            while True:
                data = conn.recv(4096)  # Daten empfangen
                if not data:  # Verbindung beendet
                    print("Verbindung geschlossen.")
                    break
                f.write(data)  # Daten in Datei schreiben
        print(f"Daten wurden in '{OUTPUT_FILE}' gespeichert.")
