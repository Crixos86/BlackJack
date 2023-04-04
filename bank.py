import socket
from game_logic import BlackJackGame
#SERVER
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

    # Anfangsblatt an die Spieler verteilen
    hand1 = [game.deal_card(), game.deal_card()]
    hand2 = [game.deal_card(), game.deal_card()]

    conn1.sendall(str(hand1).encode())
    conn2.sendall(str(hand2).encode())

    # Annahme von Spielaktionen der Spieler (Hit or Stand)
    actions = [None, None]
    for i, conn in enumerate([conn1, conn2]):
        action = conn.recv(1024).decode()
        actions[i] = action
        print(f"Player {i + 1} action: {action}")

    # Spiellogik und Kommunikation zwischen Bank und Spielern
    for i, (action, conn, hand) in enumerate(zip(actions, [conn1, conn2], [hand1, hand2])):
        if action == 'Hit':
            hand.append(game.deal_card())
            conn.sendall(str(hand).encode())
        else:
            conn.sendall(b"Stand")

    # Ergebnisse berechnen und an Spieler senden
    hand_values = [game.calculate_hand_value(hand1), game.calculate_hand_value(hand2)]
    results = ['Draw' if hand_values[0] == hand_values[1] else 'Win' if hand_values[0] > hand_values[1] else 'Lose']
    results = [result if hand_value <= 21 else 'Bust' for result, hand_value in zip(results, hand_values)]

    for conn, result in zip([conn1, conn2], results):
        conn.sendall(result.encode())
