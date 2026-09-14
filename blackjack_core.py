"""
blackjack_core.py
Core Blackjack utilities: Deck, scoring, formatting, and bot decision logic.

This module contains the pure game logic so the CLI can import and use
these functions/classes without dealing with implementation details.
"""

import random


class Deck:
    """A shuffled deck of standard playing cards.

    Cards are represented as (rank, suit) tuples where rank is a string
    like 'A', 'K', '10', '2', etc. The deck auto-rebuilds when exhausted.
    """

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """Populate and shuffle the deck with 52 cards."""
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for s in suits:
            for r in ranks:
                self.cards.append((r, s))
        random.shuffle(self.cards)

    def draw(self):
        """Draw a card from the deck, rebuilding if necessary."""
        if not self.cards:
            self.build()
        return self.cards.pop()


def card_value(rank):
    """Return the blackjack nominal value for a rank.

    Face cards are worth 10, Aces are initially 11 (adjusted later by scoring).
    """
    if rank in ['J', 'Q', 'K']:
        return 10
    if rank == 'A':
        return 11
    return int(rank)


def score_hand(hand):
    """Compute the best blackjack score for a hand, handling Aces as 1 or 11.

    The routine sums values treating Aces as 11, then reduces them to 1
    as needed to avoid busting.
    """
    total = 0
    aces = 0
    for r, _ in hand:
        val = card_value(r)
        total += val
        if r == 'A':
            aces += 1
    while total > 21 and aces:
        # convert an Ace from 11 to 1
        total -= 10
        aces -= 1
    return total


def fmt_hand(hand):
    """Return a human-friendly string representation of a hand."""
    return ', '.join([f"{r} of {s}" for r, s in hand])


def bot_decision(bot_hand, player_visible_card_rank, difficulty):
    """Decide whether the dealer bot should 'hit' or 'stand'.

    difficulty controls strategy:
    - 'easy': random-ish, more likely to hit
    - 'medium': dealer-like, hits until 17
    - 'hard': heuristic considering player's visible card
    """
    total = score_hand(bot_hand)

    if difficulty == 'easy':
        # Hit more often on low totals; occasionally hit on borderline totals.
        if total < 16:
            return 'hit'
        if total < 19 and random.random() < 0.4:
            return 'hit'
        return 'stand'

    if difficulty == 'medium':
        # Classic dealer rule: hit until reaching soft/hard 17.
        if total < 17:
            return 'hit'
        return 'stand'

    if difficulty == 'hard':
        # Aggressive heuristic: hit on low totals, consider player's visible card
        if total <= 11:
            return 'hit'
        if 12 <= total <= 16:
            try:
                player_val = card_value(player_visible_card_rank)
            except Exception:
                player_val = 10
            # If player shows a strong card, be more aggressive.
            if player_val >= 7:
                return 'hit'
            return 'stand'
        return 'stand'

    # Fallback (behave like medium)
    if total < 17:
        return 'hit'
    return 'stand'
