import os
import sys
import multiprocessing
import time

def run_bank():
    os.system("python3 bank.py")

def run_player1():
    time.sleep(1)  
    os.system("python3 player.py")

def run_player2():
    time.sleep(1)  
    os.system("python3 player.py")

if __name__ == "__main__":
    bank_process = multiprocessing.Process(target=run_bank)
    player1_process = multiprocessing.Process(target=run_player1)
    player2_process = multiprocessing.Process(target=run_player2)

    try:
        bank_process.start()
        player1_process.start()
        player2_process.start()

        bank_process.join()
        player1_process.join()
        player2_process.join()
    finally:
        # Sicherstellen, dass alle Prozesse beendet werden
        bank_process.terminate()
        player1_process.terminate()
        player2_process.terminate()
