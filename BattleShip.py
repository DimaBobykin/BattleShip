import keyboard # imports
import colorama
from termcolor import colored
import time
import os
import random
import socket
import sys

INET_PORT = 10000

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

colorama.init()

# Defining Variables
player = 0
Pieces = []
TargetBoard = []
Board = []
Room = ""
connection = None


def attack(player): # Attacks
    Info = [["[ ]", 0, 0, "grey"]]
    global connection
    global TargetBoard
    TargetBoard = clear()
    print(TargetBoard)
    printscreen(TargetBoard)
    # Grab input 0
    while True:
        for Elements in Info:
            TargetBoard[Elements[1]][Elements[2]] = Elements[0]
        inputvar = keyboard.read_key()
        if inputvar == "d":
            Info[0][2] += 1
        if inputvar == "a":
            Info[0][2] += -1
        if inputvar == "w":
            Info[0][1] += -1
        if inputvar == "s":
            Info[0][1] += 1
        if inputvar == "c":
            break

    Y = Info[0][1]
    X = Info[0][2]

    if player == 1: # check host or client
        # Send input 1
        sock.sendall(str.encode(Y))
        sock.sendall(str.encode(X))
        # Wait result 2
        Data = sock.recv(16)
        Data = Data.decode("utf-8") 
        print(Data)
        if Data == "Yes":
            Info.append(["[X]", Y, X, "red"])
        else:
            Info.append(["[O]", Y, X, "cyan"])
        printscreen(TargetBoard)
    else: 
        # Send input 1
        connection.sendall(str.encode(Y))
        connection.sendall(str.encode(X))
        # Wait result 2
        Data = connection.recv(16)
        Data = Data.decode("utf-8") 
        print(Data)
        if Data == "Yes":
            Info.append(["[X]", Y, X, "red"])
        else:
            Info.append(["[O]", Y, X, "cyan"])
        printscreen(TargetBoard)


def waitattack(player): # Waits for attack
    global connection
    global Board
    printscreen(Board)
    if player == 1: # check host or client
        # wait for request
        Y = int(sock.recv(16))
        X = int(sock.recv(16))
        # send data back
        if Board[Y][X][0] == "[#]":
            sock.sendall(str.encode("Yes"))
        else:
            sock.sendall(str.encode("No"))
    else:
        # wait for request
        Y = int(connection.recv(16))
        X = int(connection.recv(16))
        # send data back
        if Board[Y][X][0] == "[#]":
            connection.sendall(str.encode("Yes"))
        else:
            connection.sendall(str.encode("No"))


def clear(): # resets board to the orignal state
    return [[["[ ]", "cyan"] for n in range(10)] for i in range(10)]
Board = clear() 

def printscreen(Board): # Prints the board
    Board = clear()
    for i in Pieces:
        place(i[0], i[1], i[2], i[3], Board)
    # os.system('cls')
    for i in range(10):
        print(
            colored(Board[i][0][0], Board[i][0][1]), 
            colored(Board[i][1][0], Board[i][1][1]), 
            colored(Board[i][2][0], Board[i][2][1]), 
            colored(Board[i][3][0], Board[i][3][1]), 
            colored(Board[i][4][0], Board[i][4][1]), 
            colored(Board[i][5][0], Board[i][5][1]), 
            colored(Board[i][6][0], Board[i][6][1]), 
            colored(Board[i][7][0], Board[i][7][1]), 
            colored(Board[i][8][0], Board[i][8][1]),
            colored(Board[i][9][0], Board[i][9][1]))
        print()
    print(Pieces)


def place(y, x, length, rotation, Board): # Placing Ships on Board
     # Pieces getting added to board
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
    return Board


def gameloop(): # Main Game Loop
    # Defining Vars, Etc.
    global Board
    Board = clear()
    global Room
    global player
    global connection
    global TargetBoard

    for i in range(10): # Making Target Board
        TargetBoard.append([])
        for n in range(10):
            TargetBoard[i].append([])
            TargetBoard[i][n].append("[ ]")
            TargetBoard[i][n].append("cyan")
    
    while True: # Join or make a room
        print(colored("Join: J, Make a New Room: M", "cyan"))
        inputvar = keyboard.read_key()
        os.system('cls')
        if inputvar == "j":
            print(colored("Room Code:", "cyan"))
            inputVar = input()
            Room = inputVar
            server_address = ('localhost', INET_PORT)
            print('connecting to %s port %s', server_address)
            sock.connect(server_address)
            player = 1
            break
        elif inputvar == "m":
            player = 0
            print(colored("Waiting For Person to Join", "cyan"))
            server_address = ("localhost", INET_PORT)
            sock.bind(server_address)
            sock.listen(1)
            connection, client_address = sock.accept()
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
            printscreen(Board)
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

    while True: # Shooting
        if player == 0:
            finished = False
            while not finished:
                attack(player)
                waitattack(player)
        if player == 1:
            finished = False
            while not finished:
                waitattack(player)
                attack(player)


    input()

gameloop()
