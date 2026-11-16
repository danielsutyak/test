import pathlib
import re
import sys
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import blackjack_ui
from blackjack_core import Deck, basic_strategy_decision, calculate_hand_value, determine_winner
from blackjack_ui import clear_terminal, format_hand, render_card


class BlackjackModuleTests(unittest.TestCase):
    def test_calculate_hand_value_handles_aces(self):
        hand = [("A", "♠"), ("9", "♥"), ("A", "♦")]
        self.assertEqual(calculate_hand_value(hand), 21)

    def test_determine_winner_treats_bust_as_loss(self):
        self.assertEqual(determine_winner(22, 18), "bot")
        self.assertEqual(determine_winner(18, 22), "player")

    def test_format_hand_renders_cards(self):
        hand = [("K", "♥"), ("A", "♠")]
        rendered = format_hand(hand)
        self.assertIn("K", rendered)
        self.assertIn("A", rendered)

    def test_render_card_uses_consistent_block_width(self):
        with patch.object(blackjack_ui, "supports_color", return_value=False):
            block = render_card(("K", "♣"))
        self.assertEqual(block, ["┌──────┐", "│  K♣  │", "└──────┘"])

    def test_render_card_stays_aligned_when_colorized(self):
        with patch.object(blackjack_ui, "supports_color", return_value=True):
            block = render_card(("3", "♠"))
        cleaned = re.sub(r"\x1b\[[0-9;]*m", "", block[1])
        self.assertEqual(cleaned, "│  3♠  │")

    def test_basic_strategy_decision_uses_dealer_card(self):
        self.assertEqual(basic_strategy_decision([("10", "♠"), ("6", "♥")], "6"), "stand")
        self.assertEqual(basic_strategy_decision([("10", "♠"), ("4", "♥")], "10"), "hit")

    def test_clear_terminal_uses_platform_command(self):
        with patch.object(blackjack_ui.os, "name", "nt"), patch.object(blackjack_ui.os, "system") as mock_system:
            clear_terminal()
        mock_system.assert_called_once_with("cls")

    def test_deck_has_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)


if __name__ == "__main__":
    unittest.main()
