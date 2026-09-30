import sympy as sp

from .schema import (
    AreaUnderCurveInput,
    AreaUnderCurveOutput
)


def area_under_curve(
    data: AreaUnderCurveInput
) -> AreaUnderCurveOutput:

    x = sp.symbols("x")

    if data.lower_bound >= data.upper_bound:
        raise ValueError(
            "Lower bound must be less than upper bound."
        )

    try:
        function = sp.sympify(data.function)

        antiderivative = sp.integrate(
            function,
            x
        )

        area = sp.integrate(
            function,
            (x, data.lower_bound, data.upper_bound)
        )

    except Exception as e:
        raise ValueError(
            f"Invalid mathematical expression: {e}"
        )

    return AreaUnderCurveOutput(
        topic="area_under_curve",
        function=data.function,
        lower_bound=data.lower_bound,
        upper_bound=data.upper_bound,
        antiderivative=str(antiderivative),
        area=float(area)
    )