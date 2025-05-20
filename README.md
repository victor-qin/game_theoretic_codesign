## Game Theoretic Co-Design

This repository contains code testing generating example DPIs that have profit wires. The profit wires are independent, in that each player's reward depends only on their implementation. `compare_solvers` shows experimentally that the solutions from the profit-only DPI `FFMR_p` are Nash equilbria (thought not all Nash equilibria if there are non-admissable equilibria) and a superset of the admissable equilibria. The major modification needed to `FFMR_p` is for MCDP to return implementation instead of just the output of the Pareto point - with that, we can make an argument that `FFMR_p` finds all Nash equilibria under independence assumptions.

The player DPIs are in `player_1.mcdp` and `player_2.mcdp`, and are strung together in `system.mcdp`. The profit wires are positive numbers, but should be interpreted as `10 - profit = invprofit`. `matrix_game.py` translates the game and solves using best response.


### Cournot Game

`\cournot_operations` sets up and tests a Cournot game.