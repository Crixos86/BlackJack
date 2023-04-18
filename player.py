import socket
from game_logic import BlackJackGame
import tkinter as tk
from tkinter import messagebox
import json
from PIL import Image, ImageTk
import os

HOST = 'localhost'
PORT = 12345
game = BlackJackGame()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def display_hand(hand, window):
    imgs = []
    for card in hand:
        imgs.append(Image.open(os.path.join(__location__,
                                            'imgs', card['rank'] + "_of_" + card['suit'] + ".png")))
    for index, img in enumerate(imgs):
        width, height = img.size
        img = img.resize((int(width*0.2), int(height*0.2)), Image.ANTIALIAS)
        tki = ImageTk.PhotoImage(img)
        l = tk.Label(window, image=tki)
        l.grid(row=3, column=0+index)
        l.img = tki
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
    result_label = tk.Label(window, text="", font=("Arial", 12, "bold"))
    result_label.grid(row=3, column=0, columnspan=2)


    

    def update_hand(hand):
        hand_label['text'] = f"Your hand: {display_hand(hand, window)}"
        hand_value_label['text'] = f"Hand value: {game.calculate_hand_value(hand)}"
    
    

    def set_buttons_state(state):
        hit_button['state'] = state
        stand_button['state'] = state

    def update_result(result):
        result_label['text'] = f"Game result: {result}"    

    return window, update_hand, set_buttons_state, hit_button, stand_button, update_result

def main_player_ui():
    player_window, update_hand, set_buttons_state, hit_button, stand_button, update_result = create_player_ui()

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
        screen_width = player_window.winfo_screenwidth()
        screen_height = player_window.winfo_screenheight()

        window_width = 600
        window_height = 300

        if player_num == "Player 1":
            x_position = 0
        else:
            x_position = screen_width - window_width

        y_position = window_height

        player_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        player_window.mainloop()

        print("Waiting for the game result...")
        result = client_socket.recv(1024).decode()
        print(f"Game result: {result}")
        update_result(result)



if __name__ == "__main__":
    main_player_ui()
