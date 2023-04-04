import socket

HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Connected to the bank...")

    while True:
        # Kommunikation mit der Bank (Server)
        card = client_socket.recv(1024)
        if not card:
            break

        print(f"Received card: {card.decode()}")

        # Weitere Kommunikation und Spielaktionen können hier hinzugefügt werden.
