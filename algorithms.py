import itertools
from transit import TransitGrid, TransitNode
import heapq

class GraphNode:
    def __init__(self, station: TransitNode, arrival_time: float, actions = []):
        self.station = station
        self.edges = []

        # arrival_time is the same as total cost to get to the node through this edge, but is
        # needed to fetch bus departure times
        self.arrival_time = arrival_time
        self.actions = actions

class GraphEdge:
    def __init__(self, from_node: TransitNode, to_node: TransitNode, weight: float):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

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

    def expand_node(self, root_node: GraphNode):

        for nbr in root_node.station.neighbor_stations:
            root_node.edges.append(GraphEdge(root_node, nbr, self.get_transfer_time(root_node.station, nbr, root_node.arrival_time)))

    def get_path(self, grid: TransitGrid):

        (start_x, start_y) = grid.passenger.cur_pos
        start_station = grid.get_from_grid(start_x, start_y)

        (goal_x, goal_y) = grid.passenger.goal_pos
        goal_station = grid.get_from_grid(goal_x, goal_y)

        frontier = []
        i = 0  # Simple integer tie-breaker

        heapq.heappush(frontier, (0, i, start_station, []))  # (time_so_far, order, station, actions_so_far)

        best_times = {(start_station.pos_X, start_station.pos_Y): 0}

        while frontier:
            curr_time, _, curr_station, actions = heapq.heappop(frontier)

            if curr_station == goal_station:
                return actions, curr_time  # return final list of actions and total time

            for neighbor in curr_station.neighbor_stations:
                (time_to_board, time_to_unboard) = self.get_transfer_time(curr_station, neighbor, grid.time + curr_time)
                new_time = curr_time + time_to_board + time_to_unboard

                key = (neighbor.pos_X, neighbor.pos_Y)

                if key not in best_times or new_time < best_times[key]:
                    best_times[key] = new_time

                    new_actions = list(actions)  # copy actions list

                    moving_vert = curr_station.pos_X == neighbor.pos_X
                    moving_horiz = curr_station.pos_Y == neighbor.pos_Y

                    if moving_vert:
                        new_actions.append((curr_time + time_to_board, "boardVert"))
                    elif moving_horiz:
                        new_actions.append((curr_time + time_to_board, "boardHoriz"))
                    else:
                        # Should never happen in a clean grid
                        raise ValueError("Neighbor is neither vertical nor horizontal.")

                    new_actions.append((new_time, "unboard"))

                    i += 1
                    heapq.heappush(frontier, (new_time, i, neighbor, new_actions))

        return None, float('inf')
        

class ConnectionAlgorithm(Algorithm):
    def __init__(self):
        pass

    def get_path(self, grid: TransitGrid):
        pass