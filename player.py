import socket
#CLIENT
def display_hand(hand):
    return ', '.join([f"{card['rank']} of {card['suit']}" for card in hand])

def get_player_action():
    while True:
        action = input("Enter 'hit' or 'stand': ")
        if action.lower() in ['hit', 'stand']:
            return action.lower()
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")

HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Connected to the bank...")

    player_num = client_socket.recv(1024).decode()
    print(f"You are {player_num}")

    hand = eval(client_socket.recv(1024).decode())
    print(f"Your initial hand: {display_hand(hand)}")

    while True:
        action = get_player_action()
        client_socket.sendall(action.encode())

        if action == 'hit':
            card = eval(client_socket.recv(1024).decode())
            hand.append(card)
            print(f"Received card: {display_hand([card])}")
            print(f"Your updated hand: {display_hand(hand)}")
        else:
            break

    print("Waiting for the game result...")

    result = client_socket.recv(1024).decode()
    print(f"Game result: {result}")

