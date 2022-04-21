
from game import *
import random as rand

class RandomPlayer:
    def __init__(self, i):
        self.i = i
    def get_move(self, board, snake):
        r = rand.randint(0, 3)
        return moves[r]

class GeneticPlayer:

    def __init__(self,  population_size, num_generation, num_trails, window_size, hidden_size, board_size, mutation_chance=0.1, mutation_size=0.1):
        self.population_size = population_size
        self.num_generation = num_generation
        self.num_trails = num_trails
        self.window_size = window_size
        self.hidden_size = hidden_size
        self.board_size = board_size
        self.mutation_chance = mutation_chance
        self.mutation_size = mutation_size

        ##### DEBUG
        self.display = False

        self.current_brain = None

        self.population = [self.generate_brain(input_size, hidden_size, output_size) for _ in range(self.population_size)]

    def generate_brain(input_size, hidden_size, output_size):
        print('genarate brain')
        #hidden_layer1 =

