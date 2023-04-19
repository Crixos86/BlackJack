# BlackJack
Das vorliegende Projekt beinhaltet eine Implementierung des Kartenspiels Blackjack. Die Implementierung besteht aus vier Python-Dateien: 
- `game_logic.py`
- `bank.py`
- `player.py`
- `run_game.py`

## Spielverlauf und Voraussetzungen:
- Minimum Python Version 3.9
- Um das Spiel zu starten ```python3 run_game.py ``` im terminal innerhalb des Projektverzeichnisses ausführen
- Es erscheinen drei Fenster, eines für die Bank und zwei für die beiden Spieler
- Jeder Spieler hat die Möglichkeit `hit` oder `stand` auszuführen um entweder eine neue Karte anzufordern oder zu passen und das Spielergebnis abzuwarten
- Nachdem beide Spieler ihr Endwerte haben, zeigt das Bank Fenster an, welcher Spieler gewonnen hat

## Sicherheit gegen Betrug
Die Klasse `BlackJackGame` der Komponente `game_logic.py` ist eine Implementierung des Kartenspiels Blackjack. Der Grund, warum sie besonders gut gegen Betrug geeignet ist, liegt in der Methode shuffle_deck(). In dieser Methode wird ein zufälliger Seed generiert, indem die aktuelle Systemzeit mit der hashlib.sha256()-Funktion gehasht wird. Dieser Seed wird dann verwendet, um den Zufallsgenerator von Python zu initialisieren, bevor er zum Mischen des Decks verwendet wird. Durch die Verwendung eines zufälligen Seeds, der auf der Systemzeit basiert, wird es sehr schwierig, vorherzusagen, welche Karten im Deck landen werden. Dies macht es schwieriger für Spieler, durch Betrug zu gewinnen, indem sie das Deck manipulieren. <br/> Die Implementierung des Mental Poker Protokolls wurde aus Zeitgründen nicht realisiert, da das geplante Zeitkontingent bereits erschöpft war. Zusätzlich ist Mental Poker eher für P2P Situationen geeignet, wohingegen in diesem Projekt eine lokale Client Server Architektur implementiert wird, bei der die Bank die Autorität innehat und mit den genannten Features ein sicheres Verteilen der Karten ermöglicht.

## Die Komponente run_game
Die Datei startet ein Multi-Processing-Programm, das die drei anderen Python-Skripte ausführt.
- `run_bank()`: führt das `bank.py`-Skript aus.
- `run_player1 ()`: führt das `player.py`-Skript aus, das dem ersten Spieler entspricht.
- `run _player2()`: führt das `player.py`-Skript aus, das dem zweiten Spieler entspricht.
Die drei Prozesse werden gestartet und laufen parallel. Der Prozess "bank_process" startet als erster und die Prozesse "player1 process" und "player2 process" starten mit einer
Verzögerung von drei Sekunden. Schließlich werden alle Prozesse beendet, um sicherzustellen, dass keine Hintergrundprozesse mehr laufen, nachdem das Programm beendet wurde.

## Die Komponente game_logic
Neben den genannten Sicherheitsfeatures ist die Klasse `game_logic.py` für die Logik des Spielablaufs verantwortlich und beinhaltet folgende Methoden:
- `create_deck(self)`: erstellt ein Deck aus 52 Karten, bestehend aus 4 Farben (Hearts, Diamonds, Clubs, Spades) und 13 Kartenwerten (2-10, Jack, Queen, King, Ace). Das Deck wird als Liste von Dictionaries zurückgegeben, wobei jedes Dictionary die
Kartenfarbe und den Kartenwert enthält.
- `shuffle_deck(self)`: mischt das Deck mit einem Zufallszahlengenerator und einem "Seed", der aus der aktuellen Zeit generiert wird. Dafür wird die Bibliothek hashlib
verwendet, um eine SHA-256-Hashfunktion auf die aktuelle Zeit anzuwenden. Der daraus resultierende Hash wird als Seed für den Zufallszahlengenerator verwendet, um das Deck zu mischen.
- `get _card _value (self, card)`: gibt den Wert einer Karte zurück, wobei Karten mit den Werten Jack, Queen und King einen Wert von 10 und Karten mit dem Wert Ace einen Wert von 11 haben. Alle anderen Karten haben ihren entsprechenden Kartenwert.
- `calculate_hand_value(self, hand)`: berechnet den Gesamtwert einer Hand aus Karten. Sie summiert die Werte aller Karten und passt den Wert von Assen an, falls der Gesamtwert 21 überschreitet. Wenn der Gesamtwert 21 überschreitet und die Hand ein Ass enthält, wird der Wert des Asses von 11 auf 1 reduziert, um den Gesamtwert um 10 zu verringern(Gemäß Spielregeln kann ein Ass entweder den Wert 11 oder 1 annehmen).

