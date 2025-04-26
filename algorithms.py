from transit import TransitGrid, TransitNode


class GraphNode:
    def __init__(self, station: TransitNode, arrival_time: float ):
        self.station = station
        self.edges = []

        # arrival_time is the same as total cost to get to the node through this edge, but is
        # needed to fetch bus departure times
        self.arrival_time = arrival_time

class GraphEdge:
    def __init__(self, from_node: TransitNode, to_node: TransitNode, weight: float):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

class Algorithm:
    
    def __init__(self):
        pass

    def run(self, grid: TransitGrid):
        pass

class RaptorAlgorithm(Algorithm):
    def __init__(self):
        pass

    def run(self, grid: TransitGrid):
        pass

class DijkstraAlgorithm(Algorithm):
    def __init__(self):
        pass

    def run(self, grid: TransitGrid):
        pass

class DrtAlgorithm(Algorithm):
    def __init__(self):
        pass

    def run(self, grid: TransitGrid):
        pass