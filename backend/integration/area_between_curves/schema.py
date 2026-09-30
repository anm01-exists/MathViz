from pydantic import BaseModel, Field


class AreaBetweenCurvesInput(BaseModel):
    upper_function: str = Field(
        ...,
        description="Upper function of x, for example x"
    )

    lower_function: str = Field(
        ...,
        description="Lower function of x, for example x**2"
    )

    lower_bound: float
    upper_bound: float


class AreaBetweenCurvesOutput(BaseModel):
    topic: str

    upper_function: str
    lower_function: str

    lower_bound: float
    upper_bound: float

    difference_function: str
    antiderivative: str
    area: float