import random
import os

CHIPS_FILE = "chips.txt"

BANNER = r"""
.------.           ___ _         _    _         _   
|A_  _ |.         | _ ) |__ _ __| |__(_)__ _ __| |__
|( V ).-----.     | _ \ / _` / _| / /| / _` / _| / /
| \ /|K/\  |      |___/_\__,_\__|_\_\/ \__,_\__|_\_\
|  V | /  \ |                      |__/             
`-----|  \/ |     
      |  V K|     
      `------'    
"""


class Card:

    SUITS = ("Spades", "Hearts", "Diamonds", "Clubs")
    SUIT_SYMBOLS = {"Spades": "♠", "Hearts": "♥", "Diamonds": "♦", "Clubs": "♣"}
    RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def value(self):
        if self.rank in ("J", "Q", "K"):
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)

    def __str__(self):
        return f"{self.rank}{self.SUIT_SYMBOLS[self.suit]}"

    def __repr__(self):
        return self.__str__()


class Deck:

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if not self.cards:
            self.build()
            self.shuffle()
        return self.cards.pop()


class Hand:

    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        total = sum(card.value() for card in self.cards)
        ace_count = sum(1 for card in self.cards if card.rank == "A")

        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        return total

    def is_bust(self):
        return self.get_value() > 21

    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def __str__(self):
        cards_str = ", ".join(str(c) for c in self.cards)
        return f"{cards_str}  (Total: {self.get_value()})"


class Chips:

    def __init__(self, total=100):
        self.total = total
        self.bet_amount = 0

    def bet(self, amount):
        if amount <= 0 or amount > self.total:
            return False
        self.bet_amount = amount
        return True

    def win(self):
        self.total += self.bet_amount

    def lose(self):
        self.total -= self.bet_amount

    def push(self):
        pass

    def save_to_file(self, filename=CHIPS_FILE):
        try:
            with open(filename, "w") as f:
                f.write(str(self.total))
        except Exception as e:
            print(f"Could not save chips: {e}")

    @staticmethod
    def load_from_file(filename=CHIPS_FILE, default=100):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    value = int(f.read().strip())
                    return Chips(value)
            except (ValueError, IOError):
                return Chips(default)
        return Chips(default)


