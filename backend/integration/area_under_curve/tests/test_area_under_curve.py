import pytest

from backend.integration.area_under_curve.schema import (
    AreaUnderCurveInput
)

from backend.integration.area_under_curve.solver import (
    area_under_curve
)


def test_x_squared():
    data = AreaUnderCurveInput(
        function="x**2",
        lower_bound=0,
        upper_bound=3
    )

    result = area_under_curve(data)

    assert result.antiderivative == "x**3/3"
    assert result.area == pytest.approx(9.0)


def test_linear_function():
    data = AreaUnderCurveInput(
        function="x",
        lower_bound=0,
        upper_bound=2
    )

    result = area_under_curve(data)

    assert result.antiderivative == "x**2/2"
    assert result.area == pytest.approx(2.0)


def test_sine_function():
    data = AreaUnderCurveInput(
        function="sin(x)",
        lower_bound=0,
        upper_bound=3.141592653589793
    )

    result = area_under_curve(data)

    assert result.antiderivative == "-cos(x)"
    assert result.area == pytest.approx(2.0, abs=1e-6)


def test_invalid_bounds():
    data = AreaUnderCurveInput(
        function="x**2",
        lower_bound=3,
        upper_bound=0
    )

    with pytest.raises(ValueError):
        area_under_curve(data)