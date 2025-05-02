import itertools
from transit import TransitGrid, TransitNode
import heapq

class Algorithm:
    
    def __init__(self):
        pass

    def get_path(self, grid: TransitGrid):
        pass

class RaptorAlgorithm(Algorithm):
    def __init__(self):
        pass

    def get_path(self, grid: TransitGrid):
        pass

class DijkstraAlgorithm(Algorithm):
    
    def __init__(self):
        pass

    def get_transfer_time(self, from_node: TransitNode, to_node: TransitNode, start_time: float):

        inline_v = from_node.pos_X == to_node.pos_X
        inline_h = from_node.pos_Y == to_node.pos_Y

        if inline_v:
            shared_route = from_node.parent_grid.vertical_routes[from_node.pos_X]
        elif inline_h:
            shared_route = from_node.parent_grid.horizontal_routes[from_node.pos_Y]

        time_to_board = shared_route.time_until_bus(from_node, start_time)
        time_to_unboard = shared_route.time_until_bus(to_node, start_time+time_to_board)

        return (time_to_board, time_to_unboard)

        # find shared route between the stations
        # first thing: when will a bus be at this station?
        # then: how long until it will be at station b?

        pass

    def get_path(self, grid: TransitGrid):

        if grid.passenger.cur_pos == grid.passenger.goal_pos:
            return [], 0

        (start_x, start_y) = grid.passenger.cur_pos
        start_station = grid.get_from_grid(start_x, start_y)

        (goal_x, goal_y) = grid.passenger.goal_pos
        goal_station = grid.get_from_grid(goal_x, goal_y)

        frontier = []

        # tie breaker for the priority queue
        i = 0

        # in frontier we store: (time_required, order_added, station, actions_to_station)
        heapq.heappush(frontier, (0, i, start_station, []))

        # store the best time to get to a given 
        best_times = {(start_station.pos_X, start_station.pos_Y): 0}

        while frontier:
            # pop the lowest arrival time node in the frontier
            curr_time, _, curr_station, actions = heapq.heappop(frontier)

            if curr_station == goal_station:
                # return final list of actions and total time to destination
                return actions, curr_time

            for neighbor in curr_station.neighbor_stations:
                (time_to_board, time_to_unboard) = self.get_transfer_time(curr_station, neighbor, grid.time + curr_time)
                new_time = curr_time + time_to_board + time_to_unboard

                key = (neighbor.pos_X, neighbor.pos_Y)

                if key not in best_times or new_time < best_times[key]:
                    best_times[key] = new_time

                    new_actions = list(actions)

                    moving_vert = curr_station.pos_X == neighbor.pos_X
                    moving_horiz = curr_station.pos_Y == neighbor.pos_Y

                    if moving_vert:
                        new_actions.append((curr_time + time_to_board, "boardVert"))
                    elif moving_horiz:
                        new_actions.append((curr_time + time_to_board, "boardHoriz"))

                    new_actions.append((new_time, "unboard"))

                    i += 1
                    heapq.heappush(frontier, (new_time, i, neighbor, new_actions))

        return None, float('inf')
        
import copy

class ConnectionAlgorithm(Algorithm):
    def __init__(self):
        pass

    CYCLES_REQUIRED_CONSTANT = 2.5

    # takes advantage of the fact that bus movement is cyclic
    # and repeats every (size-1)*2 minutes
    def get_connections_list(self, grid:TransitGrid):
        # stores (fromStation:coordinate, departureTime:float, toStation:coordinate, arrivalTime:float)
        connections: list[tuple[tuple[int,int], float, tuple[int,int], float]] = []

        routes = grid.horizontal_routes + grid.vertical_routes

        # simulate 4 cycles for each route
        for route in routes:
            sim_time = 0
            cycle_length = (grid.size-1)*2

            # EX: if we store that we visited station A when sim_time = 5,
            # and we encounter station B when sim_time = 7, we have enough info to
            # populate a connection. then if we encounter station C when sim_time = 10, we once again
            # can populate connections, this time for A->C and B->C
            station_visit_times = {}

            bus_pos = route.bus_pos
            bus_dir = route.bus_direction

            def simulate_step(bus_pos, bus_dir, sim_time):
                (dx, dy) = route.get_movement(bus_dir)
                bus_pos, bus_dir = route.move_bus(bus_pos, bus_dir, dx, dy)

                return bus_pos, bus_dir, sim_time + 0.5

            while sim_time < cycle_length * self.CYCLES_REQUIRED_CONSTANT:

                cur_station = grid.get_from_grid(bus_pos[0], bus_pos[1])

                if not cur_station or not cur_station.is_station:
                    bus_pos, bus_dir, sim_time = simulate_step(bus_pos, bus_dir, sim_time)
                    continue

                cur_pos = (bus_pos[0], bus_pos[1])

                for pos,dep_time in station_visit_times.items():

                    # CSA dictates that connections with identical dep and arr stations are invalid
                    if pos == cur_pos:
                        continue

                    connections.append((pos, dep_time, cur_station.get_pos(), sim_time))

                station_visit_times[cur_pos] = sim_time

                bus_pos, bus_dir, sim_time = simulate_step(bus_pos, bus_dir, sim_time)
            
        # sort connections by departure time
        connections.sort(key=lambda c: c[1])

        return connections

                



    #def offset_connections_list(self, grid:TransitGrid):


    def get_path(self, grid: TransitGrid):

        if grid.passenger.cur_pos == grid.passenger.goal_pos:
            return [], 0

        # stores (fromStation:TransitNode, departureTime:float, toStation:TransitNode, arrivalTime:float)
        connections = self.get_connections_list(grid)

        # map each station to earliest arrival time, defaulting to 'inf'
        earliest_arrival = {pos: float('inf') for (dep_pos, dep_time, arr_pos, arr_time) in connections for pos in [dep_pos, arr_pos]}
        earliest_arrival[grid.passenger.cur_pos] = grid.time

        # needed to reconstruct the path
        predecessors = {}

        for (dep_pos, dep_time, arr_pos, arr_time) in connections:
            # if dep_time is after the earliest arrival to the station,
            # connection can be taken
            if dep_time >= earliest_arrival[dep_pos]:
                # if the connection would lead to an earlier arrival time at
                # the station, update the earliest arrival and predeccesor
                if arr_time < earliest_arrival[arr_pos]:
                    earliest_arrival[arr_pos] = arr_time
                    predecessors[arr_pos] = (dep_pos, dep_time, arr_pos, arr_time)

        goal = grid.passenger.goal_pos

        if goal not in predecessors:
            raise ValueError("No path found!")

        actions = []
        cur_pos = goal

        while cur_pos in predecessors:
            (dep_pos, dep_time, arr_pos, arr_time) = predecessors[cur_pos]

            actions.append((arr_time, "unboard"))

            if dep_pos[0] == arr_pos[0]:
                actions.append((dep_time, "boardVert"))
            else:
                actions.append((dep_time, "boardHoriz"))

            cur_pos = dep_pos

        actions.reverse()

        return actions, earliest_arrival[goal]