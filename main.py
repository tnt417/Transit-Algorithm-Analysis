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

    grid = TransitGrid(10)

    run_single_test(grid)

# run_full_test()

grid = TransitGrid(10, express_chance=0.2, random_bus_start=True)

grid.random_add_n_stations(10)

print(grid)

while(True):
    clear_console()
    print(grid)
    time.sleep(0.1)
    grid.step()