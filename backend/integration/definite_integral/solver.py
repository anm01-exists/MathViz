import sympy as sp

from .schema import (
    DefiniteIntegralInput,
    DefiniteIntegralOutput
)


def definite_integral(
    data: DefiniteIntegralInput
) -> DefiniteIntegralOutput:

    x = sp.symbols("x")

    # Check that the limits are valid
    if data.lower_bound >= data.upper_bound:
        raise ValueError(
            "Lower bound must be less than upper bound."
        )

    try:
        # Convert the function into a SymPy expression
        function = sp.sympify(data.function)

        # Find the antiderivative
        antiderivative = sp.integrate(function, x)

        # Calculate the definite integral
        result = sp.integrate(
            function,
            (x, data.lower_bound, data.upper_bound)
        )

    except Exception as e:
        raise ValueError(
            f"Invalid mathematical expression: {e}"
        )

    return DefiniteIntegralOutput(
        topic="definite_integral",
        function=data.function,
        lower_bound=data.lower_bound,
        upper_bound=data.upper_bound,
        antiderivative=str(antiderivative),
        result=float(result)
    )