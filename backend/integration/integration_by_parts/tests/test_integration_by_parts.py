import sympy as sp

from backend.integration.integration_by_parts.schema import (
    IntegrationByPartsInput
)

from backend.integration.integration_by_parts.solver import (
    integration_by_parts
)


def test_x_exp_x():

    data = IntegrationByPartsInput(
        u_expression="x",
        dv_expression="exp(x)"
    )

    result = integration_by_parts(data)

    assert result.u == "x"
    assert result.dv == "exp(x)"
    assert result.du_dx == "1"
    assert result.v == "exp(x)"

    expression = sp.sympify(
        result.result.replace(" + C", "")
    )

    expected = x_expected = (
        sp.symbols("x") * sp.exp(sp.symbols("x"))
        - sp.exp(sp.symbols("x"))
    )

    assert sp.simplify(expression - expected) == 0


def test_x_cos_x():

    data = IntegrationByPartsInput(
        u_expression="x",
        dv_expression="cos(x)"
    )

    result = integration_by_parts(data)

    x = sp.symbols("x")

    expression = sp.sympify(
        result.result.replace(" + C", "")
    )

    expected = (
        x * sp.sin(x) + sp.cos(x)
    )

    assert sp.simplify(expression - expected) == 0


def test_x_squared_exp_x():

    data = IntegrationByPartsInput(
        u_expression="x**2",
        dv_expression="exp(x)"
    )

    result = integration_by_parts(data)

    x = sp.symbols("x")

    expression = sp.sympify(
        result.result.replace(" + C", "")
    )

    expected = (
        sp.exp(x) * (x**2 - 2*x + 2)
    )

    assert sp.simplify(expression - expected) == 0