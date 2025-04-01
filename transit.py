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

        return out

# DESC: Represents a 'Station' on the TransitGrid, printed as an X
class TransitStation: # TODO

    def __init__(self, pos_X: int, pos_Y: int):
        self.pos_X = pos_X
        self.pos_Y = pos_Y

        # the S-score detailed in the proposal
        self.S = 0

class TransitRoute: # TODO

    def __init__(self, parent_grid: TransitGrid, direction: Direction, length: int, origin_node: TransitStation, is_express: bool):
        
        self.parent_grid = parent_grid
        self.direction = direction
        self.length = length
        self.origin_node = origin_node
        self.is_express = is_express

    def step(self): # TODO
        pass