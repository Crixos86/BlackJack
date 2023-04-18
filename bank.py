import socket
from game_logic import BlackJackGame
import tkinter as tk
import json

def main_bank_ui():
    def handle_player_turn(conn, player_num, player_hand):
        hand_value = game.calculate_hand_value(player_hand)
        if hand_value > 21:
            game_status.set(f"Player {player_num} is busted with a hand value of {hand_value}.")
            return 'stand'

        action = conn.recv(1024).decode()
        game_status.set(f"Player {player_num} action: {action}")
        if action == 'hit':
            card = game.deal_card()
            player_hand.append(card)
            print(f"Bank: Sending card to Player {player_num}: {card}")
            conn.sendall(json.dumps(card).encode())
        return action


    bank_window = tk.Tk()
    bank_window.title("Blackjack - Bank")

    game_status = tk.StringVar()
    game_status.set("Waiting for players to connect...")
    status_label = tk.Label(bank_window, textvariable=game_status)
    status_label.pack()

    

    HOST = 'localhost'
    PORT = 12345

    game = BlackJackGame()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        game_status.set("Bank: Waiting for players to connect...")

        conn1, addr1 = server_socket.accept()
        game_status.set(f"Player 1 connected from {addr1}")
        conn1.sendall("Player 1".encode())
        bank_window.update()
        conn2, addr2 = server_socket.accept()
        game_status.set(f"Player 2 connected from {addr2}")
        conn2.sendall("Player 2".encode())
        bank_window.update()
        print("Bank: Sending initial hands to players")
        player1_hand = [game.deal_card(), game.deal_card()]
        player2_hand = [game.deal_card(), game.deal_card()]

        print(f"Bank: Sending initial hand to Player 1: {player1_hand}")

        conn1.sendall(json.dumps(player1_hand).encode())
        
        print(f"Bank: Sending initial hand to Player 2: {player2_hand}")

        conn2.sendall(json.dumps(player2_hand).encode())
        
        while True:
            action1 = handle_player_turn(conn1, 1, player1_hand)
            action2 = handle_player_turn(conn2, 2, player2_hand)

            if action1 == 'stand' and action2 == 'stand':
                break
            bank_window.update()     
            if game.calculate_hand_value(player1_hand) > 21 and game.calculate_hand_value(player2_hand) > 21:
                break
            bank_window.update()        


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
        game_status.set("Game finished.")


    bank_window.mainloop()

if __name__ == "__main__":
    main_bank_ui()
