import keyboard # imports
import colorama
from termcolor import colored
import time
import os
from os import path
import random

colorama.init()

# Defining Variables
player = 0
Pieces = []
Board = []
Room = ""


def Generation(): # Geneartes Room Code
    global Room
    AllCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for _ in range(4):
        Room = Room + AllCharacters[random.randrange(len(AllCharacters))]
    print(colored(Room, "cyan"))


def clear(): # resets board to the orignal state
    global Board
    Board = []
    for i in range(10):
        Board.append([])
        for n in range(10):
            Board[i].append([])
            Board[i][n].append("[ ]")
            Board[i][n].append("cyan")


def store(): # adds to local server aka: txt file
    for i in range(10):
        BoardList = []
        for n in range(10):
            BoardList.append(Board[i][n][0])
        file = open(Room + ".txt", "a")
        file.write(str(BoardList))
        file.write("\n")
        file.close()
    

def printscreen(): # Prints the board
    clear()
    for i in Pieces:
        place(i[0], i[1], i[2], i[3])
    os.system('cls')
    for i in range(10):
        print(colored(Board[i][0][0], Board[i][0][1]), colored(Board[i][1][0], Board[i][1][1]), colored(Board[i][2][0], Board[i][2][1]), colored(Board[i][3][0], Board[i][3][1]), colored(Board[i][4][0], Board[i][4][1]), colored(Board[i][5][0], Board[i][5][1]), colored(Board[i][6][0], Board[i][6][1]), colored(Board[i][7][0], Board[i][7][1]), colored(Board[i][8][0], Board[i][8][1]), colored(Board[i][9][0], Board[i][9][1]))
        print()


def place(y, x, length, rotation): # Placing Ships on Board
    global Board # Pieces getting added to board
    if rotation:
        for i in range(length):
            if Board[y+i][x][0] == "[#]":
                Board[y+i][x][1] = "red"
            Board[y+i][x][0] = "[#]"
    else:
        for i in range(length):
            if Board[y][x+i][0] == "[#]":
                Board[y][x+i][1] = "red"
            Board[y][x+i][0] = "[#]"


def gameloop(): # Main Game Loop
    clear()
    global Room
    
    while True: # Join or make a room
        print(colored("Join: J, Make a New Room: M", "cyan"))
        inputvar = keyboard.read_key()
        os.system('cls')
        if inputvar == "j":
            print(colored("Room Code:", "cyan"))
            inputVar = input()
            if path.exists(inputVar + ".txt"):
                Room = inputVar
                file = open(Room + ".txt", "a")
                file.write("\n")
                file.close()
                break
        elif inputvar == "m":
            print(colored("Room Code:", "cyan"))
            Generation()
            file = open(Room + ".txt", "w")
            file.close()
            print(colored("Waiting For Person to Join", "cyan"))
            while True:
                if len(open(Room + ".txt").readlines()) == 1:
                    break
            break

    for i in range(5): # Placing Ships
        # length of ships
        if i == 0:
            length = 2
        if i == 1 or i == 2:
            length = 3
        if i == 3:
            length = 4
        if i == 4:
            length = 5
        Pieces.append([0, 0, length, True])
        finished = False
        while not finished: # input and movement
            printscreen()
            inputvar = keyboard.read_key()
            if inputvar == "d":
                Pieces[i][1] = Pieces[i][1] + 1
            if inputvar == "a":
                Pieces[i][1] = Pieces[i][1] + -1
            if inputvar == "w":
                Pieces[i][0] = Pieces[i][0] + -1
            if inputvar == "s":
                Pieces[i][0] = Pieces[i][0] + 1
            if inputvar == "r":
                if Pieces[i][3]:
                    Pieces[i][3] = False
                else:
                    Pieces[i][3] = True
            if inputvar == "c":  # When finished placing
                ifclear = True
                for n in range(10):
                    for j in range(10):
                        if Board[n][j][1] == 'red':
                            ifclear = False
                if ifclear:
                    finished = True
            if inputvar == "q":
                quit()
            if inputvar == "t":
                break
            time.sleep(0.2)

    input()
    os.remove(Room + ".txt")


gameloop()
