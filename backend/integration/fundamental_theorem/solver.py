import sympy as sp

from .schema import (
    FundamentalTheoremInput,
    FundamentalTheoremOutput
)


def fundamental_theorem(
    data: FundamentalTheoremInput
) -> FundamentalTheoremOutput:

    x = sp.symbols("x")

    # Validate the limits
    if data.lower_bound >= data.upper_bound:
        raise ValueError(
            "Lower bound must be less than upper bound."
        )

    try:
        # Convert the input function into a SymPy expression
        function = sp.sympify(data.function)

        # Find F(x), the antiderivative of f(x)
        antiderivative = sp.integrate(function, x)

        # Convert float bounds into exact SymPy numbers
        lower = sp.Rational(str(data.lower_bound))
        upper = sp.Rational(str(data.upper_bound))

        # Calculate F(a)
        lower_value = sp.simplify(
            antiderivative.subs(x, lower)
        )

        # Calculate F(b)
        upper_value = sp.simplify(
            antiderivative.subs(x, upper)
        )

        # Fundamental Theorem:
        # Integral from a to b of f(x) dx = F(b) - F(a)
        result = sp.simplify(
            upper_value - lower_value
        )

    except Exception as e:
        raise ValueError(
            f"Invalid mathematical expression: {e}"
        )

    return FundamentalTheoremOutput(
        topic="fundamental_theorem",
        function=data.function,
        lower_bound=data.lower_bound,
        upper_bound=data.upper_bound,
        antiderivative=str(antiderivative),
        lower_value=str(lower_value),
        upper_value=str(upper_value),
        result=str(result)
    )