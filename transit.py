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
    
    def __init__(self, size: int, express_chance = 0.2, random_bus_start = False):

        self.time = 0
        self.size = size
        self.grid = [[TransitNode(False, x, y) for y in range(size)] for x in range(size)]
        self.vertical_routes = [TransitRoute(self, Direction.POS_Y, size, self.get_from_grid(i, 0), random.random() < express_chance, random_bus_start) for i in range(size)]
        self.horizontal_routes = [TransitRoute(self, Direction.POS_X, size, self.get_from_grid(0, i), random.random() < express_chance, random_bus_start) for i in range(size)]

    def __str__(self): # TODO

        out = "TransitGrid of size " + str(self.size) + " at " + str(self.time) + " minutes\n"

        for i in reversed(range(0, self.size*2)):
            out += self.get_print_line(i) + "\n"

        out += "KEY ( B = BUS; 2 = 2xBUS, X = STATION, @ = CUR_POINT; | - = ROUTE, e = EXPRESS ROUTE, G = GOAL )" + "\n"

        return out
    
    def step(self):

        self.time += 0.5

        for route in self.horizontal_routes:
            route.step()
        for route in self.vertical_routes:
            route.step()

    def add_station(self, x, y):
        self.set_grid_cell(x, y, TransitNode(True, x, y))

    def random_add_n_stations(self, n):

        rem = n

        while rem > 0:
            posX = random.randint(0, self.size-1)
            posY = random.randint(0, self.size-1)

            atPos = self.get_from_grid(posX, posY)

            if atPos and atPos.is_station:
                continue

            self.add_station(posX, posY)
            rem -= 1

        print("Successfully added " + str(n) + " stations to the grid!")

    def get_from_grid(self, x, y):
        return self.grid[x][y]
    
    def set_grid_cell(self, x, y, obj):
        self.grid[x][y] = obj

    def get_bus_char_at_grid_position(self, x, y):

        horizontal_route = self.horizontal_routes[y]
        vertical_route = self.vertical_routes[x]

        bus_horiz = horizontal_route.get_bus_pos() == (x,y)
        bus_vert = vertical_route.get_bus_pos() == (x,y)

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

    def get_print_line(self, n):
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
                    bus_char = self.get_bus_char_at_grid_position(x,y)

                    if bus_char != "":
                        out += bus_char
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

    def __init__(self, is_station: bool, pos_X: int, pos_Y: int):
        self.is_station = is_station
        self.pos_X = pos_X
        self.pos_Y = pos_Y

        # the S-score detailed in the proposal
        self.S = 0

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

        if randomize_bus_start:
            for i in range(random.randint(0,parent_grid.size*2)):
                self.step_bus_movement()

    def get_bus_pos(self):
        return self.bus_pos
    
    def get_bus_print_char(self):

        if self.bus_direction == Direction.POS_X:
            return "\033[94m→\033[0m"
        elif self.bus_direction == Direction.NEG_X:
            return "\033[94m←\033[0m"
        elif self.bus_direction == Direction.POS_Y:
            return "\033[94m↑\033[0m"
        elif self.bus_direction == Direction.NEG_Y:
            return "\033[94m↓\033[0m"
        
    def flip_bus(self):
        if self.bus_direction == Direction.NEG_X:
            self.bus_direction = Direction.POS_X
        elif self.bus_direction == Direction.POS_X:
            self.bus_direction = Direction.NEG_X
        elif self.bus_direction == Direction.NEG_Y:
            self.bus_direction = Direction.POS_Y
        elif self.bus_direction == Direction.POS_Y:
            self.bus_direction = Direction.NEG_Y

    def step_bus_movement(self):

        dx = 0
        dy = 0

        if self.bus_direction == Direction.NEG_X:
            dx = -0.5
        elif self.bus_direction == Direction.POS_X:
            dx = 0.5
        elif self.bus_direction == Direction.POS_Y:
            dy = 0.5
        elif self.bus_direction == Direction.NEG_Y:
            dy = -0.5

        if self.is_express:
            dx *= 2
            dy *= 2

        (cur_X, cur_Y) = self.bus_pos

        if cur_X + dx >= (self.parent_grid.size-0.5) or cur_X + dx < 0:
            self.flip_bus()
            dx *= -1

        if cur_Y + dy >= (self.parent_grid.size-0.5) or cur_Y + dy < 0:
            self.flip_bus()
            dy *= -1

        self.bus_pos = (cur_X + dx, cur_Y + dy)   

    def step(self): # TODO
        self.step_bus_movement()
