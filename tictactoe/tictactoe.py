"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_cnt = 0
    O_cnt = 0

    for n in range(int(len(board))):
        for m in range(int(len(board[n]))):
            if board[n][m] == "X":
                X_cnt += 1
            if board[n][m] == "O":
                O_cnt += 1
        # if board is empty or if same number of Xs as Os.
    if X_cnt == 0 or X_cnt == O_cnt:
        next_turn = "X"
    elif X_cnt - O_cnt == 1:
        next_turn = "O"
    else:
        next_turn = "someone took too many turns."
    return next_turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(int(len(board))):
        for j in range(int(len(board[i]))):
            if board[i][j] == None: # if the spot is available, keep track of its coordinates.
                coordinates = (i,j)
                actions.add(coordinates)

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    action = (1,1)
    (i,j) = action

    # Copy the board state
    board_result = board

    # attempt to update the board by marking it at the prescribed action coordinates.

    # if it is X's turn, assing marking to be X.
    if player(board) == "X":
        marking = "X"
    else: # if it is O's turn
        marking = "O"

    if board_result[i][j] == None:
        board_result[i][j] = marking
    else: # if that coordinate is already filled, raise an error
        board_result = "that spot is already occupied."

    #print(board_result)
    return board_result



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    Empty_cnt = 0
    for n in range(int(len(board))):
        for m in range(int(len(board[n]))):
            if board[n][m] == None:
                Empty_cnt += 1
    if Empty_cnt == 0:
        print(True)
        #return True # game is over
    else:
        print(False)        
        #return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    return utility


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
