import sympy as sp

from .schema import (
    BasicIntegrationInput,
    BasicIntegrationOutput
)


def basic_integration(
    data: BasicIntegrationInput
) -> BasicIntegrationOutput:

    # Create x as the mathematical variable
    x = sp.symbols("x")

    try:
        # Convert input string into a SymPy expression
        function = sp.sympify(data.function)

        # Calculate the indefinite integral
        result = sp.integrate(function, x)

    except Exception as e:
        raise ValueError(
            f"Invalid mathematical expression: {e}"
        )

    return BasicIntegrationOutput(
        topic="basic_integration",
        function=data.function,
        antiderivative=str(result),
        result=f"{result} + C"
    )