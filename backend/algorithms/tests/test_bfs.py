from graph import Graph
from bfs import bfs


def test_bfs_traversal():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    result = bfs(graph, "A")

    assert result["traversal"] == ["A", "B", "C", "D"]