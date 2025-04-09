import time
import math
import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                            QVBoxLayout, QHBoxLayout, QSizePolicy, QInputDialog, 
                            QPushButton, QLabel, QMessageBox)
from PyQt5.QtGui import (QColor, QPalette, QFont, QIcon, QPainter, QPixmap)
from PyQt5.QtCore import (QCoreApplication, Qt, QTimer, QSize, QPropertyAnimation, 
                         QEasingCurve)


class Card(QPushButton):
    def __init__(self, value, row, col):
        super().__init__()
        self.value = value
        self.row = row
        self.col = col
        self.is_flipped = False
        self.is_matched = False
        self.setIcon(QIcon('images/card_back.png'))
        self.setIconSize(QSize(80, 80))
        self.setText("")

    def flip(self):
        if self.is_flipped:
            self.setIcon(QIcon('images/card_back.png'))
        else:
            self.setIcon(QIcon(f'images/card{self.value}.png'))
        self.is_flipped = not self.is_flipped

    def matched(self):
        self.matched = True
        self.setStyleSheet("background-color: lightgreen")

class Player:
    def __init__(self, name):
        self.name = name
        self.matched_pairs = 0

class MemoryGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Game")
        self.setStyleSheet('background-color: lightblue')
        self.setFixedSize(600, 750)
        
        # Game variables
        self.game_started = False
        self.cards = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.total_pairs = 18
        self.card_values = []
        self.Players = []
        self.current_player_index = 0
        self.reveals_remaining = 3  # reveal system variable

        # Initialize UI
        self.start_ui()

    def start_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        title_label = QLabel("Memory Game")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title_label)
        
        solo_button = QPushButton("Solo")
        solo_button.setFont(QFont("Arial", 16))
        solo_button.clicked.connect(self.setup_solo_game)
        layout.addWidget(solo_button)
        
        multi_button = QPushButton("Multiplayer")
        multi_button.setFont(QFont("Arial", 16))
        multi_button.clicked.connect(self.setup_multiplayer_game)
        layout.addWidget(multi_button)
        
        layout.addSpacing(20)

    def setup_solo_game(self):
        name, ok = QInputDialog.getText(self, "Player Name", "Enter your name:")
        if ok and name:
            num_card, ok2 = QInputDialog.getInt(self, "Number of Pairs", 
                                              "Enter number of pairs (2-18):", 
                                              18, min=2, max=18)
            if ok2 and num_card:    
                self.total_pairs = num_card
                self.Players = [Player(name)]
                self.current_player_index = 0
                self.init_ui()
                self.init_game()

    def setup_multiplayer_game(self):
        num_players, ok = QInputDialog.getInt(self, "Number of Players", 
                                            "Enter number of players (2-4):", 
                                            min=2, max=4)
        if ok and num_players:
            self.Players = []
            for i in range(num_players):
                while True:
                    name, ok = QInputDialog.getText(self, f"Player {i+1} Name", 
                                                  f"Enter name for Player {i+1}:")
                    if not ok:
                        return
                    
                    if name and name not in [p.name for p in self.Players]:
                        self.Players.append(Player(name))
                        break
                    else:
                        QMessageBox.warning(self, "Invalid Name", 
                                         "Name cannot be empty or duplicate. Please try again.")
            num_card, ok2 = QInputDialog.getInt(self, "Number of Pairs", 
                                            "Enter number of pairs (2-18):",
                                            18, min=2, max=18)
            if ok2 and num_card:    
                self.total_pairs = num_card
                self.current_player_index = 0
                self.init_ui()
                self.init_game(num_players)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        Turn_layout = QHBoxLayout()
        self.turn_label = QLabel(f"{self.Players[self.current_player_index].name}'s turn")
        self.turn_label.setAlignment(Qt.AlignLeft)
        self.turn_label.setFont(QFont("Arial", 14))
        Turn_layout.addWidget(self.turn_label)

        self.score_label = QLabel(f"Pairs found: {self.Players[self.current_player_index].matched_pairs}")
        self.score_label.setAlignment(Qt.AlignRight)
        self.score_label.setFont(QFont("Arial", 14))
        Turn_layout.addWidget(self.score_label)
        main_layout.addLayout(Turn_layout)

        # Add reveal button here
        if len(self.Players) == 1:
            self.reveal_button = QPushButton(f"reveal ({self.reveals_remaining} left)")
            self.reveal_button.setFont(QFont("Arial", 12))
            self.reveal_button.clicked.connect(self.give_reveal)
            main_layout.addWidget(self.reveal_button)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        self.grid_layout.setSpacing(5)
        main_layout.addWidget(self.grid_widget)
        
        self.restart_button = QPushButton("Restart Game")
        self.restart_button.setFont(QFont("Arial", 12))
        self.restart_button.clicked.connect(self.start_ui)
        main_layout.addWidget(self.restart_button)

    def init_game(self, n=1):
        self.matched_pairs = 0
        self.flipped_cards = []
        self.reveals_remaining = 3  # Reset reveals on new game
        if len(self.Players) == 1:
            self.reveal_button.setText(f"reveal ({self.reveals_remaining} left)")
            self.reveal_button.setEnabled(True)
        self.update_score() 
        self.game_started = True
        
        for player in self.Players:
            player.matched_pairs = 0

        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        self.card_values = [i for i in range(1, self.total_pairs + 1)] * 2
        random.shuffle(self.card_values)
        n = math.ceil(math.sqrt(self.total_pairs * 2)) 
        
        self.cards = []
        for i in range(self.total_pairs*2):
            row, col = i%n, i//n
            card = Card(self.card_values[i], row, col)
            if card.is_flipped:
                card.flip()
            card.clicked.connect(lambda _, c=card: self.card_clicked(c))
            self.cards.append(card)
            self.grid_layout.addWidget(card, row, col)

    def give_reveal(self):
        """Reveals two matching cards briefly when reveal button is clicked"""
        if not self.game_started or self.reveals_remaining <= 0:
            return
            
        # Find all unmatched and unflipped cards
        available_cards = [card for card in self.cards 
                        if not card.is_matched and not card.is_flipped]
        
        if len(available_cards) < 2:
            return
            
        # Create dictionary to group cards by value
        value_groups = {}
        for card in available_cards:
            if card.value not in value_groups:
                value_groups[card.value] = []
            value_groups[card.value].append(card)
        
        # Filter groups that have at least 2 cards (potential matches)
        potential_matches = {k:v for k,v in value_groups.items() if len(v) >= 2}
        
        if not potential_matches:
            return
            
        # Choose a random value that hasn't been revealed yet
        revealed_values = getattr(self, 'revealed_values', set())
        available_values = [v for v in potential_matches.keys() if v not in revealed_values]
        
        # If we've revealed all values, reset the tracking
        if not available_values:
            self.revealed_values = set()
            available_values = list(potential_matches.keys())
        
        chosen_value = random.choice(available_values)
        
        # Track this value so we don't reveal it again
        if not hasattr(self, 'revealed_values'):
            self.revealed_values = set()
        self.revealed_values.add(chosen_value)
        
        # Get two cards with this value
        cards_with_value = value_groups[chosen_value]
        matching_pair = random.sample(cards_with_value, 2)
        
        # Update reveal counter
        self.reveals_remaining -= 1
        self.reveal_button.setText(f"reveal ({self.reveals_remaining} left)")
        if self.reveals_remaining <= 0:
            self.reveal_button.setEnabled(False)
        
        # Briefly show the matching pair
        for card in matching_pair:
            self.animate_reveal_reveal(card)
            
        # Hide them after delay
        QTimer.singleShot(1500, lambda: [self.animate_reveal_hide(card) for card in matching_pair])
 

    def animate_reveal_reveal(self, card):
        """Animation to show a card for the reveal"""
        if card.is_flipped:
            return
            
        animation = QPropertyAnimation(card, b"iconSize")
        animation.setDuration(300)
        animation.setStartValue(QSize(0, 80))
        animation.setEndValue(QSize(80, 80))
        animation.setEasingCurve(QEasingCurve.OutBack)
        
        # Change to front image at start
        card.setIcon(QIcon(f'images/card{card.value}.png'))
        animation.start()
        
    def animate_reveal_hide(self, card):
        """Animation to hide a card after reveal"""
        if card.is_matched or card.is_flipped:
            return
            
        animation = QPropertyAnimation(card, b"iconSize")
        animation.setDuration(300)
        animation.setStartValue(QSize(80, 80))
        animation.setEndValue(QSize(0, 80))
        animation.setEasingCurve(QEasingCurve.InBack)
        
        # Change back to back image at end
        animation.finished.connect(lambda: card.setIcon(QIcon('images/card_back.png')))
        animation.start()

    def card_clicked(self, card):
        if not self.game_started or not card or card.is_matched or card.is_flipped or len(self.flipped_cards) >= 2:
            return
        
        card.flip()
        self.flipped_cards.append(card)

        if len(self.flipped_cards) == 2:
            self.check_match()

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.Players)
        self.turn_label.setText(f"{self.Players[self.current_player_index].name}'s turn")
        self.score_label.setText(f"Pairs found: {self.Players[self.current_player_index].matched_pairs}")

    def check_match(self):
        card1, card2 = self.flipped_cards
        
        if card1.value == card2.value:
            card1.matched()
            card2.matched()
            self.flipped_cards = []
            
            current_player = self.Players[self.current_player_index]
            current_player.matched_pairs += 1
            self.matched_pairs += 1
            
            if self.matched_pairs == self.total_pairs:
                self.game_over()
                return
            
            self.update_score()
        else:
            QTimer.singleShot(1000, self.flip_cards_back)

    def update_score(self):
        self.score_label.setText(f"Pairs found: {self.Players[self.current_player_index].matched_pairs}")

    def flip_cards_back(self):
        for card in self.flipped_cards:
            card.flip()
        self.flipped_cards = []
        self.next_player()

    def game_over(self):
        self.game_started = False
        max_pairs = max(player.matched_pairs for player in self.Players)
        winners = [player for player in self.Players if player.matched_pairs == max_pairs]
        
        if len(winners) == 1:
            message = f"Game Over!\n{winners[0].name} wins with {max_pairs} pairs!"
        else:
            winner_names = ", ".join([w.name for w in winners])
            message = f"Game Over!\nIt's a tie between {winner_names} with {max_pairs} pairs each!"
        
        QMessageBox.information(self, "Game Over", message)
        self.start_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = MemoryGame()
    game.show()
    sys.exit(app.exec_())
