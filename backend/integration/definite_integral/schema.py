from pydantic import BaseModel, Field


class DefiniteIntegralInput(BaseModel):
    function: str = Field(
        ...,
        description="Function of x, for example x**2"
    )

    lower_bound: float
    upper_bound: float


class DefiniteIntegralOutput(BaseModel):
    topic: str
    function: str
    lower_bound: float
    upper_bound: float
    antiderivative: str
    result: float