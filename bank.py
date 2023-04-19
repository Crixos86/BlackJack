import socket
from game_logic import BlackJackGame
import tkinter as tk
import json

INITIAL_PORT = 12345

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
        elif action == 'stand':
            game_status.set(f"Player {player_num} stands and waits.")
            bank_window.update()
        return action



    bank_window = tk.Tk()
    screen_width = bank_window.winfo_screenwidth()
    screen_height = bank_window.winfo_screenheight()

    window_width = 300
    window_height = 200

    x_position = (screen_width - window_width) // 2
    y_position = 0

    bank_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    bank_window.title("Blackjack - Bank")
    bank_window.attributes('-topmost', True) 

    game_status = tk.StringVar()
    game_status.set("Waiting for players to connect...")
    status_label = tk.Label(bank_window, textvariable=game_status)
    status_label.pack()

    

    HOST = 'localhost'

    game = BlackJackGame()

    def bank_program(PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
                server_socket.bind((HOST, PORT))
            except:
                PORT=PORT+1
                bank_program(PORT)
            print("Bank opened on port " + str(PORT))
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
            
            player1_standing = False
            player2_standing = False

            while not (player1_standing and player2_standing):
                if not player1_standing:
                    action1 = handle_player_turn(conn1, 1, player1_hand)
                    player1_standing = action1 == 'stand'
                if not player2_standing:
                    action2 = handle_player_turn(conn2, 2, player2_hand)
                    player2_standing = action2 == 'stand'

                bank_window.update()

                player1_value = game.calculate_hand_value(player1_hand)
                player2_value = game.calculate_hand_value(player2_hand)

                # Prüfen, ob einer der Spieler über 21 ist und der andere Spieler steht.
                if (player1_value > 21 and player2_standing) or (player2_value > 21 and player1_standing):
                    break

        


            player1_value = game.calculate_hand_value(player1_hand)
            player2_value = game.calculate_hand_value(player2_hand)

            if player1_value > 21:
                if player2_value > 21:
                    result1 = "It's a draw."
                    result2 = result1
                else:
                    result1 = "You lost."
                    result2 = "You won."
            elif player2_value > 21:
                result1 = "You won."
                result2 = "You lost."
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
            if result1 == "You won.":
                winner = "Player 1"
            elif result2 == "You won.":
                winner = "Player 2"
            else:
                winner = "Draw"

            game_status.set("Game finished. %s" %("It\'s a draw." if winner == "Draw" else f"Winner: {winner}"))
            # Fügen Sie die folgende Zeile hinzu, um die Aktualisierung des Bank-Fensters zu erzwingen
            bank_window.update_idletasks()
            bank_window.update()
    bank_program(INITIAL_PORT)
    bank_window.mainloop()

if __name__ == "__main__":
    main_bank_ui()
