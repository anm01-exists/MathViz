from pydantic import BaseModel, Field


class BasicIntegrationInput(BaseModel):
    function: str = Field(
        ...,
        description="Function of x, for example x**2"
    )


class BasicIntegrationOutput(BaseModel):
    topic: str
    function: str
    antiderivative: str
    result: str