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

    # Example representation when size = 5:
    # 5> X---0   0   0   0
    #  >     |
    # 4> 0   0---0---X   0
    #  >     |
    # 3> X   0   0   0   X
    #  >     |
    # 2> 0   0   0   0   0
    #  >     |
    # 1> 0   X   0   X   0
    #   ^1^^^2^^^3^^^4^^^5

    def __init__(self, size: int):

        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def __str__(self): # TODO

        out = ""

        return out

# DESC: Represents a 'Node' on the TransitGrid, printed as an X
class TransitNode: # TODO



    def __init__(self, pos_X: int, pos_Y: int):
        self.pos_X = pos_X
        self.pos_Y = pos_Y

class TransitRoute: # TODO
    # 
    def __init__(self, parent_grid: TransitGrid, direction: Direction, length: int, origin_node: TransitNode):
        pass