import pytest
import sympy as sp

from backend.integration.area_between_curves.schema import (
    AreaBetweenCurvesInput
)

from backend.integration.area_between_curves.solver import (
    area_between_curves
)


def test_x_and_x_squared():
    data = AreaBetweenCurvesInput(
        upper_function="x",
        lower_function="x**2",
        lower_bound=0,
        upper_bound=1
    )

    result = area_between_curves(data)

    x = sp.symbols("x")

    difference = sp.sympify(
        result.difference_function
    )

    expected_difference = x - x**2

    assert sp.simplify(
        difference - expected_difference
    ) == 0

    assert result.area == pytest.approx(1 / 6)


def test_constant_and_linear():
    data = AreaBetweenCurvesInput(
        upper_function="3",
        lower_function="x",
        lower_bound=0,
        upper_bound=2
    )

    result = area_between_curves(data)

    x = sp.symbols("x")

    difference = sp.sympify(
        result.difference_function
    )

    expected_difference = 3 - x

    assert sp.simplify(
        difference - expected_difference
    ) == 0

    assert result.area == pytest.approx(4.0)


def test_quadratic_curves():
    data = AreaBetweenCurvesInput(
        upper_function="x + 2",
        lower_function="x**2",
        lower_bound=0,
        upper_bound=1
    )

    result = area_between_curves(data)

    assert result.area == pytest.approx(13 / 6)


def test_invalid_bounds():
    data = AreaBetweenCurvesInput(
        upper_function="x",
        lower_function="x**2",
        lower_bound=1,
        upper_bound=0
    )

    with pytest.raises(ValueError):
        area_between_curves(data)