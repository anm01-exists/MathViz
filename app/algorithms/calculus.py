from __future__ import annotations

from sympy import sympify, symbols, limit, factor, simplify, oo, solve

def solve_limit(expression: str, variable: str, point: float) -> dict:
    """
    Solve a limit and return the mathematical steps
    required by the visualization.
    """

    x = symbols(variable)
    expr = sympify(expression)

    # Direct substitution
    substituted = expr.subs(x, point)

    # Actual limit
    result = limit(expr, x, point)

    # Try factorization
    factored = factor(expr)

    # Try simplification
    simplified = simplify(expr)

    return {
        "type": "limit",
        "method": "symbolic_limit",
        "expression": expression,
        "variable": variable,
        "point": point,

        "steps": [
            {
                "step": 1,
                "type": "original",
                "expression": str(expr),
                "message": "Start with the given limit."
            },
            {
                "step": 2,
                "type": "substitution",
                "expression": str(substituted),
                "message": "Substitute the approaching value."
            },
            {
                "step": 3,
                "type": "factorization",
                "expression": str(factored),
                "message": "Factor the expression if necessary."
            },
            {
                "step": 4,
                "type": "simplification",
                "expression": str(simplified),
                "message": "Simplify the expression."
            },
            {
                "step": 5,
                "type": "result",
                "expression": str(result),
                "message": "The limit is obtained."
            }
        ],

        "result": str(result)
    }
def solve_one_sided_limit(
    expression: str,
    variable: str,
    point: float,
    direction: str
) -> dict:
    """
    Solve a one-sided limit.

    direction:
        '+' = from the right
        '-' = from the left
    """

    x = symbols(variable)
    expr = sympify(expression)

    result = limit(expr, x, point, dir=direction)

    side = "right" if direction == "+" else "left"

    return {
        "type": "one_sided_limit",
        "method": "symbolic_limit",
        "expression": expression,
        "variable": variable,
        "point": point,
        "direction": direction,
        "side": side,
        "result": str(result),
        "steps": [
            {
                "step": 1,
                "type": "identify_side",
                "message": f"Approach {point} from the {side} side."
            },
            {
                "step": 2,
                "type": "calculate",
                "message": f"Calculate the {side}-hand limit."
            },
            {
                "step": 3,
                "type": "result",
                "message": f"The {side}-hand limit is {result}.",
                "expression": str(result)
            }
        ]
    }
def solve_two_sided_limit(
    expression: str,
    variable: str,
    point: float
) -> dict:
    """
    Solve a two-sided limit by comparing
    the left-hand and right-hand limits.
    """

    x = symbols(variable)
    expr = sympify(expression)

    left_result = limit(expr, x, point, dir="-")
    right_result = limit(expr, x, point, dir="+")

    exists = left_result == right_result

    return {
        "type": "two_sided_limit",
        "method": "compare_one_sided_limits",
        "expression": expression,
        "variable": variable,
        "point": point,

        "left_result": str(left_result),
        "right_result": str(right_result),
        "exists": exists,

        "steps": [
            {
                "step": 1,
                "type": "left_hand",
                "message": "Calculate the left-hand limit.",
                "result": str(left_result)
            },
            {
                "step": 2,
                "type": "right_hand",
                "message": "Calculate the right-hand limit.",
                "result": str(right_result)
            },
            {
                "step": 3,
                "type": "comparison",
                "message": "Compare the two one-sided limits.",
                "result": "exists" if exists else "does_not_exist"
            }
        ],

        "result": (
            str(left_result)
            if exists
            else "does_not_exist"
        )
    }
def solve_limit_at_infinity(
    expression: str,
    variable: str,
    direction: str = "+"
) -> dict:
    """
    Solve a limit as the variable approaches infinity.

    direction:
        '+' = positive infinity
        '-' = negative infinity
    """

    x = symbols(variable)
    expr = sympify(expression)

    result = limit(expr, x, oo if direction == "+" else -oo)

    infinity = "∞" if direction == "+" else "-∞"

    return {
        "type": "limit_at_infinity",
        "method": "symbolic_limit",
        "expression": expression,
        "variable": variable,
        "direction": direction,
        "target": infinity,
        "result": str(result),
        "steps": [
            {
                "step": 1,
                "type": "identify",
                "message": f"Find the limit as {variable} approaches {infinity}."
            },
            {
                "step": 2,
                "type": "evaluate",
                "message": "Analyze the behavior of the expression as the variable grows."
            },
            {
                "step": 3,
                "type": "result",
                "message": f"The limit is {result}.",
                "expression": str(result)
            }
        ]
    }
