from app.algorithms.graph import Graph


def test_add_nodes_and_edges():
    g = Graph()
    g.add_node("A")
    g.add_edge("A", "B")
    assert "A" in g.nodes
    assert "B" in g.nodes


def test_undirected_neighbors():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    assert set(g.get_neighbors("A")) == {"B", "C"}
    assert set(g.get_neighbors("B")) == {"A"}


def test_directed_neighbors():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    assert g.get_neighbors("A") == ["B"]
    assert g.get_neighbors("B") == []


def _assert_raises(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return
    raise AssertionError(f"expected ValueError from {fn.__name__}")


def test_negative_weight_rejected():
    g = Graph(weighted=True)
    _assert_raises(g.add_edge, "A", "B", -1)


def test_self_loop_rejected():
    g = Graph()
    _assert_raises(g.add_edge, "A", "A")