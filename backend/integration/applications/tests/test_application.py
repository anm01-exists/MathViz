import pytest

from backend.integration.applications.schema import ApplicationsInput
from backend.integration.applications.solver import applications


def test_displacement():
    data = ApplicationsInput(
        application_type="displacement",
        function="2*x + 3",
        lower_bound=0,
        upper_bound=5
    )

    result = applications(data)

    assert result.result == pytest.approx(40.0)
    assert result.antiderivative == "x**2 + 3*x"


def test_accumulation():
    data = ApplicationsInput(
        application_type="accumulation",
        function="x",
        lower_bound=0,
        upper_bound=4,
        initial_value=10
    )

    result = applications(data)

    assert result.result == pytest.approx(18.0)


def test_invalid_application_type():
    data = ApplicationsInput(
        application_type="invalid",
        function="x",
        lower_bound=0,
        upper_bound=1
    )

    with pytest.raises(ValueError):
        applications(data)


def test_invalid_bounds():
    data = ApplicationsInput(
        application_type="displacement",
        function="x",
        lower_bound=5,
        upper_bound=2
    )

    with pytest.raises(ValueError):
        applications(data)