def solve_continuity(
    expression: str,
    variable: str,
    point: float
) -> dict:
    """
    Check continuity of a function at a given point.
    """

    x = symbols(variable)
    expr = sympify(expression)

    function_value = expr.subs(x, point)
    limit_value = limit(expr, x, point)

    is_continuous = function_value == limit_value

    return {
        "type": "continuity",
        "method": "limit_and_function_value",
        "expression": expression,
        "variable": variable,
        "point": point,
        "function_value": str(function_value),
        "limit_value": str(limit_value),
        "is_continuous": is_continuous,
        "steps": [
            {
                "step": 1,
                "type": "function_value",
                "message": f"Find f({point}).",
                "result": str(function_value)
            },
            {
                "step": 2,
                "type": "limit",
                "message": f"Find the limit as {variable} approaches {point}.",
                "result": str(limit_value)
            },
            {
                "step": 3,
                "type": "comparison",
                "message": "Compare the function value with the limit.",
                "result": (
                    "continuous"
                    if is_continuous
                    else "not_continuous"
                )
            }
        ],
        "result": (
            "continuous"
            if is_continuous
            else "not_continuous"
        )
    }
def solve_derivative(
    expression: str,
    variable: str
) -> dict:
    """
    Calculate the derivative of a function.
    """

    x = symbols(variable)
    expr = sympify(expression)

    derivative = expr.diff(x)

    return {
        "type": "derivative",
        "method": "symbolic_differentiation",
        "expression": expression,
        "variable": variable,
        "derivative": str(derivative),
        "steps": [
            {
                "step": 1,
                "type": "function",
                "message": "Start with the given function.",
                "expression": str(expr)
            },
            {
                "step": 2,
                "type": "differentiate",
                "message": f"Differentiate with respect to {variable}."
            },
            {
                "step": 3,
                "type": "result",
                "message": "The derivative is obtained.",
                "expression": str(derivative)
            }
        ],
        "result": str(derivative)
    }
def solve_tangent_line(
    expression: str,
    variable: str,
    point: float
) -> dict:
    """
    Find the tangent line to a function at a given point.
    """

    x = symbols(variable)
    expr = sympify(expression)

    derivative = expr.diff(x)

    y_value = expr.subs(x, point)
    slope = derivative.subs(x, point)

    tangent = simplify(
        y_value + slope * (x - point)
    )

    return {
        "type": "tangent_line",
        "expression": expression,
        "variable": variable,
        "point": point,
        "function_value": str(y_value),
        "derivative": str(derivative),
        "slope": str(slope),
        "tangent_line": str(tangent),

        "steps": [
            {
                "step": 1,
                "type": "function_value",
                "message": f"Find f({point}).",
                "result": str(y_value)
            },
            {
                "step": 2,
                "type": "derivative",
                "message": "Find the derivative.",
                "result": str(derivative)
            },
            {
                "step": 3,
                "type": "slope",
                "message": f"Evaluate the derivative at x = {point}.",
                "result": str(slope)
            },
            {
                "step": 4,
                "type": "tangent",
                "message": "Construct the tangent line.",
                "result": str(tangent)
            }
        ],

        "result": str(tangent)
    }
def solve_power_rule(
    expression: str,
    variable: str
) -> dict:
    """
    Differentiate a function using the power rule.
    """

    x = symbols(variable)
    expr = sympify(expression)

    derivative = simplify(expr.diff(x))

    return {
        "type": "derivative_rule",
        "method": "power_rule",
        "expression": expression,
        "variable": variable,
        "derivative": str(derivative),

        "steps": [
            {
                "step": 1,
                "type": "identify",
                "message": "Identify the power of the variable."
            },
            {
                "step": 2,
                "type": "apply_rule",
                "message": "Apply the power rule."
            },
            {
                "step": 3,
                "type": "result",
                "message": "Simplify the derivative.",
                "expression": str(derivative)
            }
        ],

        "result": str(derivative)
    }
def solve_sum_rule(
    expression: str,
    variable: str
) -> dict:
    """
    Differentiate a sum of terms using the sum rule.
    """

    x = symbols(variable)
    expr = sympify(expression)

    terms = expr.as_ordered_terms()
    derivatives = [simplify(term.diff(x)) for term in terms]

    derivative = simplify(expr.diff(x))

    return {
        "type": "derivative_rule",
        "method": "sum_rule",
        "expression": expression,
        "variable": variable,
        "terms": [str(term) for term in terms],
        "term_derivatives": [str(d) for d in derivatives],
        "derivative": str(derivative),

        "steps": [
            {
                "step": 1,
                "type": "split",
                "message": "Differentiate each term separately."
            },
            {
                "step": 2,
                "type": "differentiate_terms",
                "message": "Apply the derivative rule to each term.",
                "expression": [
                    str(d) for d in derivatives
                ]
            },
            {
                "step": 3,
                "type": "combine",
                "message": "Add the derivatives together.",
                "expression": str(derivative)
            }
        ],

        "result": str(derivative)
    }
