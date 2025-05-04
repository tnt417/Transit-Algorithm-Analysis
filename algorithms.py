import itertools
import math
from transit import TransitGrid, TransitNode, TransitRoute
import heapq
import sys


# class RaptorRoute:
#     def __init__(self):
#         self.stops = []
#         self.trip_interval = 0

#     def __str__(self):
#         return f"RaptorRoute: <interval: {self.interval}, stops: {self.stops}>"


# class RaptorPosition:
#     def __init__(self, pos):
#         self.x = pos[0]
#         self.y = pos[1]
#         self.routes = set()
#         self.stops = set()
#         self.times_by_round = {}  # Allows for easy gaps, I am lazy
#         self.earliest_time = sys.maxsize


# class RaptorScheduledStop:
#     def __init__(self, x, y, t, route):
#         # All routes can be transferred between in 0.1 (above 0) time units
#         self.x = x
#         self.y = y
#         self.t = t
#         self.route = route

#     def get_pos(self):
#         return (self.x, self.y)

#     def __str__(self):
#         return f"RaptorStop: <x: {self.x}, y: {self.y}, t: {self.t}, rounds: {self.times_by_round}, earliest: {self.earliest_time}"


class Algorithm:
    def __init__(self):
        pass

    def get_path(self, grid: TransitGrid):
        pass


# class RaptorAlgorithm(Algorithm):
#     def __init__(self):
#         self.dijkstra = DijkstraAlgorithm() # FIXME: Remove

#     def get_trip_from_stop_time(self, route: RaptorRoute, time: int):
#         return int(time % (route.trip_interval))

#     def get_time_from_stop_and_trip(self, route: RaptorRoute, stop: RaptorScheduledStop, trip_num: int):
#         return stop.t + trip_num * route.trip_interval

#     def get_earliest_trip(self, route: RaptorRoute, stop: RaptorScheduledStop, time: int):
#         return math.ceil((time - stop.t) / route.trip_interval)

#     def build_route_data(self, route: TransitRoute):
#         route_data = RaptorRoute()
#         step = 0.5 if route.is_express else 1
#         t = 0
#         for station in route.stations:
#             route_data.stops.append(RaptorScheduledStop(
#                 station.pos_X,
#                 station.pos_Y,
#                 t,
#                 route_data))
#             t += step

#         # Create the reverse direction's timetable
#         for stop in reversed(route_data.stops):
#             route_data.stops.append(RaptorScheduledStop(
#                 stop.x,
#                 stop.y,
#                 t,
#                 route_data))
#             t += step

#         route_data.trip_interval = t
#         return route_data

#     def get_raptor_data(self, grid: TransitGrid):
#         routes = set()
#         pos_data = {}
#         for route in itertools.chain(grid.vertical_routes, grid.horizontal_routes):
#             route_data = self.build_route_data(route)
#             routes.add(route_data)

#             for stop in route_data.stops:
#                 pos = stop.get_pos()
#                 if pos not in pos_data:
#                     pos_data[pos] = RaptorPosition(pos)
#                 pos_data[pos].routes.add(route)
#                 pos_data[pos].stops.add(stop)

#         return (routes, pos_data)

#     def generate_actions_from_path(self, grid): # FIXME: Fix arguments
#         # FIXME: Reassemble properly
#         # Use dijkstra for now so it does not break
#         # Reference: https://ljn.io/posts/raptor-journey-planning-algorithm
#         return self.dijkstra.get_path(grid)

#     def get_path(self, grid: TransitGrid):
#         route_data, pos_data = self.get_raptor_data(grid)
#         start_pos = grid.passenger.cur_pos

#         end_pos = grid.passenger.goal_pos

#         round_num = 0
#         marked_positions = [start_pos]

#         pos_data[start_pos].earliest_time = 0
#         pos_data[start_pos].times_by_round[0] = 0

#         #print(route_data)

#         while len(marked_positions) > 0:
#             round_num += 1
#             Q = {}

#             for pos in marked_positions:
#                 for stop in pos_data[pos].stops:
#                     r = stop.route
#                     if (r in Q and Q[r].t < stop.t) or r not in Q:
#                         Q[r] = stop

#             marked_positions = []  # Clear all markings

#             for route, stop in Q.items():
#                 trip = None
#                 found_start = False
#                 for route_stop in route.stops:
#                     if not (found_start or
#                             route_stop.x != stop.x or
#                             route_stop.y != stop.y):
#                         continue

