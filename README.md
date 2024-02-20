# Python-Arcade
  
  
 This repository will gather a few Python games coded in Pygame, this will first contain a rudimentary Chess game and will increase in diversity overtime.


## CHESS
[![wakatime](https://wakatime.com/badge/user/d1fb42e6-38e1-489b-a7b0-fa05747ea94a/project/b22950de-2dcd-4cbf-8e57-2cf629725789.svg)](https://wakatime.com/badge/user/d1fb42e6-38e1-489b-a7b0-fa05747ea94a/project/b22950de-2dcd-4cbf-8e57-2cf629725789)

This project came from the proposition from a C++ professor to create an entire chess interface on which the player could play against a friend on the same screen as well as play against a computer player (basic AI). As for the game current state, apart from the basic moves for each piece, board displaying and basic game management, the check mate and pat state are not yet applied. I was able to add the "pion en passant", the "castle" and "nailing" of pieces.

This check-mate mechanic will be the main focus of the future addition to this program, finally making the game finishable.

### The basic board :
![image](https://user-images.githubusercontent.com/80796115/142261275-e86ab50a-b506-4a3a-9aac-1c8b953e7f44.png)

### Making a Move :

![image](https://user-images.githubusercontent.com/80796115/142261526-856c4567-a953-44c2-841a-9eb6d2fecb52.png)

### Future additions:

- **Check and Mate mechanics** : the possibility of a "pat" (player not beingable tomove while not being threatened) or "mat" (same as pat but the king is threatened).

- **Basic Tree based AI** : Adding a basic tree-based AI and a "best move" and "mistakes" post-analysis.

- **Record past moves for replay ability** : Add a box in the GUI reording past moves as well as making the last move visible on the board.

- **Basic UI components** : Label indicating whose turn it is, Abandoning or Nulle proposal buttons

- **Saves System** : Creating a saves system to continue an interesting game at a later date

- **Custom Board Creation** : Adding the ability of creating custom boards for puzzles and challenges.