def solve_product_rule(
    expression: str,
    variable: str
) -> dict:
    """
    Differentiate a product using the product rule.
    """

    x = symbols(variable)
    expr = sympify(expression)

    factors = expr.as_ordered_factors()

    if len(factors) < 2:
        derivative = simplify(expr.diff(x))
        return {
            "type": "derivative_rule",
            "method": "product_rule",
            "expression": expression,
            "variable": variable,
            "result": str(derivative),
        }

    u = factors[0]
    v = simplify(expr / u)

    u_derivative = simplify(u.diff(x))
    v_derivative = simplify(v.diff(x))

    derivative = simplify(
        u_derivative * v + u * v_derivative
    )

    return {
        "type": "derivative_rule",
        "method": "product_rule",
        "expression": expression,
        "variable": variable,
        "u": str(u),
        "v": str(v),
        "u_derivative": str(u_derivative),
        "v_derivative": str(v_derivative),
        "derivative": str(derivative),

        "steps": [
            {
                "step": 1,
                "type": "identify",
                "message": "Identify the two factors."
            },
            {
                "step": 2,
                "type": "apply_rule",
                "message": "Apply (uv)' = u'v + uv'."
            },
            {
                "step": 3,
                "type": "differentiate",
                "message": "Differentiate each factor."
            },
            {
                "step": 4,
                "type": "result",
                "message": "Simplify the result.",
                "expression": str(derivative)
            }
        ],

        "result": str(derivative)
    }
def solve_quotient_rule(expression: str, variable: str) -> dict:
    x = symbols(variable)
    expr = sympify(expression)

    numerator, denominator = expr.as_numer_denom()

    u = numerator
    v = denominator

    u_prime = u.diff(x)
    v_prime = v.diff(x)

    derivative = simplify((v * u_prime - u * v_prime) / v**2)

    return {
        "type": "quotient_rule",
        "method": "quotient_rule",
        "expression": expression,
        "variable": variable,
        "u": str(u),
        "v": str(v),
        "u_prime": str(u_prime),
        "v_prime": str(v_prime),
        "result": str(derivative),
        "steps": [
            {
                "step": 1,
                "type": "identify",
                "message": f"Let u = {u} and v = {v}."
            },
            {
                "step": 2,
                "type": "differentiate",
                "message": f"u' = {u_prime}, v' = {v_prime}."
            },
            {
                "step": 3,
                "type": "apply_rule",
                "message": "Apply the quotient rule: (vu' - uv') / v²."
            },
            {
                "step": 4,
                "type": "simplify",
                "message": f"Simplify the derivative to {derivative}."
            }
        ]
    }
def solve_chain_rule(expression: str, variable: str) -> dict:
    x = symbols(variable)
    expr = sympify(expression)

    derivative = simplify(expr.diff(x))

    # Identify a common composite-function structure
    inner = None
    outer = None

    if expr.is_Pow and expr.base.has(x):
        inner = str(expr.base)
        outer = str(expr.exp)
    elif expr.is_Function and len(expr.args) == 1:
        inner = str(expr.args[0])
        outer = str(expr.func)

    return {
        "type": "chain_rule",
        "method": "chain_rule",
        "expression": expression,
        "variable": variable,
        "outer_function": outer,
        "inner_function": inner,
        "result": str(derivative),
        "steps": [
            {
                "step": 1,
                "type": "identify",
                "message": (
                    f"Identify the outer function {outer} "
                    f"and inner function {inner}."
                )
            },
            {
                "step": 2,
                "type": "differentiate",
                "message": "Differentiate the outer function."
            },
            {
                "step": 3,
                "type": "differentiate_inner",
                "message": "Differentiate the inner function."
            },
            {
                "step": 4,
                "type": "apply_rule",
                "message": "Multiply the outer derivative by the inner derivative."
            },
            {
                "step": 5,
                "type": "simplify",
                "message": f"Simplify the result to {derivative}."
            }
        ]
    }
def solve_derivative_applications(expression: str, variable: str) -> dict:
    x = symbols(variable)
    expr = sympify(expression)

    first_derivative = simplify(expr.diff(x))
    second_derivative = simplify(first_derivative.diff(x))

    critical_points = solve(first_derivative, x)

    classifications = []

    for point in critical_points:
        second_value = simplify(second_derivative.subs(x, point))

        if second_value < 0:
            classification = "local maximum"
        elif second_value > 0:
            classification = "local minimum"
        else:
            classification = "inconclusive"

        classifications.append({
            "point": str(point),
            "second_derivative_value": str(second_value),
            "classification": classification
        })

    return {
        "type": "derivative_applications",
        "method": "critical_points_and_second_derivative",
        "expression": expression,
        "variable": variable,
        "first_derivative": str(first_derivative),
        "second_derivative": str(second_derivative),
        "critical_points": [str(p) for p in critical_points],
        "classifications": classifications,
        "steps": [
            {
                "step": 1,
                "type": "differentiate",
                "message": f"Find the first derivative: {first_derivative}"
            },
            {
                "step": 2,
                "type": "critical_points",
                "message": "Set the first derivative equal to zero and find the critical points."
            },
            {
                "step": 3,
                "type": "second_derivative",
                "message": f"Find the second derivative: {second_derivative}"
            },
            {
                "step": 4,
                "type": "classify",
                "message": "Use the second derivative to classify the critical points."
            }
        ]
    }