from app.algorithms.graph import Graph
from app.algorithms.dijkstra import dijkstra


def test_dijkstra_shortest_path():
    graph = Graph(weighted=True)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "D", 1)
    graph.add_edge("C", "D", 3)

    result = dijkstra(graph, "A", "D")

    assert result["distances"]["D"] == 5
    assert result["path"] in [
        ["A", "B", "D"],
        ["A", "C", "D"]
    ]