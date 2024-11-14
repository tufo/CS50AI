
from tictactoe import *

# Board in progress
board =  [[X, O, EMPTY],
          [O, X, EMPTY],
          [X, EMPTY, EMPTY]]

board =  [[X, O, EMPTY],
            [X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

board =  [[X, O, O],
          [O, X, X],
          [X, O, EMPTY]]

output = minimax(board)
print(output)

