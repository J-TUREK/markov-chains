import numpy as np
import random

class Player():

    def __init__(self, name, starting_pot, bet_size) -> None:
        self.name = name
        self.starting_pot = starting_pot
        self.bet_size = bet_size
        self.hand = []
        self.hand_value = 0

    def draw_card(self, card):
        self.hand.append(card)
        player_hand_value = self.calculate_hand_value(self.hand)
        self.hand_value = player_hand_value
        print(f"{self.name}: cards: {self.hand}, hand value: {player_hand_value}")

    def reset_hand(self):
        self.hand = []

    def handle_win(self, blackjack=False, bet_size=None):
        bet = bet_size if bet_size else self.bet_size
        self.pot += 1.5 if blackjack else 1 * bet
        if blackjack: print("Player wins with blackjack")

    def handle_loss(self, bet_size=None):
        bet = bet_size if bet_size else self.bet_size
        self.pot -= bet

    def calculate_hand_value(self, cards:None):
        cards = cards if cards else self.hand
        count = 0
        for card in cards:
            if card == 1:
                count = count + 11 if count <= 10 else count + 1
            elif card in [2,3,4,5,6,7,8,9]:
                count += card
            else:
                count += 10
        return count

    def auto_play(self, cards, deal_card_callback:function):
        self.hand = cards
        self.hand_value = self.calculate_hand_value(self.hand)
        while self.hand_value <= 21:
            self.draw_card(deal_card_callback())
            if self.hand_value >= 17:
                return self.hand_value

class BlackJack():

    def __init__(self, player:Player, starting_pot=1000, bet_size=100, shoes=1) -> None:
        self.shoes = shoes
        self.player = player
        self.dealer = Player(name="Dealer", starting_pot=10*starting_pot, bet_size=bet_size)
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

    def blackjack_round(self, dealer:Player, player:Player):
        dealer.reset_hand()
        player.reset_hand()

        # Initiate the cards:

        # Deal the player card
        player.draw_card(self.deal_card())
        # Deal the dealer card
        dealer.draw_card(self.deal_card())
        # Deal the second player card
        player.draw_card(self.deal_card())
        # Deal the second dealer card, faced down.
        hidden_dealer_card = self.deal_card()

        # Hidden dealer cards
        hidden_dealer_cards = dealer.hand.copy()
        hidden_dealer_cards.append(hidden_dealer_card)
        
        # Initial hand values of player and dealer
        player_hand_value = player.hand_value
        dealer_hand_value = dealer.calculate_hand_value(hidden_dealer_cards)
        print("Player cards:", player.hand, "Player total: ", player_hand_value)
        print("Dealer cards:", dealer.hand, "dealer total: ", dealer.hand_value)

        if dealer_hand_value == 21 and not player_hand_value == 21:
            print("Hidden natural, blackjack")
            player.handle_loss()
            return

        elif player_hand_value == 21 and not dealer_hand_value == 21:
            player.handle_win(blackjack=True)
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
                player.draw_card(self.deal_card())

                if player.hand_value > 21:
                    player.handle_loss()
                    return

            elif decision == 1:
                dealer_value = self.play_dealer(hidden_dealer_cards)
                if dealer_value == player.hand_value: return

                elif dealer_value > player_hand_value and dealer_value <= 21:
                    player.handle_loss() 
                    return

                elif dealer_value < player_hand_value and player_hand_value <= 21:
                    player.handle_win()
                    return

            elif decision == 2:
                player.draw_card(self.deal_card())
                if player.hand_value() > 21:
                    self.handle_loss()
                    return

                dealer_value = dealer.auto_play(hidden_dealer_cards, self.deal_card)
                if dealer_value == player_hand_value: return

                if dealer_value > player_hand_value and dealer_value <= 21:
                    player.handle_loss(bet_size=2 * player.bet_size)
                    return

                elif dealer_value < player_hand_value and player_hand_value <= 21:
                    player.handle_win(bet_size=2 * player.bet_size)
                    return
            else:
                continue
                
    # def play_dealer(self, dealer_cards):
    #     dealer_cards_value = self.count_card_value(dealer_cards)
    #     while dealer_cards_value <= 21:
    #         dealer_cards.append(self.deal_card())
    #         dealer_cards_value = self.count_card_value(dealer_cards)
    #         if dealer_cards_value >= 17:
    #             return dealer_cards_value

    def simulate_game(self):

        while True:
            self.blackjack_round()
            print("\n")
            s = input("Press enter to continue: ")
            if s == "no" or s == "No" or s == "n":
                break
            print("Running count: ", self.running_count, "True count:", self.true_count)
            if len(self.deck) < 60:
                print("Creating new deck")
                self.deck = self.create_deck(self.shoes)

if __name__ == "__main__":

    player = Player(name="Jamie", starting_pot=1000, bet_size=100)

    bj = BlackJack(player, shoes=6, players=1)
    bj.simulate_game()