"""
This PGN reader works by reading a text (pgn) file of a chess game and displays it onto a GUI window with a board
and two buttons to navigate between positions. To read the PGN of the desired file, simply add the file name as a
variable and open that variable in line 52. Two sample games are included.

The program works by first charting out all positions, move by move, and adding each position to a list of positions
called states. In the GUI, two buttons navigate by incrementing or decrementing the state/position to be shown and
reflect the position onto the game board.

A position is saved as a dictionary with the coordinates of each of the 64 squares as keys and the piece on the
square as the value. If the square has no piece on it, it has a value of None.

The GUI draws a position by cross-matching the board coordinate with a certain (x,y) coordinate in the main window.
It then draws the required square and its piece, if any. The positions shown on the board are changed by
redrawing the board in its entirety.

Sections of code have their own comments and inline documentation.
"""

'''imports'''
import pygame
import copy
from pygame.locals import *

pygame.init()
pygame.font.init()

'''variable setup'''
white = (153, 153, 153)
black = (96, 64, 32)
piece_white = (255, 255, 255)
piece_black = (0, 0, 0)
lgreen = 144, 238, 144
dgreen = (0, 100, 0)
running = True
columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
rows = [1, 2, 3, 4, 5, 6, 7, 8]
rows.reverse()
size = 70
font = pygame.font.SysFont("segoeuisymbol", 10)
pfont = pygame.font.SysFont("segoeuisymbol", 50)
tfont = pygame.font.SysFont("segoeuisymbol", 35)
mfont = pygame.font.SysFont("segoeuisymbol", 20)
current_state = 0

# unicode for pieces
wking = "\u2654"
wqueen = "\u2655"
wrook = "\u2656"
wbishop = "\u2657"
wknight = "\u2658"
wpawn = "\u2659"

bking = "\u265A"
bqueen = "\u265B"
brook = "\u265C"
bbishop = "\u265D"
bknight = "\u265E"
bpawn = "\u265F"

rarrow = "\u2192"
larrow = "\u2190"

adityas_game = "yudirambutan2015_vs_adityapentyala_2022.01.07.pgn"
# https://www.chess.com/analysis/game/live/35291867113?tab=review

haaziqs_game = "bing-bang69_vs_bolo09_2022.01.08.pgn"
# https://www.chess.com/game/live/35404079313?username=bing-bang69

pgn_text = open(haaziqs_game).read()
moves = pgn_text.split()
for i in moves:
    if "." in i:
        moves.remove(i)

'''-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-'''

# board utilities
boardlist = []
for i in rows:
    row = []
    for j in columns:
        c = str(j) + str(i)
        row.append(c)
    boardlist.append(row)  # creates an 8x8 array of coordinates

coords = {}
initial_state = {}
states = []

for i in range(0, 8):
    for j in range(0, 8):
        coords[boardlist[i][j]] = (j * size + 10, i * size)
        initial_state[boardlist[i][j]] = None  # sets up board as a dictionary with empty squares

# initial setup with pieces
# white pawns
initial_state["A2"] = wpawn
initial_state["B2"] = wpawn
initial_state["C2"] = wpawn
initial_state["D2"] = wpawn
initial_state["E2"] = wpawn
initial_state["F2"] = wpawn
initial_state["G2"] = wpawn
initial_state["H2"] = wpawn

# black pawns
initial_state["A7"] = bpawn
initial_state["B7"] = bpawn
initial_state["C7"] = bpawn
initial_state["D7"] = bpawn
initial_state["E7"] = bpawn
initial_state["F7"] = bpawn
initial_state["G7"] = bpawn
initial_state["H7"] = bpawn

# white rooks
initial_state["A1"] = wrook
initial_state["H1"] = wrook

# black rooks
initial_state["A8"] = brook
initial_state["H8"] = brook

# white knights
initial_state["B1"] = wknight
initial_state["G1"] = wknight

# black knights
initial_state["B8"] = bknight
initial_state["G8"] = bknight

# white bishops
initial_state["C1"] = wbishop
initial_state["F1"] = wbishop

# black bishops
initial_state["C8"] = bbishop
initial_state["F8"] = bbishop

# white queen
initial_state["D1"] = wqueen

# black queen
initial_state["D8"] = bqueen

# white king
initial_state["E1"] = wking

# black king
initial_state["E8"] = bking

states.append(initial_state)

'''-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-'''

# board setup - draws the board as a pygame surface
board = pygame.Surface((size * 8, size * 8))
board.fill(white)
for x in range(0, 8):
    for y in range(0, 8):
        if (x + y) % 2 != 0:
            pygame.draw.rect(board, black, (x * size, y * size, size, size))

