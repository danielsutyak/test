# Blackjack Project

This folder contains a simple terminal-based blackjack game against a bot.

## Quick start

Run the game from the project root:

```bash
python .\test\blackjack_game.py
```

## User guide

1. Start the game.
2. Choose a bot difficulty: easy, medium, or hard.
3. Enter how many rounds you want to play in this session.
4. On each round, type `h` to hit or `s` to stand.
5. Try to get as close to 21 as possible without going over.
6. After the final round, the program shows the total score.

### Blackjack rules

- Number cards are worth their face value.
- Face cards (J, Q, K) are worth 10.
- An Ace counts as 11 unless the hand would bust, in which case it counts as 1.
- If your total is over 21, you lose the round.
- The bot plays automatically using its selected difficulty level.

## Developer guide

### File structure

- `blackjack_game.py` – main game logic and session flow
- `README.md` – quick project overview and guides
- `Generate a blackjack-programm in python!.md` – alternate notes or task description

### Main logic overview

- `calculate_hand_value` handles Ace adjustment and total scoring.
- `Deck` creates and draws cards from a shuffled deck.
- `display_hand` formats visible cards and hides the bot's first card.
- `bot_turn` applies the difficulty-based AI behavior.
- `play_round` runs one complete table round.
- `main` controls session setup and totals across multiple rounds.

### Difficulty behavior

- Easy: stops at 18+, otherwise hits with a moderate chance.
- Medium: hits until reaching 17.
- Hard: more aggressive, especially at low totals.

### Useful maintenance ideas

- Add a betting system or money balance.
- Improve the bot with a more strategic decision model.
- Add a splash screen or ASCII card art.
- Split or double-down rules could be added later.

## Related guides

- [blackjack_user_guide.md](blackjack_user_guide.md)
- [blackjack_developer_guide.md](blackjack_developer_guide.md)