## Die Komponente bank
Die Komponente `bank.py` implementiert ein Blackjack-Spiel, das über das Netzwerk zwischen einem Spieler und einer Bank gespielt wird. Die Bank ist ein Server und die Spieler sind Clients, die sich mit der Bank verbinden und über eine Socket-Verbindung kommunizieren. Dazu nutzen Spieler und die Bank das `BlackJackGame`-Objekt aus der game_ logic-Komponente, um das Spiel durchzuführen. Die Bank ist für die Durchführung des Spiels zuständig, sie teilt die Karten aus, verarbeitet die Spielzüge und gibt am Ende das Ergebnis bekannt. Die Spieler
treten gegeneinander an, um zu gewinnen, indem sie Karten sammeln, deren Gesamtwert 21 oder nahe daran liegt, ohne sich zu überkaufen. Die Datei implementiert auch eine Benutzeroberfläche für die Bank, die den Spielverlauf anzeigt.
- `handle_player turn` akzeptiert eine Verbindung (conn), die Nummer des Spielers (player_num) und die Hand des Spielers (player hand) als Argumente. Die Methode berechnet den aktuellen Wert der Hand (hand value). Wenn der Wert der Hand
größer als 21 ist, gibt die Methode stand zurück, um anzuzeigen, dass der Spieler nicht mehr ziehen kann. Andernfalls empfängt sie eine Aktion (action) vom Client, der diese Verbindung verwendet. Wenn die Aktion "hit" ist, teilt die Methode eine Karte aus (card) und fügt sie der Hand des Spielers hinzu. Die Methode sendet auch die Karte an den Client,
der die Verbindung verwendet. Wenn die Aktion "stand" ist, aktualisiert die Methode den Status des Spiels und gibt "stand" zurück, um anzuzeigen, dass der Spieler nicht mehr zieht.
- `main_bank ui` ist die Hauptmethode des Codes. Sie erstellt das Benutzeroberflächenfenster (bank_window), initialisiert den Spielstatus (game_status), erstellt das Blackjack-Spiel (game) und bindet den Socket an den Host und Port (HOST,PORT). Die Methode akzeptiert Verbindungen von zwei Spielern (conn1,conn2), teilt jedem Spieler seine Hand mit und führt einen Schleifendurchlauf aus, in dem jeder Spieler abwechselnd eine Aktion ausführt. Sobald beide Spieler nicht mehr ziehen, wird der Gewinner ermittelt, und das Ergebnis wird an die Spieler gesendet. Schließlich wird die Verbindung geschlossen, und das Ergebnis wird im Spielstatus aktualisiert.
- `handle_player turn` ist besonders gut gegen Betrug geeignet, da sie die Aktionen des Spielers validiert und nur gültige Aktionen akzeptiert. Wenn ein Spieler versucht, eine ungültige Aktion auszuführen, wird die Aktion abgelehnt und nicht auf der Hand des Spielers angewandt. 

## Die Komponente player
Die Datei implementiert eine grafische Benutzeroberfläche (GUI) für einen Spieler im Blackjack-Spiel. Die GUI besteht aus einem Fenster mit verschiedenen Elementen, wie z.B. einem Label zur Anzeige der Spielerhand und Schaltflächen zum Anfordern von neuen Karten (Hit) oder zum Passen (Stand). 
- `display_hand (hand, window)`: zeigt die übergebene Hand im Fenster an und gibt die Hand als Zeichenfolge zurück.
- `create_player ui ()`: Diese Methode erstellt das Fenster und die GUI-Elemente und gibt sie als Rückgabewerte zurück.
- `main_player_ui ()`: Diese Methode startet das Fenster, behandelt die Benutzereingabe und die Serverkommunikation und zeigt das Ergebnis des Spiels an.


