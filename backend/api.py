from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .graph import Graph
from .bfs import bfs
from .dfs import dfs
from .dijkstra import dijkstra
from .integration.approximating_areas.schema import ApproximatingAreaInput
from .integration.approximating_areas.solver import approximating_area
from .integration.basic_integration.schema import BasicIntegrationInput
from .integration.basic_integration.solver import basic_integration

from .integration.definite_integral.schema import DefiniteIntegralInput
from .integration.definite_integral.solver import definite_integral

from .integration.fundamental_theorem.schema import FundamentalTheoremInput
from .integration.fundamental_theorem.solver import fundamental_theorem

from .integration.substitution.schema import SubstitutionInput
from .integration.substitution.solver import substitution

from .integration.integration_by_parts.schema import IntegrationByPartsInput
from .integration.integration_by_parts.solver import integration_by_parts

from .integration.applications.schema import ApplicationsInput
from .integration.applications.solver import applications

from .integration.area_under_curve.schema import AreaUnderCurveInput
from .integration.area_under_curve.solver import area_under_curve

from .integration.area_between_curves.schema import AreaBetweenCurvesInput
from .integration.area_between_curves.solver import area_between_curves


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/integration/approximating-area")
def run_approximating_area(data: ApproximatingAreaInput):

    result = approximating_area(data)

    return result.model_dump()
@app.post("/integration/basic-integration")
def run_basic_integration(data: BasicIntegrationInput):
    result = basic_integration(data)
    return result.model_dump()


@app.post("/integration/definite-integral")
def run_definite_integral(data: DefiniteIntegralInput):
    result = definite_integral(data)
    return result.model_dump()


@app.post("/integration/fundamental-theorem")
def run_fundamental_theorem(data: FundamentalTheoremInput):
    result = fundamental_theorem(data)
    return result.model_dump()


@app.post("/integration/substitution")
def run_substitution(data: SubstitutionInput):
    result = substitution(data)
    return result.model_dump()


@app.post("/integration/integration-by-parts")
def run_integration_by_parts(data: IntegrationByPartsInput):
    result = integration_by_parts(data)
    return result.model_dump()


@app.post("/integration/applications")
def run_applications(data: ApplicationsInput):
    result = applications(data)
    return result.model_dump()


@app.post("/integration/area-under-curve")
def run_area_under_curve(data: AreaUnderCurveInput):
    result = area_under_curve(data)
    return result.model_dump()


@app.post("/integration/area-between-curves")
def run_area_between_curves(data: AreaBetweenCurvesInput):
    result = area_between_curves(data)
    return result.model_dump()