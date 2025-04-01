from algorithms import *

def run_tests(): # TODO

    dijkstra = DijkstraAlgorithm()
    raptor = RaptorAlgorithm()
    drt = DrtAlgorithm()

    results = [benchmark_algo(dijkstra), benchmark_algo(raptor), benchmark_algo(drt)]

    print(results)

def benchmark_algo(algo): # TODO

    before_time = 0 # TODO
    
    result = algo.run()

    after_time = 0 # TODO

    return after_time - before_time

run_tests()