from graph import Graph
from dfs import dfs


def test_dfs_traversal():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    result = dfs(graph, "A")

    assert result["traversal"] == ["A", "B", "D", "C"]