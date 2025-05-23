from algorithms import *
from transit import *
import time
import matplotlib.pyplot as plt
import numpy as np

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
    return after_time - before_time, total_sim_time, len(actions)/2

def run_full_test(repetitions = 1000, grid_size = 10, express_chance = 0.2, random_bus_start=True, n_stations = 50): #TODO: this should run many tests at the same time

    dijkstra = DijkstraAlgorithm()
    raptor = RaptorAlgorithm()
    connection = ConnectionAlgorithm()

    times_seconds = {"dijkstras": 0.0, "raptor": 0.0, "connection": 0.0 }

    sum_sim_times = {"dijkstras": 0.0, "raptor": 0.0, "connection": 0.0 }

    sum_transfers = {"dijkstras": 0.0, "raptor": 0.0, "connection": 0.0 }

    for i in range(repetitions):

        seed = random.randint(0, 100000)

        grid_dij = TransitGrid(grid_size, express_chance=express_chance, random_bus_start=random_bus_start, seed=seed, n_stations=n_stations)

        elapsed_time_dij, sim_time_dij, tfrs_dij = run_algo(dijkstra, grid_dij)
        
        times_seconds["dijkstras"] += elapsed_time_dij
        sum_sim_times["dijkstras"] += sim_time_dij
        sum_transfers["dijkstras"] += tfrs_dij

        grid_rapt = TransitGrid(grid_size, express_chance=express_chance, random_bus_start=random_bus_start, seed=seed, n_stations=n_stations)
        
        elapsed_time_rapt, sim_time_rapt, tfrs_rapt = run_algo(raptor, grid_rapt)

        times_seconds["raptor"] += elapsed_time_rapt
        sum_sim_times["raptor"] += sim_time_rapt
        sum_transfers["raptor"] += tfrs_rapt

        grid_conn = TransitGrid(grid_size, express_chance=express_chance, random_bus_start=random_bus_start, seed=seed, n_stations=n_stations)
        
        elapsed_time_conn, sim_time_conn, tfrs_conn = run_algo(connection, grid_conn)
        times_seconds["connection"] += elapsed_time_conn
        sum_sim_times["connection"] += sim_time_conn
        sum_transfers["connection"] += tfrs_conn

        if sim_time_dij != sim_time_conn:
            raise ValueError("Values should be equal for optimal solutions")

    return times_seconds, {k:(v/repetitions) for (k,v) in sum_sim_times.items()}, {k:(v/repetitions) for (k,v) in sum_transfers.items()}

grid_sizes = []
times_dij = []
times_conn = []
times_rapt = []

avg_sim_dij = []
avg_sim_conn = []
avg_sim_rapt = []

avg_transfers_dij = []
avg_transfers_conn = []
avg_transfers_rapt = []

repetitions_per_size = 20

for grid_size in range(10,30):

    print("Grid size " + str(grid_size) + "...")

    grid_sizes.append(grid_size)

    express_chance = 0.2
    n_stations = grid_size*grid_size // 2

    test_results, avg_sim_times, avg_transfers = run_full_test(repetitions=repetitions_per_size, grid_size=grid_size, express_chance=express_chance, n_stations=n_stations)
    # print("Algorithm timing results for " + str(repetitions) + " repetitions of a " + str(grid_size) + "x" + str(grid_size) 
    #     + " grid with a " + str(express_chance) + " probability of express lines and " + str(n_stations) + " stations:")
    # print("Total compute time: " + str(test_results))
    # print("Average timesteps to goal: " + str(avg_sim_times))
    # print("Average transfers to goal: " + str(avg_transfers))

    times_dij.append(test_results["dijkstras"])
    times_conn.append(test_results["connection"])
    times_rapt.append(test_results["raptor"])

    avg_sim_dij.append(avg_sim_times["dijkstras"])
    avg_sim_conn.append(avg_sim_times["connection"])
    avg_sim_rapt.append(avg_sim_times["raptor"])

    avg_transfers_dij.append(avg_transfers["dijkstras"])
    avg_transfers_conn.append(avg_transfers["connection"])
    avg_transfers_rapt.append(avg_transfers["raptor"])

x = np.array(grid_sizes)

plt.figure()
plt.scatter(x, times_dij, label="Dijkstra's")
plt.scatter(x, times_rapt, label="RAPTOR")
plt.scatter(x, times_conn, label="CSA")
plt.xlabel('Grid Size')
plt.ylabel(f'Compute Time for {repetitions_per_size} Solves (s)')
plt.title('Compute Time vs Grid Size')
plt.legend()

plt.figure()
plt.scatter(x, avg_sim_dij, label="Dijkstra's and CSA")
plt.scatter(x, avg_sim_rapt, label="RAPTOR")
plt.xlabel('Grid Size')
plt.ylabel('Average Simulation Timesteps to Goal')
plt.title('Average Simulation Timesteps vs Grid Size')
plt.legend()

plt.figure()
plt.scatter(x, avg_transfers_dij, label="Dijkstra's")
plt.scatter(x, avg_transfers_rapt, label="RAPTOR")
plt.scatter(x, avg_transfers_conn, label="CSA")
plt.xlabel('Grid Size')
plt.ylabel('Average Number of Transfers to Goal')
plt.title('Average Transfers vs Grid Size')
plt.legend()

plt.show()

# small grid size

# repetitions = 100
# grid_size = 20
# express_chance = 0.2
# n_stations = grid_size*grid_size // 2

# test_results, avg_sim_times, avg_transfers = run_full_test(repetitions=repetitions, grid_size=grid_size, express_chance=express_chance, n_stations=n_stations)
# print("Algorithm timing results for " + str(repetitions) + " repetitions of a " + str(grid_size) + "x" + str(grid_size) 
#       + " grid with a " + str(express_chance) + " probability of express lines and " + str(n_stations) + " stations:")
# print("Total compute time: " + str(test_results))
# print("Average timesteps to goal: " + str(avg_sim_times))
# print("Average transfers to goal: " + str(avg_transfers))

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