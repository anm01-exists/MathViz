from backend.integration.basic_integration.schema import (
    BasicIntegrationInput
)

from backend.integration.basic_integration.solver import (
    basic_integration
)


def test_power_rule():

    data = BasicIntegrationInput(
        function="x**2"
    )

    result = basic_integration(data)

    assert result.antiderivative == "x**3/3"
    assert result.result == "x**3/3 + C"


def test_polynomial():

    data = BasicIntegrationInput(
        function="3*x**2 + 4*x"
    )

    result = basic_integration(data)

    assert result.antiderivative == "x**3 + 2*x**2"


def test_sine():

    data = BasicIntegrationInput(
        function="sin(x)"
    )

    result = basic_integration(data)

    assert result.antiderivative == "-cos(x)"