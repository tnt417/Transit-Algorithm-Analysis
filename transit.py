# REQUIREMENTS:
# Generic "TransitGrid" class: TransitRoute[], TransitNode[][],
# Generic "TransitAlgorithm" class, meant to be overriden: run_algorithm(grid)
# Main run_benchmarks function: Initialize each algorithm and time them.

from enum import Enum

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
    
    def __init__(self, size: int):

        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def __str__(self): # TODO

        out = ""

        for i in reversed(range(0, self.size*2)):
            out += self.get_print_line(i) + "\n"

        return out
    
    def add_station(self, x, y):
        self.set_grid_cell(x, y, TransitStation(x, y))

    def get_from_grid(self, x, y):
        return self.grid[x-1][y-1]
    
    def set_grid_cell(self, x, y, obj):
        self.grid[x-1][y-1] = obj

    def get_print_line(self, n):
        out = ""

        if n == 0: # print x coordinates
            out += "   ^"
            for i in range(1, self.size+1):
                out += str(i)
                if i != self.size:
                    out += "^^^"
        else:
            if n % 2 == 0: # print in-between lines (routes only)
                out += "  > "
                y = n//2

                for x in range(self.size):
                    out += "|"

                    if x != self.size-1:
                        out += "   "
            else: # print lines with nodes
                y = n//2 + 1

                if y < 10:
                    out += " " + str(y) + "> "
                else:
                    out += str(y) + "> "

                for x in range(self.size):
                    grid_element = self.get_from_grid(x,y)
                    if grid_element == None:
                        out += "o"
                    else:
                        out += str(grid_element)

                    if x != self.size-1:
                        out += "---"

                    

        return out

# DESC: Represents a 'Station' on the TransitGrid, printed as an X
class TransitStation: # TODO

    def __init__(self, pos_X: int, pos_Y: int):
        self.pos_X = pos_X
        self.pos_Y = pos_Y

        # the S-score detailed in the proposal
        self.S = 0

    def __str__(self):
        return "X"

class TransitRoute: # TODO

    def __init__(self, parent_grid: TransitGrid, direction: Direction, length: int, origin_node: TransitStation, is_express: bool):
        
        self.parent_grid = parent_grid
        self.direction = direction
        self.length = length
        self.origin_node = origin_node
        self.is_express = is_express

    def step(self): # TODO
        pass