#                     pos = stop.get_pos()
#                     if trip is not None:
#                         earliest_stop_time = pos_data[stop.get_pos()].earliest_time
#                         earliest_target_time = pos_data[end_pos].earliest_time
#                         if earliest_stop_time is None:
#                             earliest_stop_time = sys.maxsize
#                         if earliest_target_time is None:
#                             earliest_target_time = sys.maxsize

#                         arrive_time = self.get_time_from_stop_and_trip(
#                             route,
#                             route_stop,
#                             trip)
#                         if arrive_time < min(earliest_stop_time,
#                                              earliest_target_time):
#                             pos_data[pos].earliest_time = arrive_time
#                             pos_data[pos].times_by_round[round_num] = arrive_time
#                             marked_positions.append(pos)

#                     cur_time = pos_data[pos].times_by_round.get(round_num)
#                     prev_time = pos_data[pos].times_by_round.get(round_num - 1)
#                     if cur_time is None:
#                         cur_time = sys.maxsize
#                     if prev_time is None:
#                         prev_time = sys.maxsize
#                     if prev_time <= cur_time:
#                         trip = self.get_earliest_trip(route, stop, prev_time)

#             # We skip the footpath stage since all transfers are assumed to be
#             # the same station. Talk about this in our report as a limitation

#         return self.generate_actions_from_path(grid)


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

class RaptorAlgorithm(Algorithm):
    def __init__(self, max_rounds: int = 10):
        self.max_rounds = max_rounds

    def get_path(self, grid: TransitGrid):

        # print(grid)

        start_pos = grid.passenger.cur_pos
        goal_pos = grid.passenger.goal_pos
        time = grid.time

        if start_pos == goal_pos:
            return [], time

        # arrival times for each round
        arrival_times = [{s.get_pos(): float('inf') for s in grid.stations}
                         for _ in range(self.max_rounds + 1)]
        
        # arrive at the start pos at time = 0
        arrival_times[0][start_pos] = time

        # track predecessors to construct actions for the path for a given round
        round_predecessors = [ {} for _ in range(self.max_rounds+1) ]

        # stops that were traveled to on the previous round
        marked_stops = set()
        marked_stops.add(start_pos)

        # inside get_path, before your main loop
        arrival_round: dict[tuple,int] = {}   # (x,y) → the round it was first reached
        arrival_round[start_pos] = 0

        for round_num in range(1, self.max_rounds + 1):

            updated_stops = set()

            for pos in marked_stops:

                x, y = pos
                node = grid.get_from_grid(x, y)

                if not node.is_station:
                    continue

                for route in [grid.horizontal_routes[y], grid.vertical_routes[x]]:
                    # Forward scan of this route

                    curr_time = arrival_times[round_num - 1][pos]

                    neighbors_on_route = [st for st in node.neighbor_stations if st in route.stations and st is not node]

                    # simulate arrival times
                    for nbr in neighbors_on_route:

                        dep_time = curr_time + route.time_until_bus(node, curr_time)
                        arr_time = dep_time + route.time_until_bus(nbr, dep_time)

                        to_pos = (nbr.pos_X, nbr.pos_Y)

                        # print("Found nbr: " + str(to_pos) + " departs at " + str(dep_time) + " arrives at " + str(arr_time))

                        if arr_time < arrival_times[round_num][to_pos]:

                            if to_pos not in arrival_round:
                                arrival_round[to_pos] = round_num

                            arrival_times[round_num][to_pos] = arr_time
                            round_predecessors[round_num][to_pos] = (pos, dep_time, arr_time)
                            # print("Setting pred of " + str(to_pos) + " as " + str(pos))
                            updated_stops.add(to_pos)

            # print("New pred: " + str(pred))

            # print("Round num: " + str(round_num))

            # print("Round's arrival times: " + str(arrival_times[round_num]))

            # print("Updated stops: " + str(updated_stops))

            if goal_pos in updated_stops:
                break

            marked_stops = updated_stops

            # if no stops are updated, end early
            if not updated_stops:
                break

        # print(str(predecessors))

        actions = []
        cur_pos = goal_pos
        r = arrival_round[cur_pos]

        goal_arrive_time = arrival_times[r][goal_pos]

        while r > 0:
            prev_pos, dep_time, arr_time = round_predecessors[r][cur_pos]

            actions.append((arr_time, "unboard"))

            if prev_pos[0] == cur_pos[0]:
                actions.append((dep_time, "boardVert"))
            else:
                actions.append((dep_time, "boardHoriz"))

            #print(actions)

            cur_pos = prev_pos
            r = arrival_round[cur_pos]

        actions.reverse()
        return actions, goal_arrive_time