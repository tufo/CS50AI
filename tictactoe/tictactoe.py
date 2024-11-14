"""
Tic Tac Toe Player
"""

##############
# Test cases
"""
# X win by row
board =  [[X, X, X],
          [O, X, O],
          [O, O, X]]

# X win by col
board =  [[O, O, X],
          [O, X, X],
          [X, O, X]]

# X win by diag0
board =  [[O, O, X],
          [X, X, O],
          [X, O, X]]

# X win by diag1
board =  [[X, O, O],
          [O, X, O],
          [X, O, X]]

# X win by col & diag0
board =  [[X, O, X],
          [X, X, O],
          [X, O, O]]

# X win by diag0 with incomplete board.
board =  [[X, O, X],
          [EMPTY, X, O],
          [X, O, O]]

# No winner: a tie
board =  [[X, O, O],
          [O, X, X],
          [X, O, O]]

"""
##############

import math
import copy

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
        raise NameError('someone took too many turns.')
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
    coord = []
    for coordinate in action:
        coord.append(coordinate)

    i = coord[0]
    j = coord[1]

    if i <0 or i>2 or j<0 or j>2:
        raise NameError('Coordinates are out of bounds.')


    # Copy the board state
    #board_result = board
    board_result = copy.deepcopy(board) # using deep copy was important.

    # attempt to update the board by marking it at the prescribed action coordinates.

    # if it is X's turn, assign marking to be X.
    if player(board) == "X":
        marking = "X"
    elif player(board) == "O": # if it is O's turn
        marking = "O"
    #else:

    if board_result[i][j] == None:
        board_result[i][j] = marking
    else: # if that coordinate is already filled, raise an error
        raise NameError('that spot is already occupied.')

    return board_result

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None # start by assuming no one has won yet.

    # Scan through the board and write the coordinates for player X and player O
    X_coords = []
    O_coords = []

    for i in range(int(len(board))):
        for j in range(int(len(board))):

            # remember that you can still win with empty spots on the board.
            marking = board[i][j]
            if marking == "X":
                X_coords.append([i,j])
            elif marking == "O":
                O_coords.append([i,j])

    # start by checking if Player X has won.
    players_checked_iterations = 0
    player_coords = X_coords
    Player = "X"

    while winner == None and players_checked_iterations < 2: # loop through Player X, then Player O

        # ROWS: winning by means of rows
        # extract out the i & j coordinates.
        i_inds = []
        j_inds = []

        for d in range(int(len(player_coords))):
            i_inds.append(player_coords[d][0]) # i indices
            j_inds.append(player_coords[d][1]) # j indices

        # Analyze the coords for each player to see if either player has won.
        target_cnt = 3

        # scan through the list of coords to find out if any coordinate occurs (target_cnt = 3) times, which would indicate a win by rows.
        for value in i_inds:
            if i_inds.count(value) == target_cnt: # checking within i indices to indicate win by rows.
                #key_value = value # the number that occurs (target_cnt = 3) times.
                winner = Player
                return winner
            if j_inds.count(value) == target_cnt: # checking within j indices to indicate win by cols.
                #key_value = value # the number that occurs (target_cnt = 3) times.
                winner = Player
                return winner

        # DIAGS: if we didn't find a winner by means of rows in the previous logic, then run this code, then check for win by means of diags.
        if winner == None:
            diag0_coords = [[0,2],[1,1],[2,0]] # 1st option of coordinates needed to win diagonally.
            diag1_coords = [[0,0],[1,1],[2,2]] # 2nd option of coordinates needed to win diagonally.

            diag_coords = diag0_coords # start by assigning and checking the 1st option.

            diag_check_iterations = 0 # keeps track of whether we have checked both diagonally winning configs.

            while diag_check_iterations <2:
                cond = [] # a bucket to hold list of booleans.

                for n in range(int(len(diag1_coords))):
                    cond.append(diag_coords[n] in player_coords) # take each coordinate set in diag1_coords and display Bools to show if they are within X_coords.
                
                if all(cond): # if all the booleans within cond are true, then the player won diagonally.
                    winner = Player
                    return winner
                
                else: # if they haven't won yet, check if they won diagonally via diag2.
                    diag_check_iterations += 1
                    diag_coords = diag1_coords # assign diag2_coords to diag_coords

        # repeat check for other player.

        players_checked_iterations += 1
        player_coords = O_coords
        Player = "O"


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if there is a winner
    the_winner = winner(board)

    if the_winner != None: # if there is a winner
        return True

    # If there is no winner, check if the board is full yet. the board does not have to be full for the game to be over.
    Empty_cnt = 0
    for n in range(int(len(board))):
        for m in range(int(len(board[n]))):
            if board[n][m] == None:
                Empty_cnt += 1
    if Empty_cnt == 0:
        return True # game is over
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    accepts a TERMINAL board as input
    """

    the_winner = winner(board) # call on the winner() function

    if the_winner == "X":
        the_utility = 1
    elif the_winner == "O":
        the_utility = -1
    elif the_winner == None:
        the_utility = 0
    return the_utility

def minimax_alg(board):
    # winner() is already called within terminal() & utility()

    # base case: if the game is in the terminal state, return its utility
    boolean = terminal(board)
    #print(boolean)
    if boolean:
        current_utility = utility(board)
        current_action = None
        #print(current_utility)
        #print(current_action)
        return current_action, current_utility
    
    # if the game is not over, then continue.
    # initialize the utility value to give the algorithm something to compare to.
    
    current_player = player(board) # tell the generic variable who the current player is.
    current_utility = ""
    best_action = "" # initialize variable to hold the best_action.
    
    if current_player == "X":
        current_utility = float('-inf') # NEGATIVE INFINITY for Player X. -Inf only gets used in the 1st iteration of the following for loop.

        for action in actions(board): # generate a list of possible actions, iterate through each action in the list of actions.
            #print("X ACTION")
            #print(action)
            # compare this iteration of utility to see which one to pick.
            (downstream_action, downstream_utility) = minimax_alg(result(board, action)) # write the downstream utility value.
            #print("XXXXX DOWNSTREAM UTILITY")
            #print(downstream_utility)
            if current_utility < downstream_utility:
                current_utility = downstream_utility # overwrite current utility if the downstream one is better.
                best_action = action # overwrite the best_action with this iteration's for loop action.

    if current_player == "O":
        current_utility = float('inf') # NEGATIVE INFINITY for Player X. -Inf only gets used in the 1st iteration of the following for loop.

        for action in actions(board): # generate a list of possible actions, iterate through each action in the list of actions.

            # compare this iteration of utility to see which one to pick.
            (downstream_action, downstream_utility) = minimax_alg(result(board, action)) # write the downstream utility value.
            
            if current_utility > downstream_utility:
                current_utility = downstream_utility # overwrite current utility if the downstream one is better.
                best_action = action # overwrite the best_action with this iteration's for loop action.
    #print(best_action)
    #print(current_utility)
    return best_action, current_utility # return this iteration of the utility value to the upstream iteration of the function for comparison.


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    (best_action, current_utility) = minimax_alg(board)
    return best_action