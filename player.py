import socket
from game_logic import BlackJackGame
import tkinter as tk
from tkinter import messagebox
import json

HOST = 'localhost'
PORT = 12345
game = BlackJackGame()

def display_hand(hand):
    return ', '.join([f"{card['rank']} of {card['suit']}" for card in hand])

def create_player_ui():
    window = tk.Tk()
    window.title("Blackjack - Player")

    hand_label = tk.Label(window, text="")
    hand_label.grid(row=0, column=0)

    hand_value_label = tk.Label(window, text="")
    hand_value_label.grid(row=1, column=0)

    hit_button = tk.Button(window, text="Hit", state="disabled")
    hit_button.grid(row=2, column=0)

    stand_button = tk.Button(window, text="Stand", state="disabled")
    stand_button.grid(row=2, column=1)

    def update_hand(hand):
        hand_label['text'] = f"Your hand: {display_hand(hand)}"
        hand_value_label['text'] = f"Hand value: {game.calculate_hand_value(hand)}"

    def set_buttons_state(state):
        hit_button['state'] = state
        stand_button['state'] = state

    return window, update_hand, set_buttons_state, hit_button, stand_button

def main_player_ui():
    player_window, update_hand, set_buttons_state, hit_button, stand_button = create_player_ui()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        player_num = client_socket.recv(1024).decode()
        player_window.title(f"Blackjack - {player_num}")
        print("Player: Receiving initial hand")
        hand = json.loads(client_socket.recv(1024).decode())
        update_hand(hand)
        set_buttons_state("normal")

        def hit():
            client_socket.sendall("hit".encode())
            response = client_socket.recv(1024).decode()
            try:
                card = json.loads(response)
            except json.JSONDecodeError:
                print("Invalid JSON format received.")
                return
            hand.append(card)
            update_hand(hand)
            if game.calculate_hand_value(hand) > 21:
                set_buttons_state("disabled")
                messagebox.showinfo("Busted", "You are busted. Wait for the game result.")
                player_window.quit()



        def stand():
            client_socket.sendall("stand".encode())
            set_buttons_state("disabled")
            messagebox.showinfo("Stand", "You chose to stand. Wait for the game result.")
            player_window.quit()

        hit_button['command'] = hit
        stand_button['command'] = stand

        player_window.mainloop()

        print("Waiting for the game result...")
        result = client_socket.recv(1024).decode()
        print(f"Game result: {result}")
        messagebox.showinfo("Game result", result)

if __name__ == "__main__":
    main_player_ui()
