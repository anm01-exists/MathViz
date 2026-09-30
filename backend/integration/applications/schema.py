from pydantic import BaseModel, Field


class ApplicationsInput(BaseModel):
    application_type: str = Field(
        ...,
        description="Type of application: displacement or accumulation"
    )

    function: str = Field(
        ...,
        description="Function of x, for example 2*x + 3"
    )

    lower_bound: float
    upper_bound: float

    initial_value: float = Field(
        default=0,
        description="Initial value, used for accumulation applications"
    )


class ApplicationsOutput(BaseModel):
    topic: str
    application_type: str
    function: str

    lower_bound: float
    upper_bound: float

    initial_value: float

    antiderivative: str
    result: float