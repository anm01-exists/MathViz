from pydantic import BaseModel, Field


class FundamentalTheoremInput(BaseModel):
    function: str = Field(
        ...,
        description="Function of x, for example x**2"
    )

    lower_bound: float
    upper_bound: float


class FundamentalTheoremOutput(BaseModel):
    topic: str
    function: str
    lower_bound: float
    upper_bound: float
    antiderivative: str
    lower_value: str
    upper_value: str
    result: str