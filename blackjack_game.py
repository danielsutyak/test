"""Blackjack terminal game: one human player versus a bot.

The game asks for the bot difficulty once at the start of the session, then asks
how many rounds the player wants to play. Each round uses a fresh shuffled deck.
At the end, the script prints a session summary with player wins, bot wins, and draws.
"""

import time

from blackjack_core import Deck, bot_turn, calculate_hand_value, determine_winner
from blackjack_ui import clear_terminal, colorize, format_hand, print_round_header, print_session_summary


def display_hand(hand, hide_first=False):
    """Return a readable single-line string for hand output."""
    if not hand:
        return "[]"

    if hide_first:
        shown = ["[hidden]"] + [f"{rank}{suit}" for rank, suit in hand[1:]]
        return " ".join(shown)

    return " ".join(f"{rank}{suit}" for rank, suit in hand)


def choose_difficulty():
    """Prompt the user once for the bot difficulty and return the selected level."""
    print(colorize("Choose bot difficulty:", "green"))
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


def play_round(round_number, difficulty):
    """Play one full blackjack round and return the round result."""
    deck = Deck()
    player_hand = [deck.draw(), deck.draw()]
    bot_hand = [deck.draw(), deck.draw()]

    player_total = calculate_hand_value(player_hand)
    bot_total = calculate_hand_value(bot_hand)

    print_round_header(round_number)
    print(f"Bot difficulty: {difficulty.upper()}")
    print(f"Bot hand:\n{format_hand(bot_hand, hide_first=True)}")
    print(f"Your hand:\n{format_hand(player_hand)} (total: {player_total})")

    while True:
        action = input("Hit or stand? (h/s): ").strip().lower()

        if action in {"h", "hit"}:
            player_hand.append(deck.draw())
            player_total = calculate_hand_value(player_hand)
            print(f"Your hand:\n{format_hand(player_hand)} (total: {player_total})")

            if player_total > 21:
                print("You busted! The bot wins this round.")
                print(f"Bot final hand:\n{format_hand(bot_hand)} (total: {bot_total})")
                return "bot"
        elif action in {"s", "stand"}:
            break
        else:
            print("Invalid input. Please choose h or s.")

    print(f"Bot reveals:\n{format_hand(bot_hand)} (total: {bot_total})")
    bot_turn(bot_hand, deck, difficulty, dealer_upcard=player_hand[0])
    bot_total = calculate_hand_value(bot_hand)
    print(f"Bot final hand:\n{format_hand(bot_hand)} (total: {bot_total})")

    winner = determine_winner(player_total, bot_total)
    if winner == "player":
        print("You win!")
    elif winner == "bot":
        print("The bot wins!")
    else:
        print("It's a draw!")

    return winner


def main():
    """Run the entire blackjack session."""
    clear_terminal()
    print(colorize("Welcome to Blackjack! You play against a bot.", "magenta"))
    print("Try to get as close to 21 as possible without going over.")

    difficulty = choose_difficulty()
    total_rounds = ask_round_count()

    player_wins = 0
    bot_wins = 0
    draws = 0

    for round_number in range(1, total_rounds + 1):
        clear_terminal()
        winner = play_round(round_number, difficulty)
        if winner == "player":
            player_wins += 1
        elif winner == "bot":
            bot_wins += 1
        else:
            draws += 1

        if round_number < total_rounds:
            print("\nRound result displayed. Next round starts in 5 seconds...")
            time.sleep(5)

    print_session_summary(player_wins, bot_wins, draws)


if __name__ == "__main__":
    main()
