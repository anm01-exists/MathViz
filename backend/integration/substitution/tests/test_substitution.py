from backend.integration.substitution.schema import (
    SubstitutionInput
)

from backend.integration.substitution.solver import (
    substitution
)


def test_basic_substitution():

    data = SubstitutionInput(
        function="2*x*(x**2+1)**3",
        u_expression="x**2+1"
    )

    result = substitution(data)

    assert result.u == "x**2 + 1"
    assert result.du_dx == "2*x"
    assert result.transformed_function == "u**3"
    assert result.result == "(x**2 + 1)**4/4 + C"


def test_exponential_substitution():

    data = SubstitutionInput(
        function="2*x*exp(x**2)",
        u_expression="x**2"
    )

    result = substitution(data)

    assert result.u == "x**2"
    assert result.du_dx == "2*x"
    assert result.transformed_function == "exp(u)"
    assert result.result == "exp(x**2) + C"


def test_invalid_constant_substitution():

    data = SubstitutionInput(
        function="x**2",
        u_expression="5"
    )

    try:
        substitution(data)
        assert False
    except ValueError:
        assert True