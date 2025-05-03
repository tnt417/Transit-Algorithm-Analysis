from algorithms import *
from transit import *
import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_algo(algo: Algorithm, grid: TransitGrid): # TODO

    before_time = time.time()

    actions, total_sim_time = algo.get_path(grid)

    if actions == None:
        raise RuntimeError("No path found!")

    action_index = 0

    while(True):

        # execute actions
        while action_index < len(actions) and actions[action_index][0] <= grid.time:
            action_time, action = actions[action_index]
            grid.take_action(action)
            action_index += 1

        grid.step()

        if grid.passenger_at_goal():
            break

    after_time = time.time()

    # returns elapsed time
    return after_time - before_time, total_sim_time

def run_full_test(repetitions = 1000, grid_size = 10, express_chance = 0.2, random_bus_start=True, n_stations = 50): #TODO: this should run many tests at the same time

    dijkstra = DijkstraAlgorithm()
    raptor = RaptorAlgorithm()
    connection = ConnectionAlgorithm()

    times_seconds = {"dijkstras": 0.0, "raptor": 0.0, "connection": 0.0 }

    max_sim_times = {"dijkstras": 0.0, "raptor": 0.0, "connection": 0.0 }

    for i in range(repetitions):

        seed = random.randint(0, 100000)

        grid_dij = TransitGrid(grid_size, express_chance=express_chance, random_bus_start=random_bus_start, seed=seed, n_stations=n_stations)
        
        # print(grid_dij)

        elapsed_time_dij, sim_time_dij = run_algo(dijkstra, grid_dij)
        
        times_seconds["dijkstras"] += elapsed_time_dij
        max_sim_times["dijkstras"] = max(max_sim_times["dijkstras"], sim_time_dij)

        # TODO: uncomment once implemented
        # grid_rapt = TransitGrid(grid_size, express_chance=express_chance, random_bus_start=random_bus_start, seed=seed, n_stations=n_stations)
        # times_seconds["raptor"] += run_algo(raptor, grid_rapt)

        # TODO: uncomment once implemented
        grid_conn = TransitGrid(grid_size, express_chance=express_chance, random_bus_start=random_bus_start, seed=seed, n_stations=n_stations)
        
        elapsed_time_conn, sim_time_conn = run_algo(connection, grid_conn)
        times_seconds["connection"] += elapsed_time_conn
        max_sim_times["connection"] = max(sim_time_conn, max_sim_times["connection"])

        if sim_time_dij != sim_time_conn:
            raise ValueError("Values should be equal for optimal solutions")

    return times_seconds, max_sim_times

# small grid size

repetitions = 1000
grid_size = 50
express_chance = 0.2
n_stations = grid_size*grid_size // 2

test_results, max_sim_times = run_full_test(repetitions=repetitions, grid_size=grid_size, express_chance=express_chance, n_stations=n_stations)
print("Algorithm timing results for " + str(repetitions) + " repetitions of a " + str(grid_size) + "x" + str(grid_size) 
      + " grid with a " + str(express_chance) + " probability of express lines and " + str(n_stations) + " stations:")
print(test_results)
print(max_sim_times)

# medium grid size

# repetitions = 100
# grid_size = 25
# express_chance = 0.2
# n_stations = grid_size*grid_size // 2

# test_results, max_sim_times = run_full_test(repetitions=repetitions, grid_size=grid_size, express_chance=express_chance, n_stations=n_stations)
# print("Algorithm timing results for " + str(repetitions) + " repetitions of a " + str(grid_size) + "x" + str(grid_size) 
#       + " grid with a " + str(express_chance) + " probability of express lines and " + str(n_stations) + " stations:")
# print(test_results)
# print(max_sim_times)

# large grid size

# repetitions = 100
# grid_size = 50
# express_chance = 0.2
# n_stations = grid_size*grid_size // 2

# test_results, max_sim_times = run_full_test(repetitions=repetitions, grid_size=grid_size, express_chance=express_chance, n_stations=n_stations)
# print("Algorithm timing results for " + str(repetitions) + " repetitions of a " + str(grid_size) + "x" + str(grid_size) 
#       + " grid with a " + str(express_chance) + " probability of express lines and " + str(n_stations) + " stations:")
# print(test_results)
# print(max_sim_times)

# UNCOMMENT TO TEST DIJKSTRAS INCLUDING PRINTING INTERMEDIATE GRIDS
# dij = DijkstraAlgorithm()

# before_time = time.time()

# for i in range(5):
#     grid = TransitGrid(100, express_chance=0.2, random_bus_start=True, seed = -1, n_stations = 500)
#     actions, total_time = dij.get_path(grid)

#     if actions == None:
#         raise RuntimeError("No path found!")

#     # print(grid)

#     action_index = 0

#     while(True):

#         #clear_console()
#         #print(grid)
#         #print(actions)

#         # execute actions
#         while action_index < len(actions) and actions[action_index][0] <= grid.time:
#             action_time, action = actions[action_index]
#             grid.take_action(action)
#             action_index += 1
#             #time.sleep(5)

#         #time.sleep(0.5)
#         grid.step()

#         if grid.passenger_at_goal():
#             break

# after_time = time.time()

# elapsed_seconds = after_time - before_time

# print("Successfully simulated 1,000 dijkstras! Took " + str(elapsed_seconds) + " seconds")