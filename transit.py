# REQUIREMENTS:
# Generic "TransitGrid" class: TransitRoute[], TransitNode[][],
# Generic "TransitAlgorithm" class, meant to be overriden: run_algorithm(grid)
# Main run_benchmarks function: Initialize each algorithm and time them.

from enum import Enum
import random

class Direction(Enum): # TODO
    NEG_X = 1
    POS_X = 2
    NEG_Y = 3
    POS_Y = 4

class TransitGrid: # TODO

    # SAMPLE PRINT
    # TransitGrid: Size = 5
    # 5> X---X   .   .   .
    #  > E   |
    # 4> E   X-------X   .
    #  > E   B       |
    # 3> X---o---B---o---G
    #  > E   |       |   |
    # 2> E   |   .   B   |
    #  > E   |       |   |
    # 1> @---X---0---X---B
    #   ^1^^^2^^^3^^^4^^^5
    # KEY ( B = BUS; 2 = 2xBUS, X = STATION; @ = CUR_POINT; - | o = ROUTE, E = EXPRESS ROUTE, G = GOAL )
    
    def __init__(self, size: int, express_chance = 0.2, random_bus_start = False, seed = -1, n_stations = 50):

        # self.passengers = []

        # seed to -1 for random seed
        if seed != -1:
            random.seed(seed)

        self.time = 0
        self.size = size
        self.grid = [[TransitNode(False, x, y, self) for y in range(size)] for x in range(size)]
        self.vertical_routes = [TransitRoute(self, Direction.POS_Y, size, self.get_from_grid(i, 0), random.random() < express_chance, random_bus_start) for i in range(size)]
        self.horizontal_routes = [TransitRoute(self, Direction.POS_X, size, self.get_from_grid(0, i), random.random() < express_chance, random_bus_start) for i in range(size)]

        self.stations = []
        self.random_add_n_stations(n_stations)
        self.update_station_neighbors()

        self.passenger = TransitPassenger(self.get_random_station().get_pos(), self.get_random_station().get_pos(), self)

    def update_station_neighbors(self):
        for s in self.stations:
            for vert_station in self.vertical_routes[s.pos_X].stations:
                if vert_station == s:
                    continue
                s.notify_add_neighbor_station(vert_station)
            for horiz_station in self.horizontal_routes[s.pos_Y].stations:
                if horiz_station == s:
                    continue
                s.notify_add_neighbor_station(horiz_station)

    def __str__(self): # TODO

        out = "TransitGrid of size " + str(self.size) + " at " + str(self.time) + " minutes\n"

        for i in reversed(range(0, self.size*2)):
            out += self.get_print_line(i) + "\n"

        out += "KEY{\033[94m→←↑↓2\033[0m = BUS; X = STATION; \033[92m@\033[0m = PASSENGER; \033[92mG\033[0m = GOAL; | - = ROUTE, e = EXPRESS ROUTE}" + "\n"

        return out
    
    def step(self):

        self.time += 0.5

        for route in self.horizontal_routes:
            route.step()
        for route in self.vertical_routes:
            route.step()

    def add_station(self, x, y):
        station = TransitNode(True, x, y, self)
        self.set_grid_cell(x, y, station)
        self.stations.append(station)

        self.vertical_routes[x].notify_add_station(station)
        self.horizontal_routes[y].notify_add_station(station)

    def get_random_station(self):
        return random.choice(self.stations)

    def TEST_manual_board(self):

        if self.passenger.boarded:
            self.try_unboard_passenger(self.passenger)
            return

        for r in self.vertical_routes:
            if self.try_board_passenger(r, self.passenger):
                return
            
        for r in self.horizontal_routes:
            if self.try_board_passenger(r, self.passenger):
                return

    def take_action(self, action: str):
        if action == "boardHoriz":
            self.try_board_passenger(self.horizontal_routes[int(self.passenger.cur_pos[1])], self.passenger)
        elif action == "boardVert":
            self.try_board_passenger(self.vertical_routes[int(self.passenger.cur_pos[0])], self.passenger)
        elif action == "unboard":
            self.try_unboard_passenger(self.passenger)
        else:
            raise RuntimeError("Invalid action!")

    # TODO: check that boarding/unboarding happens at stations only
    def try_board_passenger(self, route: "TransitRoute", passenger: "TransitPassenger"):

        passenger_node = self.get_from_grid(passenger.cur_pos[0], passenger.cur_pos[1])

        if route.bus_pos != passenger.cur_pos or not passenger_node.is_station:
            return False
        
        route.board_passenger(passenger)

    def try_unboard_passenger(self, passenger: "TransitPassenger"):

        # fails if bus is at not at the station
        if passenger.route.get_bus_station() == None:
            return False
        
        passenger.route.unboard_passenger(passenger)

    def random_add_n_stations(self, n):
        rem = n

        while rem > 0:

            # calculate S values for the grid
            S_counts = {(x, y): len(self.horizontal_routes[y].stations) + len(self.vertical_routes[x].stations)
                        for x in range(self.size)
                        for y in range(self.size)
                        if not self.get_from_grid(x, y).is_station
                        }

            min_S = min(S_counts.values())

            candidates = [pos for pos, s in S_counts.items() if s == min_S]

            (posX, posY) = random.choice(candidates)
            self.add_station(posX, posY)
            
            rem -= 1

    def get_from_grid(self, x, y):

        if int(x) != x or int(y) != y:
            return None

        return self.grid[int(x)][int(y)]
    
    def set_grid_cell(self, x, y, obj):
        self.grid[x][y] = obj

    def get_bus_char_at_grid_position(self, x, y):

        horizontal_route = self.horizontal_routes[y]
        vertical_route = self.vertical_routes[x]

        bus_horiz = horizontal_route.get_bus_pos() == (x,y)
        bus_vert = vertical_route.get_bus_pos() == (x,y)

        if bus_horiz and horizontal_route.boarded_passenger != None:
            return horizontal_route.get_bus_print_char()
        
        if bus_vert and vertical_route.boarded_passenger != None:
            return vertical_route.get_bus_print_char()

        if bus_horiz and bus_vert:
            return "\033[94m2\033[0m"
        
        if bus_horiz:
            return horizontal_route.get_bus_print_char()
        
        if bus_vert:
            return vertical_route.get_bus_print_char()
        
        return ""
    
    def get_intermediate_bus_char_vertical(self, x, y_dec):

        vertical_route = self.vertical_routes[x]

        bus_vert = vertical_route.get_bus_pos() == (x,y_dec)
        
        if bus_vert:
            return vertical_route.get_bus_print_char()
        
        return ""
    
    def get_intermediate_bus_char_horizontal(self, x_dec, y):

        horizontal_route = self.horizontal_routes[y]

        bus_horiz = horizontal_route.get_bus_pos() == (x_dec,y)
        
        if bus_horiz:
            return horizontal_route.get_bus_print_char()
        
        return ""

    def get_random_grid_pos(self):
        return (random.randint(0, self.size-1), random.randint(0, self.size-1))
    
    def passenger_at_goal(self):
        return self.passenger.cur_pos == self.passenger.goal_pos
    
    # def add_n_passengers(self, n):
    #     for i in range(n):
    #         self.passengers.append(TransitPassenger(self.get_random_grid_pos(), self.get_random_grid_pos, self))

    # def passengers_at_pos(self, pos):

    #     n = 0

    #     for p in self.passengers:
    #         if p.cur_pos == pos:
    #             n += 1

    #     return n

    def get_print_line(self, n: int):
        out = ""

        if n == 0: # print x coordinates
            out += "   ^"
            for i in range(0, self.size):
                out += str(i)
                if i != self.size-1:
                    out += "^^^"
        else:
            if n % 2 == 0: # print in-between lines (routes only)
                out += "  > "

                y = n//2

                for x in range(self.size):
                    intermed_bus = self.get_intermediate_bus_char_vertical(x, y - 0.5)

                    if intermed_bus != "":
                        out += intermed_bus
                    elif self.vertical_routes[x].is_express:
                        out += "e"
                    else:
                        out += "|"

                    if x != self.size-1:
                        out += "   "
            else: # print lines with nodes
                y = n//2

                if y < 10:
                    out += " " + str(y) + "> "
                else:
                    out += str(y) + "> "

                for x in range(self.size):
                    transit_char = self.get_bus_char_at_grid_position(x,y)

                    # n_passengers = self.passengers_at_pos((x,y))

                    # if n_passengers > 0:
                    #     bus_char = str(n_passengers)

                    if self.passenger.cur_pos == (x,y):
                        transit_char = "\033[92m@\033[0m"

                    if self.passenger.goal_pos == (x,y):
                        transit_char = "\033[92mG\033[0m"

                    if transit_char != "":
                        out += transit_char
                    else:
                        grid_element = self.get_from_grid(x,y)
                        out += str(grid_element)

                    if x != self.size-1:
                        intermed_bus = self.get_intermediate_bus_char_horizontal(x + 0.5, y)

                        if self.horizontal_routes[y].is_express:
                            out += "e"
                            if intermed_bus != "":
                                out += intermed_bus
                            else:
                                out += "e"
                            out += "e"
                        else:
                            out += "-"
                            if intermed_bus != "":
                                out += intermed_bus
                            else:
                                out += "-"
                            out += "-"

                    

        return out

