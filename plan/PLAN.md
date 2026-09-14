Blackjack Project Plan
======================

Objective: Implement a single-player Blackjack game in Python where a human plays against a bot with changeable difficulties. The player can play rounds until they choose to stop.

Planned steps:

1. Implement core game logic: deck, dealing, hand scoring (Aces as 1/11).
2. Implement player actions: hit, stand.
3. Implement bot with adjustable difficulties: easy, medium, hard.
4. Add a CLI loop to play multiple rounds until the user quits.
5. Add a short README with run instructions.

Notes:

- Bot difficulties:
  - easy: mostly random / hits more often.
  - medium: dealer-like (hits until 17).
  - hard: simple heuristic based on player's visible card.
