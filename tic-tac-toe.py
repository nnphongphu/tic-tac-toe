# ----- Start of Introduction -----
# Tic Tac Toe Project
# Created by Phong-Phu Nguyen
# Updated from June 14, 2019 - June 15, 2019
#
# First project with Python
# Has both basic AI (random decisions) as well as
# educated AI (minimax)
# ----- End of Introduction -----

# Library import
from tkinter import *
from math import *
from math import inf as infinity
import random
from copy import deepcopy

# Tkinter setup
root = Tk()
screen = Canvas(root, width=500, height=500, background="#222")
screen.pack()

# Variable setup
project_name = "Tic Tac Toe"
difficulty = ["Easy", "Norm", "Hard"]
running = False
level = 0
MAX = 1
result_evaluate = {
    "X WINS!": -1,
    "O WINS!": 1,
    "DRAW!": 0
}

def valid(array, x, y):
    return array[x - 1][y - 1] == 0


def is_game_over(array):
    potential_win = []
    for row in array:
        potential_win.append(set(row))

    for i in range(3):
        potential_win.append(set([array[k][i] for k in range(3)]))

    potential_win.append(set([array[i][i] for i in range(3)]))
    potential_win.append(set([array[i][2 - i] for i in range(3)]))

    for trio in potential_win:
        if trio == set([-1]):
            return "X WINS!"
        elif trio == set([1]):
            return "O WINS!"
    return "DRAW!"


def feasible_moves(array):
    ans = []
    for row in range(3):
        for col in range(3):
            if valid(array, row + 1, col + 1):
                ans.append([row, col])
    return ans


class Board:
    player = 1
    array = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]

    def move_board(self, x, y, c):
        self.array[x - 1][y - 1] = c
        self.update_board(x, y, c)

    def dumb_move(self):
        moves = feasible_moves(self.array)
        ans = moves[random.randint(0, len(moves) - 1)]
        self.move_board(ans[0] + 1, ans[1] + 1, 1)

    def slightly_less_dumb_move(self):
        # Check if there is any move that make O the winner
        for i in [1, -1]:
            for row in range(3):
                if self.array[row].count(i) == 2 and self.array[row].count(0) == 1:
                    for col in range(3):
                        if self.array[row][col] == 0:
                            self.move_board(row + 1, col + 1, 1)
                            return
            for j in range(3):
                col = [self.array[k][j] for k in range(3)]
                if col.count(i) == 2 and col.count(0) == 1:
                    for k in range(3):
                        if self.array[k][j] == 0:
                            self.move_board(k + 1, j + 1, 1)
                            return
            c1 = [self.array[j][j] for j in range(3)]
            if c1.count(i) == 2 and c1.count(0) == 1:
                for j in range(3):
                    if self.array[j][j] == 0:
                        self.move_board(j + 1, j + 1, 1)
                        return

            c2 = [self.array[j][2 - j] for j in range(3)]
            if c2.count(i) == 2 and c2.count(0) == 1:
                for j in range(3):
                    if self.array[j][2 - j] == 0:
                        self.move_board(j + 1, 3 - j, 1)
                        return

        if valid(self.array, 2, 2):
            self.move_board(2, 2, 1)
            return

        self.dumb_move()
        return

    def minimax(self, state, depth, player):
        # Is player playing max?
        if player == MAX:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or is_game_over(state) != "DRAW!":
            return [-1, -1, result_evaluate.get(is_game_over(state))]

        for cell in feasible_moves(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == MAX:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score
        return best

    def update_board(self, x, y, c):
        if c == -1:
            x1 = 100 + 100 * (y - 1) + 10
            y1 = 50 + 100 * (x - 1) + 10
            screen.create_line(x1, y1, x1 + 80, y1 + 80, width=5, fill="#7B2435")
            screen.create_line(x1, y1 + 80, x1 + 80, y1, width=5, fill="#7B2435")
        else:
            x1 = 100 + 100 * (y - 1) + 50
            y1 = 50 + 100 * (x - 1) + 50
            screen.create_oval(x1 - 40, y1 - 40, x1 + 40, y1 + 40, width=5, outline="#FFBC87")

        number_of_moves = len(feasible_moves(self.array))
        if number_of_moves == 0:
            screen.create_text(250, 30, text=is_game_over(self.array), font=("Helvetica", 30), fill="#FFFFFF")
            self.player = 0
        elif is_game_over(self.array) != "DRAW!":
            screen.create_text(250, 30, text=is_game_over(self.array), font=("Helvetica", 30), fill="#FFFFFF")
            self.player = 0

        self.player = -self.player
        if self.player == -1:
            if level == 1:
                self.dumb_move()
            elif level == 2:
                self.slightly_less_dumb_move()
            else:
                next_move = self.minimax(self.array.copy(), number_of_moves, 1)
                self.move_board(next_move[0] + 1, next_move[1] + 1, 1)


def create_buttons():
    screen.create_rectangle(0, 400, 250, 505, fill="#81E7FF")
    screen.create_rectangle(250, 400, 505, 505, fill="#FF6666")

    screen.create_text(250/2, 450, text="RENEW", font=("Helvetica", 30), fill="#FFFFFF")
    screen.create_text(250 + 250/2, 450, text="MENU", font=("Helvetica", 30), fill="#FFFFFF")


def draw_the_board():
    screen.create_line(200, 50, 200, 350, width=5, fill="#78FFF0")
    screen.create_line(300, 50, 300, 350, width=5, fill="#78FFF0")
    screen.create_line(100, 150, 400, 150, width=5, fill="#78FFF0")
    screen.create_line(100, 250, 400, 250, width=5, fill="#78FFF0")


def play_game():
    screen.delete(ALL)
    create_buttons()
    draw_the_board()


def click_handle(event):
    global level, running, board
    x_mouse = event.x
    y_mouse = event.y
    if running:
        if y_mouse >= 400:
            # Renew click
            if x_mouse <= 250:
                board.player = 1
                board.array = [[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]]
                play_game()
            # Quit click
            else:
                board.player = 1
                board.array = [[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]]
                running = False
                screen.delete(ALL)
                run_game()
        else:
            # Is it the player's turn?
            if board.player == 1:
                if 110 <= x_mouse <= 390 and 60 <= y_mouse <= 340:
                    y = int(ceil((x_mouse - 100)/100))
                    x = int(ceil((y_mouse - 50)/100))
                    if valid(board.array, x, y):
                        board.move_board(x, y, -1)
    else:
        # Difficulty click
        if 250 <= y_mouse <= 300:
            # Easy
            if 25 <= x_mouse <= 175:
                level = 1
            # Normal
            elif 175 <= x_mouse <= 325:
                level = 2
            # Hard
            elif 325 <= x_mouse <= 475:
                level = 3
        if level != 0:
            running = True
            play_game()


def run_game():
    # Title and shadow
    screen.create_text(252, 202 - 30/2, text=project_name.upper(), anchor="c", font=("Helvetica", 30), fill="#737373")
    screen.create_text(250, 200 - 30/2, text=project_name.upper(), anchor="c", font=("Helvetica", 30), fill="#FFFFFF")

    # Creating difficulty buttons
    for i in range(3):
        screen.create_rectangle(25 + 150 * i, 250, 25 + 150 + 150 * i, 300, fill="#FFFFFF")
        screen.create_text(25 + 150 * i + 75, 275, text=difficulty[i], font=("Helvetica", 30), fill="#737373")


# Board setup
board = Board()
run_game()
root.bind("<Button-1>", click_handle)
root.wm_title(project_name)
root.mainloop()