screen = pygame.display.set_mode((750, 600))
screen.blit(board, (0, 0))

for x in range(0, 8):
    for y in range(0, 8):
        if (x + y) % 2 == 0:
            text = font.render(boardlist[y][x], True, black)
        else:
            text = font.render(boardlist[y][x], True, white)
        screen.blit(text, (x * size, y * size))

'''-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-'''

'''functions required'''


# creates a new position for a new move
def make_move(move):
    to = move[-2:]
    if move[-1] == "+" or move[-1] == "#":
        to = move[-3:-1]
        move = move[:-1]
    to = to[0].upper() + to[1]
    from_coord = None
    # checks if castle
    if move[0] == "O":
        castle(move)

    # checks if pawn move
    elif move[0].islower() and len(move) == 2:
        if move[1] == "4" and len(states) % 2 != 0 and states[-1][move[0].upper() + "3"] != wpawn:
            from_coord = move[0].upper() + "2"
        elif move[1] == "5" and len(states) % 2 == 0 and states[-1][move[0].upper() + "6"] != bpawn:
            from_coord = move[0].upper() + "7"
        else:
            if len(states) % 2 != 0:
                from_coord = move[0].upper() + str(int(move[1]) - 1)
            elif len(states) % 2 == 0:
                from_coord = move[0].upper() + str(int(move[1]) + 1)
        next_move(from_coord, to)

    # checks if pawn takes
    elif move[0].islower() and len(move) == 4:
        if len(states) % 2 != 0:
            # if states[-1][move[0].upper() + str(int(move[3])-1)] == wpawn:
            from_coord = move[0].upper() + str(int(move[3]) - 1)
        elif len(states) % 2 == 0:
            # if states[-1][move[0].upper() + str(int(move[3]) + 1)] == wpawn:
            from_coord = move[0].upper() + str(int(move[3]) + 1)
        next_move(from_coord, to)

    # queen moves
    elif move[0] == "Q":
        if len(states) % 2 != 0:
            for i in states[-1]:
                if states[-1][i] == wqueen:
                    from_coord = i
            next_move(from_coord, to)

        elif len(states) % 2 == 0:
            for i in states[-1]:
                if states[-1][i] == bqueen:
                    from_coord = i
            next_move(from_coord, to)

    #     king moves
    elif move[0] == "K":
        if len(states) % 2 != 0:
            for i in states[-1]:
                if states[-1][i] == wking:
                    from_coord = i
            next_move(from_coord, to)

        elif len(states) % 2 == 0:
            for i in states[-1]:
                if states[-1][i] == bking:
                    from_coord = i
            next_move(from_coord, to)

    # knight moves
    elif move[0] == "N" and len(move) == 3:
        possible = possible_knight_moves(to)
        if len(states) % 2 != 0:
            for i in possible:
                if states[-1][i] == wknight:
                    from_coord = i
            next_move(from_coord, to)
        elif len(states) % 2 == 0:
            for i in possible:
                if states[-1][i] == bknight:
                    from_coord = i
            next_move(from_coord, to)

    elif move[0] == "N" and len(move) == 4 and move[1] != "x":
        rough_possible = possible_knight_moves(to)
        possible = []
        if move[1] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            for i in rough_possible:
                if i[0] == move[1].upper():
                    possible.append(i)
        else:
            for i in rough_possible:
                if i[1] == move[1]:
                    possible.append(i)
        if len(states) % 2 != 0:
            for i in possible:
                if states[-1][i] == wknight:
                    from_coord = i
            next_move(from_coord, to)
        elif len(states) % 2 == 0:
            for i in possible:
                if states[-1][i] == bknight:
                    from_coord = i
            next_move(from_coord, to)

    elif move[0] == "N" and len(move) == 4 and move[1] == "x":
        possible = possible_knight_moves(to)
        if len(states) % 2 != 0:
            for i in possible:
                if states[-1][i] == wknight:
                    from_coord = i
            next_move(from_coord, to)
        elif len(states) % 2 == 0:
            for i in possible:
                if states[-1][i] == bknight:
                    from_coord = i
            next_move(from_coord, to)

    # bishop moves
    elif move[0] == "B" and 3 <= len(move) <= 4:
        possible = possible_bishop_moves(to)
        if len(states) % 2 != 0:
            for i in possible:
                if states[-1][i] == wbishop:
                    from_coord = i
            next_move(from_coord, to)
        elif len(states) % 2 == 0:
            for i in possible:
                if states[-1][i] == bbishop:
                    from_coord = i
            next_move(from_coord, to)

    # rook moves
    elif move[0] == "R" and len(move) == 3:
        if len(states) % 2 != 0:
            possible = possible_rook_moves(to, "white")
            for i in possible:
                if states[-1][i] == wrook:
                    from_coord = i
            next_move(from_coord, to)
        elif len(states) % 2 == 0:
            possible = possible_rook_moves(to, "black")
            for i in possible:
                if states[-1][i] == brook:
                    from_coord = i
            next_move(from_coord, to)
    elif move[0] == "R" and len(move) == 4 and move[1] != "x":
        if len(states) % 2 != 0:
            rough_possible = possible_rook_moves(to, "white")
            possible = []
            if move[1] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                for i in rough_possible:
                    if i[0] == move[1].upper():
                        possible.append(i)
            else:
                for i in rough_possible:
                    if i[1] == move[1]:
                        possible.append(i)
            for i in possible:
                if states[-1][i] == wrook:
                    from_coord = i
            next_move(from_coord, to)
        elif len(states) % 2 == 0:
            rough_possible = possible_rook_moves(to, "black")
            possible = []
            if move[1] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                for i in rough_possible:
                    if i[0] == move[1].upper():
                        possible.append(i)
            else:
                for i in rough_possible:
                    if i[1] == move[1]:
                        possible.append(i)
            for i in possible:
                if states[-1][i] == brook:
                    from_coord = i
            next_move(from_coord, to)
    elif move[0] == "R" and len(move) == 4 and move[1] == "x":

        if len(states) % 2 != 0:
            possible = possible_rook_moves(to, "white")
            for i in possible:
                if states[-1][i] == wrook:
                    from_coord = i
            next_move(from_coord, to)
        elif len(states) % 2 == 0:
            possible = possible_rook_moves(to, "black")
            for i in possible:
                if states[-1][i] == brook:
                    from_coord = i
            next_move(from_coord, to)


