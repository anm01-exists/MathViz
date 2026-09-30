from integration.approximating_areas.schema import (
    ApproximatingAreaInput
)

from integration.approximating_areas.solver import (
    approximating_area
)


def test_left_riemann_sum():

    data = ApproximatingAreaInput(
        function="x^2",
        lower_bound=0,
        upper_bound=3,
        num_rectangles=8,
        method="left"
    )

    result = approximating_area(data)

    print(result.model_dump())

    assert result.topic == "approximating_areas"
    assert result.function == "x^2"
    assert result.num_rectangles == 8
    assert result.approximation > 0