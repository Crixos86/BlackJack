import socket
from game_logic import BlackJackGame

HOST = 'localhost'
PORT = 12345

game = BlackJackGame()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Bank: Waiting for players to connect...")

    conn1, addr1 = server_socket.accept()
    print(f"Bank: Player 1 connected from {addr1}")

    conn2, addr2 = server_socket.accept()
    print(f"Bank: Player 2 connected from {addr2}")

    # Spiellogik und Kommunikation zwischen Bank und Spielern
    while True:
        # Beispiel: Senden einer Karte an jeden Spieler
        card1 = game.deal_card()
        card2 = game.deal_card()

        conn1.sendall(str(card1).encode())
        conn2.sendall(str(card2).encode())

        # Kommunikation mit den Spielern und Spiellogik fortsetzen...
        # Hier können Sie den Spielablauf entsprechend der BlackJack-Regeln implementieren.

