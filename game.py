
import numpy as np
import tkinter as tk
import time as time
import random as rand

# Globals
UP = (-1,0)
DOWN = (1,0)
LEFT = (0,-1)
RIGHT = (0,1)

moves = [UP, DOWN, LEFT, RIGHT]

empty = 0
food = 99

class Game:
    def __init__(self, size, num_snakes, players, gui=None,display=False, max_turns=100):
        self.size = size
        self.num_snakes = num_snakes
        self.players = players
        self.gui = gui
        self.display = display
        self.max_turns = max_turns

        self.num_food = 4
        self.turns = 0
        self.snake_size = 3

# i indexing the size of the snake j indxing the number of snakes

        self.snakes = [[((j + 1) * self.size // (2 * self.num_snakes), self.size // 2 + 1) for i in range(self.snake_size)]
for j in range(self.num_snakes)]

        # TODO: breke to variables and ardenstand what they do
        self.food = [(self.size // 4, self.size // 4), (3 * self.size // 4, self.size // 4), ( self.size // 4, 3 * self.size // 4), (3 * self.size // 4, 3 * self.size // 4)]

        self.players_id = [i for i in range(self.num_snakes)]

        self.board = np.zeros([self.size, self.size])

        for i in self.players_id:
            for tup in self.snakes[i]:
                self.board[tup[0] ,tup[i]] = i + 1

        for tup in self.food:
            self.board[tup[0], tup[i]] = food

        self.food_index = 0

        self.food_xy = []

        for _ in range(200):
            self.food_xy.append((rand.randint(0, 9), rand.randint(0, 9)))

        print(self.food_xy)

    def move(self):
        moves = []
        # moves the head
        for i in self.players_id:
            snake_i = self.snakes[i]
            move_i =  self.players[i].get_move(self.board, snake_i)
            moves.append(move_i)
            snake_head = snake_i[-1]
            new_square = (snake_head[0] + move_i[0], snake_head[1] + move_i[1])
            snake_i.append(new_square)

        # move tail

        for i in self.players_id:
            head_i = self.snakes[i][-1]
            if head_i not in self.food:
                self.board[self.snakes[i][0][0]][self.snakes[i][0][1]] = empty
                self.snakes[i].pop(0)
            else:
                self.food.remove(head_i)

        # check out of bounds

        for i in self.players_id:
            head_i = self.snakes[i][-1]
            if head_i[0] >= self.size or head_i[1] >= self.size or head_i[0] < 0 or head_i[1] < 0:
                # the snake is dead
                print('removed - collision with borders ')
                self.players_id.remove(i)

            else:
                self.board[head_i[0]] [head_i[1]] = i + 1

        # check for collisions

        for i in self.players_id:
            head_i = self.snakes[i][-1]
            for j in range(self.num_snakes):
                # collision with itself
                if i == j:
                    if head_i in self.snakes[i][:-1]:
                        print('remove - collision with itself')
                        self.players_id.remove(i)
                else:
                    # collision with other snake
                    if head_i in self.snakes[j]:
                        print('removed - collision with other snake')
                        self.players_id.remove(i)

        # update food

        while len(self.food) < self.num_food:
            x = self.food_xy[self.food_index][0]
            y = self.food_xy[self.food_index][1]

            while self.board[x][y] != empty:
                self.food_index += 1
                x = self.food_xy[self.food_index][0]
                y = self.food_xy[self.food_index][1]
            self.food.append((x,y))
            self.board[x][y] = food
            self.food_index += 1

        return moves

    def play(self, display, termination):

        if display:
            self.dispaly_board()

        while True:
            if termination:
                for i in self.players_id:
                    if len(self.snakes[0]) - self.turns / 20 <= 0:
                        self.players_id.remove()

                        # remove return if more then one snake
                        return -2
            print(len(self.players_id))
            if len(self.players_id) == 0:
                return  -1

            if self.turns >= self.max_turns:
                return  0

            moves = self.move()
            self.turns += 1

            if display:
                for move in moves:
                    if move == UP:
                        print("up")

                    if move == DOWN:
                        print("down")

                    if move == LEFT:
                        print("left")

                    if move == RIGHT:
                        print("right")

                self.dispaly_board()

                if self.gui is not None:
                    self.gui.update()

                time.sleep(1)

    def dispaly_board(self):

        for i in range(self.size):
            for j in range(self.size):
                # empty place
                if self.board[i][j] == empty:
                    print('|_', end="")
                # their is food here
                elif self.board[i][j] == food:
                    print('|F', end="")
                # their is snake here
                else:
                    #print('|*', end="")
                    print('|' + str(int(self.board[i][j])), end="")
            print('|')


class Gui:

    def __init__(self, game, size):
        self.game = game
        self.game.gui = self
        self.size = size

        self.ratio = self.size / self.game.size

        self.app = tk.Tk()
        self.canvas = tk.Canvas(self.app, width=self.size,height=self.size)
        self.canvas.pack()

        for i in range(len(self.game.snakes)):
            color = '#' + '{0:03X}'.format((i + 1)* 500)
            snake = self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio * (snake[-1][1]), self.ratio * (snake[-1][0]), self.ratio * (snake[-1][1] + 1), self.ratio * (snake[-1][0] + 1),fill=color)

            for j in range(len(snake) - 1):
                color = '#' + '{0:03X}'.format((i + 1) * 123)
                snake = self.game.snakes[i]
                self.canvas.create_rectangle(self.ratio * (snake[j][1]), self.ratio * (snake[j][0]),
                                             self.ratio * (snake[j][1] + 1), self.ratio * (snake[j][0] + 1),
                                             fill=color)

            for food in self.game.food:
                self.canvas.create_rectangle(self.ratio * (food[1]), self.ratio * (food[0]),
                                             self.ratio * (food[1] + 1), self.ratio * (food[0] + 1),
                                             fill='#000000000')

    def update(self):
        self.canvas.delete("all")
        for i in range(len(self.game.snakes)):
            color = '#' + '{0:03X}'.format((i + 1) * 500)
            snake = self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio * (snake[-1][1]), self.ratio * (snake[-1][0]),
                                         self.ratio * (snake[-1][1] + 1), self.ratio * (snake[-1][0] + 1), fill=color)

            for j in range(len(snake) - 1):
                color = '#' + '{0:03X}'.format((i + 1) * 123)
                snake = self.game.snakes[i]
                self.canvas.create_rectangle(self.ratio * (snake[j][1]), self.ratio * (snake[j][0]),
                                             self.ratio * (snake[j][1] + 1), self.ratio * (snake[j][0] + 1),
                                             fill=color)

            for food in self.game.food:
                self.canvas.create_rectangle(self.ratio * (food[1]), self.ratio * (food[0]),
                                             self.ratio * (food[1] + 1), self.ratio * (food[0] + 1),
                                             fill='#000000000')


            self.canvas.pack()
            self.app.update()