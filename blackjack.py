"""
blackjack.py
Command-line interface for playing a single-player Blackjack game.

This file handles user interaction (input/output) and imports the
game primitives from `blackjack_core.py` so the core logic stays testable
and importable.
"""

from blackjack_core import Deck, score_hand, fmt_hand, bot_decision


def player_turn(deck, player_hand):
    """Run the player's turn loop until they stand or bust.

    Prompts the user to 'hit' or 'stand'. Returns the final numeric total.
    """
    while True:
        total = score_hand(player_hand)
        print(f"Your hand: {fmt_hand(player_hand)} (Total: {total})")
        if total > 21:
            print("You busted!")
            return total
        choice = input("Hit or stand? (h/s): ").strip().lower()
        if choice.startswith('h'):
            card = deck.draw()
            player_hand.append(card)
            print(f"You drew: {card[0]} of {card[1]}")
            continue
        else:
            return total


def play_round(difficulty):
    """Play a single round: deal, run player then bot, compare results."""
    deck = Deck()
    player_hand = [deck.draw(), deck.draw()]
    bot_hand = [deck.draw(), deck.draw()]

    # Show the dealer's up-card only
    print(f"Dealer shows: {bot_hand[0][0]} of {bot_hand[0][1]}")

    player_total = player_turn(deck, player_hand)
    if player_total > 21:
        print("Dealer wins this round.")
        return

    # Dealer (bot) plays using `bot_decision` strategy until it stands or busts
    while True:
        bot_total = score_hand(bot_hand)
        print(f"Dealer hand: {fmt_hand(bot_hand)} (Total: {bot_total})")
        if bot_total > 21:
            print("Dealer busted — you win!")
            return
        decision = bot_decision(bot_hand, player_hand[0][0], difficulty)
        if decision == 'hit':
            card = deck.draw()
            bot_hand.append(card)
            print(f"Dealer draws: {card[0]} of {card[1]}")
            continue
        else:
            break

    # Final comparison and result messaging
    bot_total = score_hand(bot_hand)
    print(f"Final — You: {player_total}, Dealer: {bot_total}")
    if bot_total > 21 or player_total > bot_total:
        print("You win!")
    elif player_total < bot_total:
        print("Dealer wins!")
    else:
        print("Push (tie).")


def choose_difficulty():
    """Prompt the user to pick a bot difficulty.

    Returns one of 'easy', 'medium', 'hard'. Default is 'medium'.
    """
    while True:
        diff = input("Choose bot difficulty (easy/medium/hard) [medium]: ").strip().lower()
        if diff == '':
            return 'medium'
        if diff in ('easy', 'medium', 'hard'):
            return diff
        print("Invalid choice — please type easy, medium, or hard.")


def main():
    """Main CLI entrypoint. Repeats rounds until the user quits."""
    print("Welcome to Blackjack — play against the dealer bot!")
    difficulty = choose_difficulty()
    print(f"Using difficulty: {difficulty}")
    while True:
        play_round(difficulty)
        again = input("Play another round? (y/n) ").strip().lower()
        if not again.startswith('y'):
            print("Thanks for playing!")
            break


if __name__ == '__main__':
    main()
