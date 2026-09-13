from graph import Graph
from dfs import dfs


graph = Graph()

graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")

result = dfs(graph, "A")

print("DFS traversal:", result["traversal"])
print("DFS states:")

for state in result["states"]:
    print(state)