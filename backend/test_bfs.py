import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import Graph
from bfs import bfs


class TestBFS(unittest.TestCase):

    def test_bfs_traversal(self):
        graph = Graph()

        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")

        result = bfs(graph, "A")

        self.assertEqual(
            result["traversal"],
            ["A", "B", "C", "D"]
        )


if __name__ == "__main__":
    unittest.main()