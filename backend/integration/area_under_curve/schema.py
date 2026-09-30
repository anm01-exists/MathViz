from pydantic import BaseModel, Field


class AreaUnderCurveInput(BaseModel):
    function: str = Field(
        ...,
        description="Function of x, for example x**2"
    )

    lower_bound: float
    upper_bound: float


class AreaUnderCurveOutput(BaseModel):
    topic: str
    function: str
    lower_bound: float
    upper_bound: float

    antiderivative: str
    area: float