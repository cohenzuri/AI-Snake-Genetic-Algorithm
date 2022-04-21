
from players import *
from game import *

size = 10
num_snakes = 1
gui_size = 800
players = [RandomPlayer(0)]

game = Game(size, num_snakes, players, display=True, max_turns=100)
gui = Gui(game, gui_size)
print(game.play(True, termination=False))