# Isolation_narquie
My current version of Isolation (AI Nanodegree)

This is a project that I wrote / am writing for my AI Nanodegree class with Udacity.

The objective of the program is to win against an Alpha-Beta pruning opponent with a certain strategy (or heuristic) in Isolation, a game where chess-like knights attempt to block each other on a 7x7 board by removing parts of the board they landed on.
The heuristics that I developed are on par with this Alpha-Beta pruning opponent and is better at defeating less complex opponents as opposed to the Alpha-Beta pruning opponent.

The techniques I used were minimax, Alpha-Beta search, and iterative deepening. I constructed a heuristic which values locking opponents into disadvantageous positions rather than maximizing its own movements. 

The code cannot be run without the helper classes included... run tournament.py for results of the three heuristics I created against the Alpha-Beta pruning opponent.
