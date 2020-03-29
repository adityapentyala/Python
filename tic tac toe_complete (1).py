#tic tac toe game
#after you get 3 in a row, click on the X/O tile again to display win message box
#EDIT(17/10/2017): Added scoreboard and resetting of game

#CODE(with partial explanation):

#modules import and variable setup
from tkinter import *
import tkinter as tk
root = tk.Tk()
import tkinter.messagebox
root.title("tic tac toe")
bclick = True
var = 1
Owins = 0
Xwins = 0
draw = 0


#definition of function for making playing area
def board(buttons):
   global bclick
   if buttons["text"] == " " and bclick == True:
       buttons["text"] = "O"
       bclick = False
   elif buttons["text"] == " " and bclick == False:
       buttons["text"] = "X"
       bclick = True
       
#now for win situations
#there are 8 win situations for X or O (see down for grid plot): 123 ; 456 ; 789 ; 147 ; 258 ; 369 ; 159 and 357
#so , the below codes check for any of the situations for X or O
      
#situation if player X wins
   elif (button1["text"] == "X" and button2["text"] == "X" and button3["text"] == "X" or
       button4["text"] == "X" and button5["text"] == "X" and button6["text"] == "X" or
       button7["text"] == "X" and button8["text"] == "X" and button9["text"] == "X" or
       button1["text"] == "X" and button4["text"] == "X" and button7["text"] == "X" or
       button2["text"] == "X" and button5["text"] == "X" and button8["text"] == "X" or
       button3["text"] == "X" and button6["text"] == "X" and button9["text"] == "X" or
       button1["text"] == "X" and button5["text"] == "X" and button9["text"] == "X" or
       button3["text"] == "X" and button5["text"] == "X" and button7["text"] == "X" ):
            tk.messagebox.showinfo("Winner X", "Player X won the game")
            button1["text"] = " "
            button2["text"] = " "
            button3["text"] = " "
            button4["text"] = " "
            button5["text"] = " "
            button6["text"] = " "
            button7["text"] = " "
            button8["text"] = " "
            button9["text"] = " "
            global Xwins
            Xwins = Xwins + 1
            Xscoreboard["text"] = "X =", Xwins
#situation if player O wins
   elif (button1["text"] == "O" and button2["text"] == "O" and button3["text"] == "O" or
        button4["text"] == "O" and button5["text"] == "O" and button6["text"] == "O" or
        button7["text"] == "O" and button8["text"] == "O" and button9["text"] == "O" or
        button1["text"] == "O" and button4["text"] == "O" and button7["text"] == "O" or
        button2["text"] == "O" and button5["text"] == "O" and button8["text"] == "O" or
        button3["text"] == "O" and button6["text"] == "O" and button9["text"] == "O" or
        button1["text"] == "O" and button5["text"] == "O" and button9["text"] == "O" or
        button3["text"] == "O" and button5["text"] == "O" and button7["text"] == "O" ):
             tk.messagebox.showinfo("Winner O", "Player O won the game")
             button1["text"] = " "
             button2["text"] = " "
             button3["text"] = " "
             button4["text"] = " "
             button5["text"] = " "
             button6["text"] = " "
             button7["text"] = " "
             button8["text"] = " "
             button9["text"] = " "
             global Owins                       
             Owins = Owins + 1
             Oscoreboard["text"] = "O =", Owins
   elif (button1["text"] != "X" or button2["text"] != "X" or button3["text"] != "X" and
       button4["text"] != "X" or button5["text"] != "X" or button6["text"] != "X" and
       button7["text"] != "X" or button8["text"] != "X" or button9["text"] != "X" and
       button1["text"] != "X" or button4["text"] != "X" or button7["text"] != "X" and
       button2["text"] != "X" or button5["text"] != "X" or button8["text"] != "X" and
       button3["text"] != "X" or button6["text"] != "X" or button9["text"] != "X" and
       button1["text"] != "X" or button5["text"] != "X" or button9["text"] != "X" and
       button3["text"] != "X" or button5["text"] != "X" or button7["text"] != "X" and
       button1["text"] != "O" or button2["text"] != "O" or button3["text"] != "O" and
       button4["text"] != "O" or button5["text"] != "O" or button6["text"] != "O" and
       button7["text"] != "O" or button8["text"] != "O" or button9["text"] != "O" and
       button1["text"] != "O" or button4["text"] != "O" or button7["text"] != "O" and
       button2["text"] != "O" or button5["text"] != "O" or button8["text"] != "O" and
       button3["text"] != "O" or button6["text"] != "O" or button9["text"] != "O" and
       button1["text"] != "O" or button5["text"] != "O" or button9["text"] != "O" and
       button3["text"] != "O" or button5["text"] != "O" or button7["text"] != "O" ):
              tk.messagebox.showinfo("DRAW", "Well played!")
              button1["text"] = " "
              button2["text"] = " "
              button3["text"] = " "
              button4["text"] = " "
              button5["text"] = " "
              button6["text"] = " "
              button7["text"] = " "
              button8["text"] = " "
              button9["text"] = " "
              global draw
              draw =draw + 1
              drawscoreboard["text"] = "Draw =", draw
        
#code to make 3 x 3 grid with 9 buttons
buttons = StringVar()

#button no.1
button1 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button1))
button1.grid(row = 1, column = 0, sticky = S+N+E+W)

#button no.2
button2 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button2))
button2.grid(row = 2, column = 0, sticky = S+N+E+W)

#button no.3
button3 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button3))
button3.grid(row = 3, column = 0, sticky = S+N+E+W)

#button no.4
button4 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button4))
button4.grid(row = 1, column = 1, sticky = S+N+E+W)

#button no.5
button5 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button5))
button5.grid(row = 2, column = 1, sticky = S+N+E+W)

#button no.6
button6 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button6))
button6.grid(row = 3, column = 1, sticky = S+N+E+W)

#button no.7
button7 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button7))
button7.grid(row = 1, column = 2, sticky = S+N+E+W)

#button no.8
button8 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button8))
button8.grid(row = 2, column = 2, sticky = S+N+E+W)

#button no.9
button9 = Button(root, text = " ", height = 4, width = 8, command = lambda: board(button9))
button9.grid(row = 3, column = 2, sticky = S+N+E+W)

Xscoreboard = Label(root, text = ("X =", Xwins))
Xscoreboard.grid(row = 1, column = 5, sticky = S+N+E+W)

Oscoreboard = Label(root, text = ("O =", Owins))
Oscoreboard.grid(row = 2, column = 5, sticky = S+N+E+W)

drawscoreboard = Label(root, text = ("Draw =", draw))
drawscoreboard.grid(row = 3, column = 5, sticky = S+N+E+W)

#looping the program
root.mainloop()


#Have a good day!
#NOTE:
#the grid is in the form:-
#                             1   2   3
#                             4   5   6
#                             7   8   9





              
