"""Display helpers for blackjack, including color and ASCII card art."""

import os
import re
import sys


def clear_terminal():
    """Clear the terminal window for a cleaner game display."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

RESET = "\033[0m"
COLORS = {
    "red": "\033[31m",
    "black": "\033[30m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "magenta": "\033[35m",
}


def supports_color():
    """Return True when ANSI style codes are likely supported."""
    return sys.stdout.isatty() or os.environ.get("TERM") is not None


def colorize(text, color_name):
    """Wrap text with ANSI escape codes if possible."""
    if not supports_color():
        return text
    color = COLORS.get(color_name, "")
    return f"{color}{text}{RESET}"


def suit_color(suit):
    """Choose a terminal color based on the card suit."""
    return "red" if suit in {"♥", "♦"} else "black"


def strip_ansi(text):
    """Remove ANSI escape codes so visible width can be measured correctly."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def center_visible(text, width):
    """Center text using the visible, non-ANSI length."""
    visible = len(strip_ansi(text))
    if visible >= width:
        return text

    padding = width - visible
    left = padding // 2
    right = padding - left
    return " " * left + text + " " * right


def render_card(card, hidden=False):
    """Render a single card as a small ASCII card block."""
    top = "┌──────┐"
    bottom = "└──────┘"

    if hidden:
        return [top, "│░░░░░░│", bottom]

    rank, suit = card
    color_name = suit_color(suit)
    content = f"{rank}{suit}"
    visible_content = colorize(content, color_name)
    inner = center_visible(visible_content, 6)
    middle = f"│{inner}│"
    return [top, middle, bottom]


def format_hand(hand, hide_first=False):
    """Return a multi-line ASCII representation of a hand."""
    if not hand:
        return "[]"

    blocks = []
    for index, card in enumerate(hand):
        if hide_first and index == 0:
            blocks.append(render_card(card, hidden=True))
        else:
            blocks.append(render_card(card))

    lines = ["" for _ in range(3)]
    for block in blocks:
        for idx, line in enumerate(block):
            lines[idx] += f"{line} "

    return "\n".join(line.rstrip() for line in lines)


def print_round_header(round_number):
    """Print a decorative separator and title for the round."""
    print("\n" + "=" * 30)
    print(colorize(f"Round {round_number}", "cyan"))
    print("=" * 30)


def print_session_summary(player_wins, bot_wins, draws):
    """Display a color-enhanced end-of-session summary."""
    print("\n" + "-" * 30)
    print(f"{colorize('Final score', 'green')}: You {player_wins} - {bot_wins} Bot | Draws: {draws}")
    print("Thanks for playing! Goodbye!")
