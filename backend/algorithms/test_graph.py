from graph import Graph

graph = Graph()

graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")

print("Nodes:", graph.nodes)
print("Edges:", graph.edges)
print("Neighbors of A:", graph.get_neighbors("A"))