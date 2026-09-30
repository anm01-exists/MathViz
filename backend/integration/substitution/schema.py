from pydantic import BaseModel, Field


class SubstitutionInput(BaseModel):
    function: str = Field(
        ...,
        description="Integrand, for example 2*x*(x**2+1)**3"
    )

    u_expression: str = Field(
        ...,
        description="Substitution expression, for example x**2+1"
    )


class SubstitutionOutput(BaseModel):
    topic: str
    original_function: str
    u: str
    du_dx: str
    transformed_function: str
    result: str