from pydantic import BaseModel, Field


class IntegrationByPartsInput(BaseModel):
    u_expression: str = Field(
        ...,
        description="The u part, for example x"
    )

    dv_expression: str = Field(
        ...,
        description="The dv part without dx, for example exp(x)"
    )


class IntegrationByPartsOutput(BaseModel):
    topic: str
    u: str
    dv: str
    du_dx: str
    v: str
    remaining_integral: str
    result: str