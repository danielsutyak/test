"""Core rules and state for the blackjack game."""

import random

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
    """Return the numeric value for a single card rank."""
    return CARD_VALUES[card_rank]


def calculate_hand_value(hand):
    """Compute the total for a hand while preserving legal Ace values."""
    total = 0
    aces = 0

    for rank, _ in hand:
        total += get_card_value(rank)
        if rank == "A":
            aces += 1

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


class Deck:
    """A shuffled deck that can be drawn from repeatedly."""

    def __init__(self):
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        """Return a card and reshuffle if the deck runs out."""
        if not self.cards:
            self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
            random.shuffle(self.cards)
        return self.cards.pop()


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


def basic_strategy_decision(hand, dealer_upcard):
    """Return a simple basic-strategy action using the visible dealer card."""
    total = calculate_hand_value(hand)
    if dealer_upcard is None:
        return "hit" if total < 17 else "stand"

    if isinstance(dealer_upcard, tuple):
        dealer_rank = dealer_upcard[0]
    else:
        dealer_rank = dealer_upcard

    if dealer_rank in {"J", "Q", "K"}:
        dealer_value = 10
    elif dealer_rank == "A":
        dealer_value = 11
    else:
        dealer_value = int(dealer_rank)

    soft_total = any(rank == "A" for rank, _ in hand) and total <= 21 and total >= 12

    if total > 21:
        return "stand"

    if soft_total:
        if total >= 19:
            return "stand"
        if total in {13, 14, 15, 16, 17, 18}:
            return "stand" if dealer_value in {2, 3, 4, 5, 6} else "hit"
        return "hit"

    if total >= 17:
        return "stand"

    if total in {13, 14, 15, 16}:
        return "stand" if dealer_value in {2, 3, 4, 5, 6} else "hit"

    if total == 12:
        return "stand" if dealer_value in {4, 5, 6} else "hit"

    if total == 11:
        return "hit"

    if total == 10:
        return "hit" if dealer_value in {10, 11} else "hit"

    return "hit"


def bot_turn(bot_hand, deck, difficulty, dealer_upcard=None):
    """Let the bot decide whether to hit or stand by difficulty."""
    bot_total = calculate_hand_value(bot_hand)

    while True:
        if bot_total > 21:
            return

        if difficulty == "easy":
            if bot_total >= 18:
                return
            if random.random() < 0.55:
                bot_hand.append(deck.draw())
                bot_total = calculate_hand_value(bot_hand)
                continue
            return

        if difficulty == "medium":
            if bot_total >= 17:
                return
            bot_hand.append(deck.draw())
            bot_total = calculate_hand_value(bot_hand)
            continue

        if difficulty == "hard":
            if dealer_upcard is not None:
                decision = basic_strategy_decision(bot_hand, dealer_upcard)
                if decision == "stand":
                    return
                bot_hand.append(deck.draw())
                bot_total = calculate_hand_value(bot_hand)
                continue

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

        return
