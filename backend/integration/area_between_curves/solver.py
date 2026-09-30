import sympy as sp

from .schema import (
    AreaBetweenCurvesInput,
    AreaBetweenCurvesOutput
)


def area_between_curves(
    data: AreaBetweenCurvesInput
) -> AreaBetweenCurvesOutput:

    x = sp.symbols("x")

    if data.lower_bound >= data.upper_bound:
        raise ValueError(
            "Lower bound must be less than upper bound."
        )

    try:
        upper_function = sp.sympify(
            data.upper_function
        )

        lower_function = sp.sympify(
            data.lower_function
        )

        difference = sp.expand(
            upper_function - lower_function
        )

        antiderivative = sp.integrate(
            difference,
            x
        )

        area = sp.integrate(
            difference,
            (x, data.lower_bound, data.upper_bound)
        )

    except Exception as e:
        raise ValueError(
            f"Invalid mathematical expression: {e}"
        )

    if area < 0:
        raise ValueError(
            "Upper function must be above the lower function "
            "over the given interval."
        )

    return AreaBetweenCurvesOutput(
        topic="area_between_curves",
        upper_function=data.upper_function,
        lower_function=data.lower_function,
        lower_bound=data.lower_bound,
        upper_bound=data.upper_bound,
        difference_function=str(difference),
        antiderivative=str(antiderivative),
        area=float(area)
    )