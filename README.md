# parcheesi

## This is a work in progress

My aim is to create a Python (tkinter) version of the board game Parcheesi which can be played by up to 4 players (or have computer players filling the spaces) over a local network.

Rules I will implement:
Players have 4 tokens which start off in their start area. The aim is to move the tokens to the centre of the board, moving anti-clockwise along the outer track, until they reach the centre.

On their turn, a player rolls 2 dice and moves one or two of their tokens according to the numbers on the dice. They can move the same token for both numbers (in any order) or two different tokens for each number. if a token lands on an opponent's token, the token that was landed on is sent back to the start area.

The following extra rules apply:
1. A player must roll a 5 (either on a single die or as a total of two dice) before they can move a piece from the start onto the track.
2. If you roll a 5 and you have tokens in the start area, you *must* take one out.
3. If two tokens belonging to the same player land on the same place, a block is formed that opponents cannot cross.
4. Tokens that land on the marked "safe" places cannot be sent back.
5. Only tokens of the matching colour can go up the "home" path to the centre of the board.
6. If you roll a double, you can take a second turn.
7. However, if you roll three double in a row, the token closest to home (the centre) is returned to the start area and play moves to the next player.
8. When you send an opponent back to the start, you can move one of your tokens forward by 20 places.

