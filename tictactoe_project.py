"""
This is a simple CUI tic tac toe game against an AI program
which can play ideally, i.e., can never be beaten. It can only
draw or win. There are 3 difficulty settings - easy, in which
the AI will behave erratically 25% of the time, normal, in
which it will behave erratically 10% of the time, and hard,
which will always make the ideal move.
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = " "

''''''


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    Xcount = 0
    Ocount = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == "X":
                Xcount += 1
            elif board[i][j] == "O":
                Ocount += 1
    if Xcount == Ocount:
        return X
    else:
        return O


def actions(board):
    possibleactions = []
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                possible_action = (i, j)
                possibleactions.append(possible_action)
    return possibleactions


def result(board, action):
    new_board = copy.deepcopy(board)
    playersymbol = player(new_board)
    if action is None:
        raise Exception("ActionIsNone")
    if new_board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = playersymbol
    return new_board


def winner(board):
    reward = utility(board)
    if reward == 1:
        return X
    elif reward == -1:
        return O
    else:
        return None


def terminal(board):
    filled = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] != EMPTY:
                filled += 1
    if filled == 9:
        return True
    for i in range(0, 3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return True
        elif board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return True
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return True
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return True
    return False


def utility(board):
    if terminal(board):
        for i in range(0, 3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] == X:
                return 1
            elif board[0][i] == board[1][i] == board[2][i] and board[0][i] == X:
                return 1
            elif board[i][0] == board[i][1] == board[i][2] and board[i][0] == 0:
                return -1
            elif board[0][i] == board[1][i] == board[2][i] and board[0][i] == 0:
                return -1
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] == X:
            return 1
        elif board[0][2] == board[1][1] == board[2][0] and board[0][2] == X:
            return 1
        elif board[0][0] == board[1][1] == board[2][2] and board[0][0] == O:
            return -1
        elif board[0][2] == board[1][1] == board[2][0] and board[0][2] == O:
            return -1
        return 0


def minimax(board):
    if terminal(board):
        return None
    optimalaction = None
    if random.random() < chance:
        optimalaction = random.choice(actions(board))
        return optimalaction
    else:
        if player(board) == X:
            bestval = -math.inf
            for act in actions(board):
                value = minval(result(board, act))
                if bestval < value:
                    bestval = value
                    optimalaction = act
            return optimalaction
        elif player(board) == O:
            bestval = math.inf
            for act in actions(board):
                value = maxval(result(board, act))
                if bestval > value:
                    bestval = value
                    optimalaction = act
            return optimalaction


def maxval(board):
    if terminal(board):
        return utility(board)
    val = -math.inf
    for action in actions(board):
        val = max(val, minval(result(board, action)))
    return val


def minval(board):
    if terminal(board):
        return utility(board)
    val = math.inf
    for action in actions(board):
        val = min(val, maxval(result(board, action)))
    return val


def print_instructions():
    print("INSTRUCTIONS")
    print("The grid is of the form")
    print("|-----|-----|-----|")
    for i in range(0, 3):
        for j in range(0, 3):
            if j == 0:
                print("|", end="")
            print(f"({i},{j})", end="|")
            if j == 2:
                print()
                print("|-----|-----|-----|")
    print("When choosing your symbol, type in either X or O")
    print("Difficulty settings:")
    print("Easy: 25% chance of making a random move")
    print("Normal: 10% chance of making a random move")
    print("Hard: Literally unbeatable")
    print("To place your symbol, you must enter the coordinate where you wish to place your symbol.")
    print("Input must be given in the form x,y with no space or brackets")
    print("For example, if you wish to place your symbol in the middle, you must enter '1,1'")
    print("Example: ")
    print("Where would you like to place your O? 1,1")
    print("Make sure you DONOT place your symbol in an invalid state.")
    print("That's all. Have fun!")
    print()


def print_board(board):
    print("|---|---|---|")
    for i in range(0, 3):
        for j in range(0, 3):
            if j == 0:
                print("| ", end="")
            print(board[i][j], end=" | ")
            if j == 2:
                print()
                print("|---|---|---|")
    print()


def user_input(user):
    try:
        action = input(f"Where would you like to place your {user}? ").split(",")
        action = (int(action[0]), int(action[1]))
    except:
        print("Invalid expression, try again.")
        user_input(user)
    return action


if __name__ == '__main__':
    print_instructions()
    playing = True
    global chance
    chance = 0
    diff = int(input("Select difficulty level: Easy(1) | Normal(2) | Hard(3) : "))
    if diff == 1:
        chance = 0.25
    elif diff == 2:
        chance = 0.10
    elif diff == 3:
        chance = 0
    while playing:
        user = input("Would you like to be X or O? (X starts): ").upper()
        while user != X and user != O:
            print("Please choose a valid option:")
            user = input("Would you like to be X or O? (X starts): ").upper()
        if user == X:
            user_turn = True
            ai = O
        else:
            user_turn = False
            ai = X
        board = initial_state()
        gameover = False
        print("Game starts!")
        print()
        print_board(board)
        print()
        while not gameover:
            if not user_turn:
                print("AI is thinking...")
                print()
                ai_action = minimax(board)
                board = result(board, ai_action)
                user_turn = True
                gameover = terminal(board)
            elif user_turn:
                action = user_input(user)
                '''while action not in actions(board):
                    print("Invalid action! Try again:")
                    action = user_input(user)'''
                board = result(board, action)
                user_turn = False
                gameover = terminal(board)
                print()
            print_board(board)
        if winner(board) == X:
            print("X is the winner!")
        elif winner(board) == O:
            print("O is the winner!")
        else:
            print("Well played, it is a draw!")
        again = input("Would you like to play again? (Y/N): ").upper()
        while again != "Y" and again != "N":
            again = input("Would you like to play again? (Y/N): ").upper()
        if again == "Y":
            playing = True
        else:
            playing = False