# draws a board position onto the pygame window
def draw_state(state):
    for sq in state:
        if state[sq] is None:
            erase(sq)
        else:
            draw(sq, state[sq])
    pygame.draw.rect(screen, piece_white, (590, 90, 110, 30))
    if current_state % 2 == 0:
        text = mfont.render(f"{int(current_state / 2)}, Black", True, piece_black)
    elif current_state % 2 != 0:
        text = mfont.render(f"{int((current_state + 1) / 2)}, White", True, piece_black)
    if current_state == 0:
        text = mfont.render(f"START", True, piece_black)
    elif current_state == len(states) - 1:
        text = mfont.render(f"END", True, piece_black)
    screen.blit(text, (600, 90))


# erases a square, i.e., reflecting the source of a piece move
def erase(coord):
    x = coords[coord][0] - 10
    y = coords[coord][1]
    if ((x + y) / size) % 2 != 0:
        sq = pygame.Surface((size, size))
        pygame.draw.rect(sq, black, (0, 0, size, size))
        t = font.render(coord, True, white)
        screen.blit(sq, (x, y))
        screen.blit(t, (x, y))
    else:
        sq = pygame.Surface((size, size))
        pygame.draw.rect(sq, white, (0, 0, size, size))
        t = font.render(coord, True, black)
        screen.blit(sq, (x, y))
        screen.blit(t, (x, y))


# drawing a square with piece, i.e., reflecting destination of piece moved
def draw(coord, piece):
    x = coords[coord][0] - 10
    y = coords[coord][1]
    c = piece_white
    if piece in [bpawn, brook, bknight, bbishop, bqueen, bking]:
        c = piece_black
    p = pfont.render(piece, True, c)
    if ((x + y) / size) % 2 != 0:
        sq = pygame.Surface((size, size))
        pygame.draw.rect(sq, black, (0, 0, size, size))
        t = font.render(coord, True, white)
        screen.blit(sq, (x, y))
        screen.blit(t, (x, y))
        screen.blit(p, (x + 10, y))
    else:
        sq = pygame.Surface((size, size))
        pygame.draw.rect(sq, white, (0, 0, size, size))
        t = font.render(coord, True, black)
        screen.blit(sq, (x, y))
        screen.blit(t, (x, y))
        screen.blit(p, (x + 10, y))


# adds position to list of positions
def next_move(from_coord, to_coord):
    new_state = copy.deepcopy(states[-1])
    piece = states[-1][from_coord]
    new_state[from_coord] = None
    new_state[to_coord] = piece
    states.append(new_state)


