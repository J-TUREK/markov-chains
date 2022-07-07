import numpy as np
import random

class Player():

    def __init__(self, name, starting_pot, bet_size) -> None:
        self.name = name
        self.starting_pot = starting_pot
        self.bet_size = bet_size
        self.hand = []

    def draw_card(self, card, hand_value_callback):
        self.hand.append(self.deal_card())
        player_hand_value = hand_value_callback(self.hand)
        print(f"{self.name}: ")

    def reset_hand(self):
        self.hand = []

class BlackJack():

    def __init__(self, starting_pot=1000, bet_size=100, shoes=1, players=1) -> None:
        self.shoes = shoes
        self.players = players
        self.pot = starting_pot
        self.bet_size = bet_size
        self.deck = self.create_deck(shoes)
        self.running_count = 0
        self.true_count = 0

    def create_deck(self, shoes=1):
        ''' Create a numeric representation of a deck of cards with potentially many shoes '''
        deck = [x + 1 for _ in range(4 * shoes if shoes > 0 else 1) for x in range(13)]
        deck.sort()
        return deck

    def count_card(self, card):
        if card in [2,3,4,5,6]: self.running_count += 1
        elif card in [7,8,9]: self.running_count += 0
        else: self.running_count += -1
        self.true_count = self.running_count / self.shoes

    def deal_card(self):
        card = random.choice(self.deck)
        self.count_card(card)
        self.remove_card_from_deck(card)
        return card

    def remove_card_from_deck(self, card):
        self.deck.remove(card)

    def handle_win(self, blackjack=False, bet_size=None):
        bet = bet_size if bet_size else self.bet_size
        self.pot += 1.5 if blackjack else 1 * bet

    def handle_loss(self, bet_size=None):
        bet = bet_size if bet_size else self.bet_size
        self.pot -= bet

    def blackjack_round(self):
        dealer_cards = []
        player_cards = []
        # Initiate the cards:

        # Deal the player card
        player_cards.append(self.deal_card())
        # Deal the dealer card
        dealer_cards.append(self.deal_card())
        # Deal the second player card
        player_cards.append(self.deal_card())
        # Deal the second dealer card, faced down.
        hidden_dealer_card = self.deal_card()

        # Hidden dealer cards
        hidden_dealer_cards = dealer_cards.copy()
        hidden_dealer_cards.append(hidden_dealer_card)
        
        # Initial hand values of player and dealer
        player_hand_value = self.count_card_value(player_cards)
        dealer_hand_value = self.count_card_value(hidden_dealer_cards)
        print("Player cards:", player_cards, "Player total: ", player_hand_value)
        print("Dealer cards:", dealer_cards, "dealer total: ", self.count_card_value(dealer_cards))

        if dealer_hand_value == 21 and not player_hand_value == 21:
            print("Hidden natural, blackjack")
            self.handle_loss()
            return
            
        if player_hand_value == 21 and not dealer_hand_value == 21:
            print("Player wins with blackjack")
            self.handle_win(blackjack=True)
            return

        if player_hand_value == 21 and dealer_hand_value == 21:
            return

        while player_hand_value <=21 and dealer_hand_value <= 21:
            decision = input(
"""
hit: 0
Stand: 1
double: 2
""")

            if decision == 0:
                player_cards.append(self.deal_card())
                player_hand_value = self.count_card_value(player_cards)
                print("")

                if player_hand_value > 21:
                    self.handle_loss()
                    return

            elif decision == 1:
                dealer_value = self.play_dealer(hidden_dealer_cards)
                if dealer_value == player_hand_value: return

                elif dealer_value > player_hand_value and dealer_value <= 21:
                    self.handle_loss() 
                    return

                elif dealer_value < player_hand_value and player_hand_value <= 21:
                    self.handle_win()
                    return

            elif decision == 2:
                player_cards.append(self.deal_card())
                player_hand_value = self.count_card_value(player_cards)
                if player_hand_value > 21:
                    self.handle_loss()
                    return

                dealer_value = self.play_dealer(hidden_dealer_cards)
                if dealer_value == player_hand_value: return

                if dealer_value > player_hand_value and dealer_value <= 21:
                    self.handle_loss(bet_size=2 * self.bet_size)
                    return

                elif dealer_value < player_hand_value and player_hand_value <= 21:
                    self.handle_win(bet_size=2 * self.bet_size)
                    return
            else:
                continue
                

    def play_dealer(self, dealer_cards):
        dealer_cards_value = self.count_card_value(dealer_cards)
        while dealer_cards_value <= 21:
            dealer_cards.append(self.deal_card())
            dealer_cards_value = self.count_card_value(dealer_cards)
            if dealer_cards_value >= 17:
                return dealer_cards_value
            

    def count_card_value(self, cards):
        count = 0
        for card in cards:
            if card == 1:
                count = count + 11 if count <= 10 else count + 1
            elif card in [2,3,4,5,6,7,8,9]:
                count += card
            else:
                count += 10
        return count

    def simulate_game(self):

        while True:
            self.blackjack_round()
            print("\n")
            s = input("Press enter to continue: ")
            if s == "no" or s == "No" or s == "n":
                break
            print("Running count: ", self.running_count, "True count:", self.true_count)
            if len(self.deck) < 60:
                self.deck = self.create_deck(self.shoes)

if __name__ == "__main__":

    bj = BlackJack(shoes=6, players=1)
    bj.simulate_game()