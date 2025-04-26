from algorithms import *
from transit import *
import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_single_test(grid: TransitGrid): # TODO

    dijkstra = DijkstraAlgorithm()
    raptor = RaptorAlgorithm()
    drt = DrtAlgorithm()

    results = [benchmark_algo(dijkstra, grid), benchmark_algo(raptor, grid), benchmark_algo(drt, grid)]

    print(results)

def benchmark_algo(algo: Algorithm, grid: TransitGrid): # TODO

    before_time = 0 # TODO

    result = algo.run(grid)

    after_time = 0 # TODO

    return after_time - before_time

def run_full_test(): #TODO: this should run many tests at the same time

    grid = TransitGrid(100)

    run_single_test(grid)

# run_full_test()

grid = TransitGrid(10, express_chance=0.2, random_bus_start=True, seed = -1, n_stations = 50)

print(grid)

while(True):
    clear_console()
    print(grid)

    # get user input here
    grid.TEST_manual_board()

    time.sleep(0.5)
    grid.step()