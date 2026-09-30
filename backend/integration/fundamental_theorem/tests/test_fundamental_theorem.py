import pytest

from backend.integration.fundamental_theorem.schema import (
    FundamentalTheoremInput
)

from backend.integration.fundamental_theorem.solver import (
    fundamental_theorem
)


def test_x_squared():
    data = FundamentalTheoremInput(
        function="x**2",
        lower_bound=0,
        upper_bound=3
    )

    result = fundamental_theorem(data)

    assert result.antiderivative == "x**3/3"
    assert result.lower_value == "0"
    assert result.upper_value == "9"
    assert result.result == "9"


def test_linear_function():
    data = FundamentalTheoremInput(
        function="x",
        lower_bound=0,
        upper_bound=2
    )

    result = fundamental_theorem(data)

    assert result.antiderivative == "x**2/2"
    assert result.lower_value == "0"
    assert result.upper_value == "2"
    assert result.result == "2"


def test_polynomial():
    data = FundamentalTheoremInput(
        function="3*x**2 + 2*x",
        lower_bound=0,
        upper_bound=2
    )

    result = fundamental_theorem(data)

    assert result.result == "12"


def test_invalid_bounds():
    data = FundamentalTheoremInput(
        function="x**2",
        lower_bound=3,
        upper_bound=0
    )

    with pytest.raises(ValueError):
        fundamental_theorem(data)