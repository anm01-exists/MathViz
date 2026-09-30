import sympy as sp

from .schema import (
    IntegrationByPartsInput,
    IntegrationByPartsOutput
)


def integration_by_parts(
    data: IntegrationByPartsInput
) -> IntegrationByPartsOutput:

    x = sp.symbols("x")

    try:
        # Convert input expressions to SymPy
        u = sp.sympify(data.u_expression)
        dv = sp.sympify(data.dv_expression)

        # du/dx
        du_dx = sp.diff(u, x)

        # v = integral of dv
        v = sp.integrate(dv, x)

        # Remaining integral: integral(v * du)
        remaining_integral_expression = sp.simplify(
            v * du_dx
        )

        remaining_integral = sp.integrate(
            remaining_integral_expression,
            x
        )

        # Integration by parts:
        # integral(u dv) = u*v - integral(v du)
        result = sp.simplify(
            u * v - remaining_integral
        )

    except Exception as e:
        raise ValueError(
            f"Invalid integration by parts input: {e}"
        )

    return IntegrationByPartsOutput(
        topic="integration_by_parts",
        u=str(u),
        dv=str(dv),
        du_dx=str(du_dx),
        v=str(v),
        remaining_integral=str(
            remaining_integral_expression
        ),
        result=f"{result} + C"
    )