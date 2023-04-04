import socket
from game_logic import BlackJackGame

HOST = 'localhost'
PORT = 12345

game = BlackJackGame()

def handle_player_turn(conn, player_num, player_hand):
    action = conn.recv(1024).decode()
    print(f"Player {player_num} action: {action}")
    if action == 'hit':
        card = game.deal_card()
        player_hand.append(card)
        conn.sendall(str(card).encode())
    return action

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Bank: Waiting for players to connect...")

    conn1, addr1 = server_socket.accept()
    print(f"Bank: Player 1 connected from {addr1}")
    conn1.sendall("Player 1".encode())

    conn2, addr2 = server_socket.accept()
    print(f"Bank: Player 2 connected from {addr2}")
    conn2.sendall("Player 2".encode())

    player1_hand = [game.deal_card(), game.deal_card()]
    player2_hand = [game.deal_card(), game.deal_card()]

    conn1.sendall(str(player1_hand).encode())
    conn2.sendall(str(player2_hand).encode())

    while True:
        action1 = handle_player_turn(conn1, 1, player1_hand)
        action2 = handle_player_turn(conn2, 2, player2_hand)

        if action1 == 'stand' and action2 == 'stand':
            break

    player1_value = game.calculate_hand_value(player1_hand)
    player2_value = game.calculate_hand_value(player2_hand)

    if player1_value > 21:
        if player2_value > 21:
            result1 = "Both players busted. It's a draw."
            result2 = result1
        else:
            result1 = "You busted. You lost."
            result2 = "Player 1 busted. You won."
    elif player2_value > 21:
        result1 = "Player 2 busted. You won."
        result2 = "You busted. You lost."
    elif player1_value > player2_value:
        result1 = "You won."
        result2 = "You lost."
    elif player1_value < player2_value:
        result1 = "You lost."
        result2 = "You won."
    else:
        result1 = "It's a draw."
        result2 = result1

    conn1.sendall(result1.encode())
    conn2.sendall(result2.encode())

    conn1.close()
    conn2.close()
    print("Game finished.")


