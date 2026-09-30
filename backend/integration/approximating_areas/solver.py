import sympy as sp

from .schema import (
    ApproximatingAreaInput,
    ApproximatingAreaOutput
)


def approximating_area(
    data: ApproximatingAreaInput
) -> ApproximatingAreaOutput:

    # Create x as the mathematical variable
    x = sp.symbols("x")

    # Convert the input function into a SymPy expression
    function = sp.sympify(data.function)

    # Get the limits and number of rectangles
    a = data.lower_bound
    b = data.upper_bound
    n = data.num_rectangles

    # Width of each rectangle
    dx = (b - a) / n

    total = 0

    # Calculate the Riemann sum
    for i in range(n):

        if data.method == "left":
            x_i = a + i * dx

        elif data.method == "right":
            x_i = a + (i + 1) * dx

        elif data.method == "midpoint":
            x_i = a + (i + 0.5) * dx

        else:
            raise ValueError(
                "Method must be left, right, or midpoint"
            )

        # Height of the rectangle
        height = function.subs(x, x_i)

        # Rectangle area = height × width
        total += height * dx

    approximation = float(total)

    return ApproximatingAreaOutput(
        topic="approximating_areas",
        function=data.function,
        lower_bound=a,
        upper_bound=b,
        num_rectangles=n,
        method=data.method,
        approximation=approximation
    )