from graph import Graph
from dijkstra import dijkstra


graph = Graph(weighted=True)

graph.add_edge("A", "B", 4)
graph.add_edge("A", "C", 2)
graph.add_edge("B", "D", 1)
graph.add_edge("C", "D", 3)

result = dijkstra(graph, "A", "D")

print("Distances:", result["distances"])
print("Shortest path:", result["path"])

print("Dijkstra states:")

for state in result["states"]:
    print(state)