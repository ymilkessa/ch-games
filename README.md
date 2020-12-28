# ch-games
Python based implementations of checkers and chess

## Overview

This repository contains console-based versions of the games chess and checkers. You can play either game in three general ways: human-human (where you play on both sides or play with another person), human-computer (where you play against the computer) and computer-computer (when you make the computer play against itself).
There are three ways in which the computer can play the game. The first is `random`; in this mode, the computer selects a move at random from among all of its possible moves. The second mode is `simple`, where the computer picks a move that gives it the largest gain in points. The third is `minimax#`; this runs a minimax algorithm to extimate the most optimal move. In the command line arguments, the # is replaced by an integer with represents the depths of the minimax search. That is, if you want the computer to do a minimax search going until the next 3 turns, you would enter `minimax3` in the run command (see example below).

## Instructions

1. Clone this repository
2. Go into the main folder: `cd ch-games`
3. Enter a run command in this format: `python3 main.py <game-type> <player1> <player2> <size> <history>

For `<game-type>`, you should write either `chess` or `checkers`.
For `<player1>`, write one of `human`, `simple`, `random` or `minimax#` (where # is replaced by an integer). Do the same for `<player2>`. Player1 plays the **white** pieces while player2 plays the **black** pieces.

`<size>` corresponds to the number of rows or columns on the board. It has the default value of 8. You can only enter a different number for checkers; the chess board is always 8X8.

For `<history>`, just enter `history` if you want undo/redo options after each turn. Otherwise, skip this argument.

## Example

Here is how you play chess against an AI player that does a minimax search down to the next 3 turns: (This is also enabling the undo/redo features.)
```
python3 main.py chess human minimax3 8 history
```
