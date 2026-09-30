from pydantic import BaseModel, Field


class ApproximatingAreaInput(BaseModel):
    function: str = Field(
        ...,
        description="Function of x, for example x^2"
    )

    lower_bound: float
    upper_bound: float

    num_rectangles: int = Field(
        ...,
        gt=0
    )

    method: str = "left"


class ApproximatingAreaOutput(BaseModel):
    topic: str
    function: str

    lower_bound: float
    upper_bound: float

    num_rectangles: int
    method: str

    approximation: float