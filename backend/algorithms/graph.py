class Graph:
    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self.nodes = set()
        self.edges = []

    def add_node(self, node):
        if node is None or node == "":
            raise ValueError("Node cannot be empty.")

        self.nodes.add(node)

    def add_edge(self, source, destination, weight=1):
        if source is None or source == "":
            raise ValueError("Source node cannot be empty.")

        if destination is None or destination == "":
            raise ValueError("Destination node cannot be empty.")

        if source == destination:
            raise ValueError("Self-loops are not allowed.")

        if self.weighted:
            if weight is None:
                raise ValueError("Weight is required for a weighted graph.")

            if weight < 0:
                raise ValueError(
                    "Edge weight cannot be negative for Dijkstra's algorithm."
                )

            self.edges.append((source, destination, weight))
        else:
            self.edges.append((source, destination))

        self.nodes.add(source)
        self.nodes.add(destination)

        if not self.directed:
            if self.weighted:
                self.edges.append((destination, source, weight))
            else:
                self.edges.append((destination, source))

    def get_neighbors(self, node):
        if node not in self.nodes:
            raise ValueError(f"Node '{node}' does not exist in the graph.")

        neighbors = []

        for edge in self.edges:
            if edge[0] == node:
                if self.weighted:
                    neighbors.append((edge[1], edge[2]))
                else:
                    neighbors.append(edge[1])

        return neighbors