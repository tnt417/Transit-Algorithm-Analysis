from algorithms import *
from transit import *

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

grid = TransitGrid(10)

grid.add_station(3, 3)

print(grid)