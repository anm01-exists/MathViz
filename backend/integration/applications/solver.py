import sympy as sp

from .schema import (
    ApplicationsInput,
    ApplicationsOutput
)


def applications(
    data: ApplicationsInput
) -> ApplicationsOutput:

    # Create mathematical variable
    x = sp.symbols("x")

    # Validate application type
    if data.application_type not in [
        "displacement",
        "accumulation"
    ]:
        raise ValueError(
            "application_type must be 'displacement' "
            "or 'accumulation'."
        )

    # Validate bounds
    if data.lower_bound >= data.upper_bound:
        raise ValueError(
            "lower_bound must be less than upper_bound."
        )

    # Convert function string into SymPy expression
    try:
        function = sp.sympify(data.function)
    except Exception as exc:
        raise ValueError(
            f"Invalid function: {data.function}"
        ) from exc

    # Calculate antiderivative
    antiderivative = sp.integrate(function, x)

    # Calculate definite integral
    integral_value = sp.integrate(
        function,
        (x, data.lower_bound, data.upper_bound)
    )

    # Calculate final result
    if data.application_type == "displacement":
        result = integral_value

    else:
        # Accumulated quantity = initial value + integral
        result = data.initial_value + integral_value

    return ApplicationsOutput(
        topic="applications_of_integration",
        application_type=data.application_type,
        function=data.function,
        lower_bound=data.lower_bound,
        upper_bound=data.upper_bound,
        initial_value=data.initial_value,
        antiderivative=str(antiderivative),
        result=float(result)
    )