import pytest

from backend.integration.definite_integral.schema import (
    DefiniteIntegralInput
)

from backend.integration.definite_integral.solver import (
    definite_integral
)


def test_x_squared():

    data = DefiniteIntegralInput(
        function="x**2",
        lower_bound=0,
        upper_bound=3
    )

    result = definite_integral(data)

    assert result.result == pytest.approx(9.0)


def test_linear_function():

    data = DefiniteIntegralInput(
        function="x",
        lower_bound=0,
        upper_bound=2
    )

    result = definite_integral(data)

    assert result.result == pytest.approx(2.0)


def test_sine_function():

    data = DefiniteIntegralInput(
        function="sin(x)",
        lower_bound=0,
        upper_bound=3.141592653589793
    )

    result = definite_integral(data)

    assert result.result == pytest.approx(2.0, abs=1e-6)


def test_invalid_bounds():

    data = DefiniteIntegralInput(
        function="x**2",
        lower_bound=3,
        upper_bound=0
    )

    with pytest.raises(ValueError):
        definite_integral(data)
        