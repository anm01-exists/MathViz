from fastapi import FastAPI
from graph import Graph
from bfs import bfs
from dfs import dfs
from dijkstra import dijkstra


def clean_json(data):
    """
    Convert values that cannot be safely returned as JSON.
    Dijkstra uses infinity (inf) for unknown distances,
    so we convert inf to None.
    """

    if isinstance(data, dict):
        return {
            key: clean_json(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [
            clean_json(value)
            for value in data
        ]

    if data == float("inf"):
        return None

    return data


app = FastAPI(title="MathViz Graph API")


@app.get("/")
def home():
    return {
        "message": "MathViz Graph API is running"
    }


@app.get("/bfs")
def run_bfs(start: str = "A"):
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    result = bfs(graph, start)

    return clean_json(result)


@app.get("/dfs")
def run_dfs(start: str = "A"):
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    result = dfs(graph, start)

    return clean_json(result)


@app.get("/dijkstra")
def run_dijkstra(
    start: str = "A",
    destination: str = "D"
):
    graph = Graph(weighted=True)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "D", 1)
    graph.add_edge("C", "D", 3)

    result = dijkstra(graph, start, destination)

    return clean_json(result)