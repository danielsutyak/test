# Blackjack User Guide

## Goal

The goal of the game is to get as close to 21 as possible without going over. You play against a bot that chooses its actions based on the difficulty level you select.

## How to play

1. Run the game with Python.
2. Choose a bot difficulty.
3. Enter the number of rounds you want to play.
4. On each round, type `h` to hit or `s` to stand.
5. After all rounds, the game shows your final score.

## Difficulty levels

- Easy: more forgiving and less aggressive.
- Medium: balanced difficulty.
- Hard: more aggressive and risk-taking.

## Rules

- Number cards count as their value.
- J, Q, and K count as 10.
- Ace counts as 11 unless that would make the total exceed 21, in which case it counts as 1.
- If your total goes over 21, you lose the round.
- If the bot exceeds 21, you win the round.
- If both totals are equal, the round is a draw.

## Tips

- Try to stay around 17 to 20 for a strong hand.
- Be careful with low totals when the bot is hard mode.
- The game is session-based, so all rounds use the same chosen difficulty.
