# Blackjack Developer Guide

## Project summary

This project is a console-based blackjack game written in Python. It uses no external libraries and is designed to be easy to read, modify, and extend.

## Main file

- `blackjack_game.py` contains the complete game logic.

## Core functions

### `get_card_value(card_rank)`
Returns the numeric value for a rank such as `2`, `J`, or `A`.

### `calculate_hand_value(hand)`
Totals a hand and adjusts Ace values so the total stays valid.

### `Deck`
Creates a shuffled 52-card deck and manages drawing cards.

### `display_hand(hand, hide_first=False)`
Formats a hand for terminal output. The optional hidden-card behavior is used for the bot.

### `bot_turn(bot_hand, deck, difficulty)`
Controls the bot's decision-making logic based on the difficulty selected at the start of the game.

### `play_round(round_number, difficulty)`
Runs one full round: deal cards, let the user act, reveal the bot, determine the winner, and print the result.

### `main()`
Set up session settings once, then run the requested number of rounds and print the final score summary.

## Difficulty design

The three difficulties are intentionally simple and readable:

- Easy: lower-risk behavior.
- Medium: fixed threshold strategy.
- Hard: more aggressive play and occasional risk-taking.

These behaviors are all implemented inside `bot_turn` so they are easy to adjust or replace.

## Suggested enhancements

- Add betting and bankroll management.
- Add split and double-down rules.
- Improve the bot with a more advanced strategy model.
- Add colored terminal output or ASCII card art.
- Refactor into multiple modules for cleaner separation.

## Verification

Run the script in a terminal and test the flow with sample input. A basic check looks like this:

```bash
python .\test\blackjack_game.py
```

Then provide:

- a difficulty choice
- a round count
- `h` or `s` inputs while playing

The output should show the session summary and final score after the selected number of rounds.