class BlackjackGame:

    def __init__(self):
        self.deck = Deck()
        self.chips = Chips.load_from_file()
        self.wins = 0
        self.losses = 0
        self.pushes = 0

    def get_bet_amount(self):
        while True:
            raw = input(f"\nYou have {self.chips.total} chips. Enter your bet: ")
            try:
                amount = int(raw)
            except ValueError:
                # Non-numeric input should not crash the program
                print("Please enter a number only (e.g. 50). Try again.")
                continue

            if self.chips.bet(amount):
                return amount
            else:
                print("Invalid bet (must be greater than 0 and no more than your balance).")

    def deal_initial_cards(self):
        player_hand = Hand("Player")
        dealer_hand = Hand("Dealer")

        for _ in range(2):
            player_hand.add_card(self.deck.deal_card())
            dealer_hand.add_card(self.deck.deal_card())

        return player_hand, dealer_hand

    def print_summary(self, player_hands, dealer_hand, reveal_dealer=False):
        print("\n" + "=" * 50)
        print("ROUND SUMMARY")
        print("=" * 50)

        for idx, hand in enumerate(player_hands, start=1):
            label = f"Player Hand {idx}" if len(player_hands) > 1 else "Player Hand"
            print(f"{label:<15}: {hand}")

        if reveal_dealer:
            print(f"{'Dealer Hand':<15}: {dealer_hand}")
        else:
            hidden = f"{dealer_hand.cards[0]}, ??"
            print(f"{'Dealer Hand':<15}: {hidden}")

        print(f"{'Current Chips':<15}: {self.chips.total}")
        print("=" * 50)

    def play_single_hand(self, hand):
        while True:
            print(f"\nYour Hand: {hand}")
            if hand.is_bust():
                print("Bust! This hand has lost.")
                return False
            if hand.get_value() == 21:
                print("21! Perfect hand.")
                return True

            choice = input("Hit (h) or Stand (s)? ").strip().lower()
            if choice == "h":
                new_card = self.deck.deal_card()
                print(f"You drew: {new_card}")
                hand.add_card(new_card)
            elif choice == "s":
                return True
            else:
                print("Please enter 'h' or 's' only.")

    def dealer_play(self, dealer_hand):
        print(f"\nDealer's Hand (revealed): {dealer_hand}")
        while dealer_hand.get_value() < 17:
            new_card = self.deck.deal_card()
            print(f"Dealer drew: {new_card}")
            dealer_hand.add_card(new_card)
            print(f"Dealer's Hand now: {dealer_hand}")

    def decide_winner(self, player_hand, dealer_hand):
        player_value = player_hand.get_value()
        dealer_value = dealer_hand.get_value()

        if player_hand.is_bust():
            print("You busted — Dealer wins.")
            self.chips.lose()
            self.losses += 1
        elif dealer_hand.is_bust():
            print("Dealer busted — You win!")
            self.chips.win()
            self.wins += 1
        elif player_value > dealer_value:
            print("You win!")
            self.chips.win()
            self.wins += 1
        elif player_value < dealer_value:
            print("Dealer wins.")
            self.chips.lose()
            self.losses += 1
        else:
            print("Push (Tie) — bet returned.")
            self.chips.push()
            self.pushes += 1

    def play_round(self):
        self.deck.shuffle()
        bet_amount = self.get_bet_amount()
        player_hand, dealer_hand = self.deal_initial_cards()

        print(f"\nYour Hand: {player_hand}")
        print(f"Dealer's Hand: {dealer_hand.cards[0]}, ??")

        player_hands = [player_hand]
        if player_hand.can_split():
            split_choice = input(
                f"\nYour first two cards match ({player_hand.cards[0].rank}, "
                f"{player_hand.cards[1].rank}). Split into two hands? (y/n): "
            ).strip().lower()
            if split_choice == "y":
                card1, card2 = player_hand.cards
                hand_a = Hand("Player")
                hand_b = Hand("Player")
                hand_a.add_card(card1)
                hand_a.add_card(self.deck.deal_card())
                hand_b.add_card(card2)
                hand_b.add_card(self.deck.deal_card())
                player_hands = [hand_a, hand_b]
                print(f"\nHand 1: {hand_a}")
                print(f"Hand 2: {hand_b}")

        any_alive = False
        for idx, hand in enumerate(player_hands, start=1):
            if len(player_hands) > 1:
                print(f"\n--- Playing Hand {idx} ---")
            alive = self.play_single_hand(hand)
            if alive:
                any_alive = True

        if any_alive:
            self.dealer_play(dealer_hand)
        else:
            print("\n(All player hands have busted, no need for the dealer to play.)")

        for hand in player_hands:
            print(f"\n--- Result: {hand} vs Dealer {dealer_hand} ---")
            self.decide_winner(hand, dealer_hand)

        self.print_summary(player_hands, dealer_hand, reveal_dealer=True)
        self.chips.save_to_file()

    def final_report(self):
        print("\n" + "#" * 50)
        print("FINAL REPORT")
        print("#" * 50)
        print(f"Total Wins   : {self.wins}")
        print(f"Total Losses : {self.losses}")
        print(f"Total Pushes : {self.pushes}")
        print(f"Final Chips  : {self.chips.total}")
        print("#" * 50)
        print("Thanks for playing!")

    def run(self):
        print(BANNER)

        while True:
            if self.chips.total <= 0:
                print("\nYou're out of chips.")
                restart = input("Reset and start over with 100 chips? (y/n): ").strip().lower()
                if restart == "y":
                    self.chips = Chips(100)
                    continue
                else:
                    print("Game over.")
                    break

            self.play_round()

            again = input("\nPlay another round? (y/n): ").strip().lower()
            if again != "y":
                break

        self.chips.save_to_file()
        self.final_report()


if __name__ == "__main__":
    game = BlackjackGame()
    game.run()