# special function for castling
def castle(m):
    if len(m) == 5:
        if len(states) % 2 == 0:
            new_state = copy.deepcopy(states[-1])
            new_state["A8"], new_state["D8"] = new_state["D8"], new_state["A8"]
            new_state["E8"], new_state["C8"] = new_state["C8"], new_state["E8"]
            states.append(new_state)
        else:
            new_state = copy.deepcopy(states[-1])
            new_state["A1"], new_state["D1"] = new_state["D1"], new_state["A1"]
            new_state["E1"], new_state["C1"] = new_state["C1"], new_state["E1"]
            states.append(new_state)
    elif len(m) == 3:
        if len(states) % 2 == 0:
            new_state = copy.deepcopy(states[-1])
            new_state["H8"], new_state["F8"] = new_state["F8"], new_state["H8"]
            new_state["E8"], new_state["G8"] = new_state["G8"], new_state["E8"]
            states.append(new_state)
        else:
            new_state = copy.deepcopy(states[-1])
            new_state["H1"], new_state["F1"] = new_state["F1"], new_state["H1"]
            new_state["E1"], new_state["G1"] = new_state["G1"], new_state["E1"]
            states.append(new_state)


# checks for possible knight moves
def possible_knight_moves(coord):
    possible_rows = str(int(coord[1]) + 2), str(int(coord[1]) + 1), str(int(coord[1]) - 1), str(int(coord[1]) - 2)
    possible_columns = columns[columns.index(coord[0]) + 1], columns[columns.index(coord[0]) - 1], columns[
        columns.index(coord[0]) + 2], columns[columns.index(coord[0]) - 2]
    possible_moves = []
    for i in possible_columns:
        for j in possible_rows:
            if (i + j) in states[-1]:
                possible_moves.append(i + j)
    return possible_moves


# checks for possible bishop moves
def possible_bishop_moves(coord):
    val = int(columns.index(coord[0])) + int(coord[1])
    possible_moves = []
    for i in states[-1]:
        if (int(columns.index(i[0])) + int(i[1])) % 2 == val % 2:
            possible_moves.append(i)
    return possible_moves


# checks for possible rook moves
def possible_rook_moves(coord, turn):
    possible_moves = []
    possible_column = []
    column_reflection = []
    possible_row = []
    row_reflection = []
    for i in states[-1]:
        if i[0] == coord[0]:
            possible_column.append(i)
        if i[1] == coord[1]:
            possible_row.append(i)
    for i in possible_column:
        column_reflection.append(states[-1][i])
    for i in possible_row:
        row_reflection.append(states[-1][i])
    to_index_r = possible_row.index(coord)
    to_index_c = possible_column.index(coord)
    for i in range(0, to_index_r):
        if row_reflection[i] is None:
            possible_moves.append(possible_row[i])
        else:
            possible_moves.append(possible_row[i])
            break
    for i in range(to_index_r + 1, 8):
        if row_reflection[i] is None:
            possible_moves.append(possible_row[i])
        else:
            possible_moves.append(possible_row[i])
            break
    for i in range(0, to_index_c):
        if column_reflection[i] is None:
            possible_moves.append(possible_column[i])
        else:
            possible_moves.append(possible_column[i])
            break
    for i in range(to_index_c + 1, 8):
        if column_reflection[i] is None:
            possible_moves.append(possible_column[i])
        else:
            possible_moves.append(possible_column[i])
            break
    return possible_moves


# goes to previous position
def prev():
    global current_state
    if current_state > 0:
        current_state -= 1
    draw_state(states[current_state])


# goes to next position
def next():
    global current_state
    if current_state < len(states) - 1:
        current_state += 1
    draw_state(states[current_state])


'''-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-'''

draw_state(initial_state)

pygame.display.flip()

for i in range(0, len(moves)):
    make_move(moves[i])

# looping the program to keep reflecting changes and allow for user interaction
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 590 <= mouse[0] <= 640 and 30 <= mouse[1] <= 60:
                prev()
            if 650 <= mouse[0] <= 700 and 30 <= mouse[1] <= 60:
                next()
    mouse = pygame.mouse.get_pos()
    if 590 <= mouse[0] <= 640 and 30 <= mouse[1] <= 60:
        pygame.draw.rect(screen, lgreen, (590, 30, 50, 30))
    else:
        pygame.draw.rect(screen, dgreen, (590, 30, 50, 30))

    if 650 <= mouse[0] <= 700 and 30 <= mouse[1] <= 60:
        pygame.draw.rect(screen, lgreen, (650, 30, 50, 30))
    else:
        pygame.draw.rect(screen, dgreen, (650, 30, 50, 30))

    rbutton = tfont.render(rarrow, True, piece_black)
    lbutton = tfont.render(larrow, True, piece_black)
    screen.blit(lbutton, (600, 20))
    screen.blit(rbutton, (660, 20))

    pygame.display.update()