# DESC: Represents a 'Station' on the TransitGrid, printed as an X
class TransitNode: # TODO

    def __init__(self, is_station: bool, pos_X: int, pos_Y: int, parent_grid: TransitGrid):
        self.is_station = is_station
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.neighbor_stations = []
        self.parent_grid = parent_grid

        # the S-score detailed in the proposal, for generation only
        # TODO
        self.S = 0

    def notify_add_neighbor_station(self, node: "TransitNode"):
        self.neighbor_stations.append(node)

    def get_pos(self):
        return (self.pos_X, self.pos_Y)

    def __str__(self):
        if self.is_station:
            return "X"
        else:
            return "o"

class TransitRoute: # TODO

    def __init__(self, parent_grid: TransitGrid, direction: Direction, length: int, origin_node: TransitNode, is_express: bool, randomize_bus_start: bool):
        
        self.parent_grid = parent_grid
        self.direction = direction
        self.length = length
        self.origin_node = origin_node
        self.is_express = is_express
        self.bus_pos = origin_node.get_pos()
        self.bus_direction = direction
        self.boarded_passenger = None
        self.stations = []

        if randomize_bus_start:
            for i in range(random.randint(0,parent_grid.size*2)):
                self.step_bus_movement()

        self.start_direction = self.bus_direction
        self.start_pos = self.bus_pos

    def notify_add_station(self, station: TransitNode):
        self.stations.append(station)

    def get_bus_pos(self):
        return self.bus_pos
    
    def get_random_pos(self):
        if self.direction == Direction.POS_X:
            return (random.randint(0, self.parent_grid.size-1), self.start_pos[1])
        else:
            return (self.start_pos[0], random.randint(0, self.parent_grid.size-1))
    
    def get_bus_station(self):

        for s in self.stations:
            if self.bus_pos == s.get_pos():
                return s
        
        return None
    
    def get_bus_print_char(self):
        if self.boarded_passenger != None:
            return "\033[94m@\033[0m"
        elif self.bus_direction == Direction.POS_X:
            return "\033[94m→\033[0m"
        elif self.bus_direction == Direction.NEG_X:
            return "\033[94m←\033[0m"
        elif self.bus_direction == Direction.POS_Y:
            return "\033[94m↑\033[0m"
        elif self.bus_direction == Direction.NEG_Y:
            return "\033[94m↓\033[0m"
        
    def get_opposing_direction(direction):
        if direction == Direction.NEG_X:
            return Direction.POS_X
        elif direction == Direction.POS_X:
            return Direction.NEG_X
        elif direction == Direction.NEG_Y:
            return Direction.POS_Y
        elif direction == Direction.POS_Y:
            return Direction.NEG_Y

    def flip_bus(self):
        self.bus_direction = TransitRoute.get_opposing_direction(self.bus_direction)

    def get_movement(self, direction: Direction, timestep: int = 0.5):

        dx = 0
        dy = 0

        if direction == Direction.NEG_X:
            dx = -timestep
        elif direction == Direction.POS_X:
            dx = timestep
        elif direction == Direction.POS_Y:
            dy = timestep
        elif direction == Direction.NEG_Y:
            dy = -timestep

        if self.is_express:
            dx *= 2
            dy *= 2

        return dx, dy

    def time_until_bus(self, station: TransitNode, start_time: float):
        if station not in self.stations:
            raise RuntimeError("Station will never be visited by route: not on route")

        # for regular routes: cycle every 2*(size-1) minutes
        # for express routes: cycle every size-1 minutes
        # modulus by this value to get the "cycle time"
        # at that point, we can simulate from starting time
        # and run until 

        if self.is_express:
            cycle_time = self.parent_grid.size-1
        else:
            cycle_time = 2*(self.parent_grid.size-1)

        time_normalized = start_time % cycle_time
        time_step = 0.5

        simul_pos = self.start_pos
        simul_dir = self.start_direction

        timer = 0

        while timer < time_normalized:
            dx, dy = self.get_movement(simul_dir)
            simul_pos, simul_dir = self.move_bus(simul_pos, simul_dir, dx, dy)
            timer += time_step

        timer = 0

        while True:
            if simul_pos == station.get_pos():
                return timer

            dx, dy = self.get_movement(simul_dir)
            simul_pos, simul_dir = self.move_bus(simul_pos, simul_dir, dx, dy)
            timer += time_step

    def move_bus(self, pos, direction, dx, dy):
        (cur_X, cur_Y) = pos

        new_X = cur_X + dx
        new_Y = cur_Y + dy
        new_dir = direction

        if new_X >= (self.parent_grid.size-0.5) or new_X < 0:
            new_dir = TransitRoute.get_opposing_direction(new_dir)
            new_X = cur_X - dx

        if new_Y >= (self.parent_grid.size-0.5) or new_Y < 0:
            new_dir = TransitRoute.get_opposing_direction(new_dir)
            new_Y = cur_Y - dy

        return (new_X, new_Y), new_dir

    def step_bus_movement(self):

        dx, dy = self.get_movement(self.bus_direction)

        (new_X, new_Y), new_dir = self.move_bus(self.bus_pos, self.bus_direction, dx, dy)

        self.bus_pos = (new_X, new_Y)
        self.bus_direction = new_dir   

    def step(self): # TODO
        self.step_bus_movement()

    def board_passenger(self, passenger: "TransitPassenger"):
        passenger.set_route(self)
        self.boarded_passenger = passenger

    def unboard_passenger(self, passenger: "TransitPassenger"):
        passenger.set_route(None)
        passenger.cur_pos = self.bus_pos
        self.boarded_passenger = None


class TransitPassenger:

    def __init__(self, start_pos: tuple[int, int], goal_pos: tuple[int, int], parent_grid: TransitGrid):
        self.cur_pos = start_pos
        self.goal_pos = goal_pos
        self.parent_grid = parent_grid
        self.boarded = False
        self.route = None

    def set_route(self, route: TransitRoute):
        self.route = route
        self.boarded = (route != None)
        if self.boarded:
            self.cur_pos = (-1, -1)