"""Blackjack terminal game: one human player versus a bot.

The game asks for the bot difficulty once at the start of the session, then asks
how many rounds the player wants to play. Each round uses a fresh shuffled deck.
At the end, the script prints a session summary with player wins, bot wins, and draws.
"""

import random

# A standard 52-card deck using suit and rank pairs. Each card is stored as a tuple:
# (rank, suit), for example ("A", "♥").
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}


def get_card_value(card_rank):
    """Return the numeric value for a given rank."""
    return CARD_VALUES[card_rank]


def calculate_hand_value(hand):
    """Calculate the hand total while correctly reducing Ace values as needed."""
    total = 0
    aces = 0

    for rank, _ in hand:
        total += get_card_value(rank)
        if rank == "A":
            aces += 1

    # If the hand exceeds 21, convert Aces from 11 to 1 until the total is valid.
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


class Deck:
    """A shuffled deck that can be drawn from repeatedly."""

    def __init__(self):
        # Create a full deck of cards and shuffle it once at creation time.
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        """Return a card from the deck and reshuffle if the deck is empty."""
        if not self.cards:
            self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
            random.shuffle(self.cards)
        return self.cards.pop()


def display_hand(hand, hide_first=False):
    """Return a readable string version of a hand.

    When hide_first is True, the first card is replaced with [hidden] to simulate a
    dealer or bot hiding one card.
    """
    if not hand:
        return "[]"

    if hide_first:
        shown = ["[hidden]"] + [f"{rank}{suit}" for rank, suit in hand[1:]]
        return " ".join(shown)

    return " ".join(f"{rank}{suit}" for rank, suit in hand)


def bot_turn(bot_hand, deck, difficulty):
    """Let the bot decide whether to hit or stand based on its configured difficulty."""
    bot_total = calculate_hand_value(bot_hand)

    while True:
        if bot_total > 21:
            return

        if difficulty == "easy":
            # Easy bot is cautious but still takes risks. It stands at 18+ and hits
            # about 55% of the time below that threshold.
            if bot_total >= 18:
                return
            if random.random() < 0.55:
                bot_hand.append(deck.draw())
                bot_total = calculate_hand_value(bot_hand)
                continue
            return

        if difficulty == "medium":
            # Medium bot hits until it reaches 17, which gives a balanced challenge.
            if bot_total >= 17:
                return
            bot_hand.append(deck.draw())
            bot_total = calculate_hand_value(bot_hand)
            continue

        if difficulty == "hard":
            # Hard bot is aggressive. It hits more often at lower totals and only stops
            # at a stronger total, with a small chance of taking a risky draw at mid-range.
            if bot_total >= 19:
                return
            if bot_total <= 11:
                bot_hand.append(deck.draw())
                bot_total = calculate_hand_value(bot_hand)
                continue

            if 12 <= bot_total <= 18:
                if random.random() < 0.25:
                    bot_hand.append(deck.draw())
                    bot_total = calculate_hand_value(bot_hand)
                    continue
                return

            bot_hand.append(deck.draw())
            bot_total = calculate_hand_value(bot_hand)
            continue


def print_round_header(round_number):
    """Print a separator and a title for each round."""
    print("\n" + "=" * 30)
    print(f"Round {round_number}")
    print("=" * 30)


def choose_difficulty():
    """Prompt the user once for the bot difficulty and return the selected level."""
    print("Choose bot difficulty:")
    print("1) Easy")
    print("2) Medium")
    print("3) Hard")

    while True:
        choice = input("Your choice: ").strip().lower()
        if choice in {"1", "easy"}:
            return "easy"
        if choice in {"2", "medium"}:
            return "medium"
        if choice in {"3", "hard"}:
            return "hard"
        print("Invalid choice. Please choose 1, 2, or 3.")


def ask_round_count():
    """Ask for the number of rounds to play in the current session."""
    while True:
        try:
            rounds = int(input("How many rounds would you like to play? ").strip())
            if rounds > 0:
                return rounds
            print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def determine_winner(player_total, bot_total):
    """Return the winner for a round using standard blackjack rules."""
    if player_total > 21 and bot_total > 21:
        return "draw"
    if player_total > 21:
        return "bot"
    if bot_total > 21:
        return "player"
    if player_total > bot_total:
        return "player"
    if bot_total > player_total:
        return "bot"
    return "draw"


def play_round(round_number, difficulty):
    """Play one full blackjack round and return the round result."""
    # Each round gets a brand new shuffled deck to keep the game fair and simple.
    deck = Deck()
    player_hand = [deck.draw(), deck.draw()]
    bot_hand = [deck.draw(), deck.draw()]

    player_total = calculate_hand_value(player_hand)
    bot_total = calculate_hand_value(bot_hand)

    print_round_header(round_number)
    print(f"Bot difficulty: {difficulty.upper()}")
    print(f"Bot hand: {display_hand(bot_hand, hide_first=True)}")
    print(f"Your hand: {display_hand(player_hand)} (total: {player_total})")

    while True:
        action = input("Hit or stand? (h/s): ").strip().lower()

        if action in {"h", "hit"}:
            player_hand.append(deck.draw())
            player_total = calculate_hand_value(player_hand)
            print(f"Your hand: {display_hand(player_hand)} (total: {player_total})")

            if player_total > 21:
                print("You busted! The bot wins this round.")
                print(f"Bot final hand: {display_hand(bot_hand)} (total: {bot_total})")
                return "bot"
        elif action in {"s", "stand"}:
            break
        else:
            print("Invalid input. Please choose h or s.")

    # Reveal the bot's hidden card and finish the bot's turn according to difficulty.
    print(f"Bot reveals: {display_hand(bot_hand)} (total: {bot_total})")
    bot_turn(bot_hand, deck, difficulty)
    bot_total = calculate_hand_value(bot_hand)
    print(f"Bot final hand: {display_hand(bot_hand)} (total: {bot_total})")

    winner = determine_winner(player_total, bot_total)
    if winner == "player":
        print("You win!")
    elif winner == "bot":
        print("The bot wins!")
    else:
        print("It's a draw!")

    return winner


def main():
    """Run the entire blackjack session: one difficulty choice, one round count prompt,
    then play the requested number of rounds and report the final score.
    """
    print("Welcome to Blackjack! You play against a bot.")
    print("Try to get as close to 21 as possible without going over.")

    # Ask each of these only once per program run.
    difficulty = choose_difficulty()
    total_rounds = ask_round_count()

    player_wins = 0
    bot_wins = 0
    draws = 0

    for round_number in range(1, total_rounds + 1):
        winner = play_round(round_number, difficulty)
        if winner == "player":
            player_wins += 1
        elif winner == "bot":
            bot_wins += 1
        else:
            draws += 1

    print(f"\nFinal score: You {player_wins} - {bot_wins} Bot | Draws: {draws}")
    print("Thanks for playing! Goodbye!")


if __name__ == "__main__":
    main()
