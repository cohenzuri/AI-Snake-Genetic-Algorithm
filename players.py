import math
import numpy as np
from game import *
import random as rand

class RandomPlayer:
    def __init__(self, i):
        self.i = i
    def get_move(self, board, snake):
        r = rand.randint(0, 3)
        return moves[r]

class GeneticPlayer:

    def __init__(self, population_size, num_generations, num_trails, window_size, hidden_size, board_size, mutation_chance=0.1, mutation_size=0.1):
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_trails = num_trails
        self.window_size = window_size
        self.hidden_size = hidden_size
        self.board_size = board_size
        self.mutation_chance = mutation_chance
        self.mutation_size = mutation_size

        ##### DEBUG
        self.display = False

        self.current_brain = None

        self.population = [self.generate_brain(self.window_size**2, self.hidden_size, len(moves)) for _ in range(self.population_size)]

    def generate_brain(self, input_size, hidden_size, output_size):

        hidden_layer_1 = np.array([[rand.uniform(-1, 1) for _ in range(input_size + 1)] for _ in range(hidden_size)])
        hidden_layer_2 = np.array([[rand.uniform(-1, 1) for _ in range(hidden_size + 1)] for _ in range(hidden_size)])
        output_layer = np.array([[rand.uniform(-1, 1) for _ in range(hidden_size + 1)] for _ in range(output_size)])

        return[hidden_layer_1, hidden_layer_2, output_layer]

    def get_move(self, board, snake):
        input_vector = self.proccess_board(board, snake[-1][0], snake[-1][1], snake[-2][0], snake[-2][1])

        hidden_layer_1 = self.current_brain[0]
        hidden_layer_2 = self.current_brain[1]
        output_layer = self.current_brain[2]

        # Forword prop

        #####################
        test_2 = hidden_layer_1.shape[0]
        #test_1 = math.tanh(np.dot(input_vector, hidden_layer_1[0]))
        test_3 = np.dot(input_vector, hidden_layer_1[0])
        test_4 = math.tanh(test_3)
        print('test' ,test_4)
        #####################

        hidden_result_1 = np.array([math.tanh(np.dot(input_vector, hidden_layer_1[i])) for i in range(hidden_layer_1.shape[0])]+[1])
        hidden_result_2 = np.array([math.tanh(np.dot(hidden_result_1, hidden_layer_2[i])) for i in range(hidden_layer_2.shape[0])]+[1])
        output_result = np.array([math.tanh(np.dot(hidden_result_2, output_layer[i])) for i in range(output_layer.shape[0])])
        max_index = np.argmax(output_result)

        return moves[max_index]

    def proccess_board(self, board, x1, y1, x2, y2):
        # x and y is the position of the snake
        input_vector = [[0 for _ in range(self.window_size)] for _ in range(self.window_size)]

        for i in range(self.window_size):
            for j in range(self.window_size):
                ii = x1 + i - self.window_size//2
                jj = y1 + j - self.window_size//2

                # if window out of bounds snake cant move to that position
                if ii  < 0 or jj < 0 or ii >= self.board_size or jj >= self.board_size:
                    print('try to move out of board borders')
                    input_vector[i][j] = -1
                elif board[ii][jj] == food:
                    print('move to location with food')
                    input_vector[i][j] = 1
                elif board[ii][jj] == empty:
                    input_vector[i][j] = 0
                else:
                    print('try to move to position with enother snake')
                    return -1

        if self.display:
            print(np.array(input_vector))

        input_vector = list(np.array(input_vector).flatten()) + [1]
        return  np.array(input_vector)

    def reproduce(self, top_25):
        new_population = []

        # the copy for the top 25 percentage go the the next generation as is
        for brain in top_25:
            new_population.append(brain)
        # add mutations to the top 25 percentage and add them to the next generation
        for brain in top_25:
            new_brain = self.mutate(brain)
            new_population.append(new_brain)
        # spawn new random brains and add them to the next generation
        for _ in range(self.population_size//2):
            new_population.append(self.generate_brain(self.window_size ** 2, self.hidden_size, len(moves)))

        return new_population

    def mutate(self, brain):
        new_brain = []
        for layer in brain:
            new_layer = np.copy(layer)
            for i in range(new_layer.shape[0]):
                for j in range(new_layer.shape[1]):
                    if rand.uniform(0,1) < self.mutation_chance:
                        new_layer[i][j] += rand.uniform(-1,1)*self.mutation_size
            new_brain.append(new_layer)
        return  new_brain

    def one_generation(self):
        scores = [0 for _ in range(self.population_size)]
        max_score = 0

        for i in range(self.population_size):
            for j in range(self.num_trails):
                self.current_brain = self.population[i]
                game = Game(self.board_size, 1, [self])
                outcome = game.play(False,termination=True)
                score = len(game.snakes[0])
                scores[i] += score

                if outcome == 0:
                    print(f'snake {i} made it to the last turn')
                if score > max_score:
                    max_score = score
                    print(f'max score at snake id {i}')

        # Testing of each brain is complete and they are all ranked
        top_25_indexs = list(np.argsort(score))[3*(self.population_size//4): self.population_size]
        print(scores)
        top_25 = [self.population[i] for i in top_25_indexs][::-1]
        self.population = self.reproduce(top_25)


    def evolve_pop(self):
        for i in range(self.num_generations):
            self.one_generation()
            print("gen", i)

        # display board for top brains
        key = input('enter any character to display board')
        for brain in self.population:
            self.display = True
            self.current_brain = brain
            game = Game(self.board_size, 1, [self], display=True)
            gui = Gui(game, 800)
            game.play(True, termination=True)
            print('snake length', len(game.snakes[0]))

