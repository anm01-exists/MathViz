import sympy as sp

from .schema import (
    SubstitutionInput,
    SubstitutionOutput
)


def substitution(
    data: SubstitutionInput
) -> SubstitutionOutput:

    x = sp.symbols("x")
    u = sp.symbols("u")

    try:
        # Convert input strings into SymPy expressions
        function = sp.sympify(data.function)
        u_expression = sp.sympify(data.u_expression)

        # Calculate du/dx
        du_dx = sp.diff(u_expression, x)

        # u must depend on x
        if du_dx == 0:
            raise ValueError(
                "Substitution expression must depend on x."
            )

        # Divide the integrand by du/dx.
        # factor() keeps expressions such as
        # (x**2 + 1)**3 together.
        transformed = sp.factor(
            function / du_dx
        )

        # Replace the chosen u-expression by u
        transformed_function = sp.simplify(
            transformed.subs(
                u_expression,
                u
            )
        )

        # Integrate with respect to u
        result_u = sp.integrate(
            transformed_function,
            u
        )

        # Substitute u back in terms of x
        result = sp.simplify(
            result_u.subs(
                u,
                u_expression
            )
        )

    except ValueError:
        raise

    except Exception as e:
        raise ValueError(
            f"Invalid substitution input: {e}"
        )

    return SubstitutionOutput(
        topic="substitution",
        original_function=data.function,
        u=str(u_expression),
        du_dx=str(du_dx),
        transformed_function=str(
            transformed_function
        ),
        result=f"{result} + C"
    )