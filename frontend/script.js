const API_BASE_URL = "http://127.0.0.1:8000";

async function callIntegrationAPI(endpoint, data) {
    try {
        const response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Something went wrong"
            );
        }

        displayResult(result);

    } catch (error) {
        displayResult({
            error: error.message
        });
    }
}


function displayResult(result) {
    const resultBox = document.getElementById("result");

    if (!resultBox) {
        return;
    }

    resultBox.textContent =
        JSON.stringify(result, null, 2);
}


// Basic Integration
async function runDefiniteIntegral() {

    const functionElement =
        document.getElementById("definite-function") ||
        document.getElementById("function");

    const lowerElement =
        document.getElementById("definite-lower") ||
        document.getElementById("lower-bound") ||
        document.getElementById("lower");

    const upperElement =
        document.getElementById("definite-upper") ||
        document.getElementById("upper-bound") ||
        document.getElementById("upper");

    if (!functionElement || !lowerElement || !upperElement) {
        displayResult({
            error: "Definite Integral input fields could not be found."
        });
        return;
    }

    const functionInput = functionElement.value;

    const lower = parseFloat(lowerElement.value);

    const upper = parseFloat(upperElement.value);

    await callIntegrationAPI(
        "/integration/definite-integral",
        {
            function: functionInput,
            lower_bound: lower,
            upper_bound: upper
        }
    );
}

// Definite Integral
async function runDefiniteIntegral() {

    const functionInput =
        document.getElementById("definite-function").value;

    const lower =
        parseFloat(
            document.getElementById("definite-lower").value
        );

    const upper =
        parseFloat(
            document.getElementById("definite-upper").value
        );

    await callIntegrationAPI(
        "/integration/definite-integral",
        {
            function: functionInput,
            lower_bound: lower,
            upper_bound: upper
        }
    );
}


// Fundamental Theorem
async function runFundamentalTheorem() {

    const functionInput =
        document.getElementById("ftc-function").value;

    const lower =
        parseFloat(
            document.getElementById("ftc-lower").value
        );

    const upper =
        parseFloat(
            document.getElementById("ftc-upper").value
        );

    await callIntegrationAPI(
        "/integration/fundamental-theorem",
        {
            function: functionInput,
            lower_bound: lower,
            upper_bound: upper
        }
    );
}


// Substitution
async function runSubstitution() {

    const functionInput =
        document.getElementById("substitution-function").value;

    const uExpression =
        document.getElementById("u-expression").value;

    await callIntegrationAPI(
        "/integration/substitution",
        {
            function: functionInput,
            u_expression: uExpression
        }
    );
}


// Integration by Parts
async function runIntegrationByParts() {

    const uExpression =
        document.getElementById("parts-u").value;

    const dvExpression =
        document.getElementById("parts-dv").value;

    await callIntegrationAPI(
        "/integration/integration-by-parts",
        {
            u_expression: uExpression,
            dv_expression: dvExpression
        }
    );
}


// Applications
async function runApplications() {

    const applicationType =
        document.getElementById("application-type").value;

    const functionInput =
        document.getElementById("application-function").value;

    const lower =
        parseFloat(
            document.getElementById("application-lower").value
        );

    const upper =
        parseFloat(
            document.getElementById("application-upper").value
        );

    const initialValue =
        parseFloat(
            document.getElementById("initial-value").value
        ) || 0;

    await callIntegrationAPI(
        "/integration/applications",
        {
            application_type: applicationType,
            function: functionInput,
            lower_bound: lower,
            upper_bound: upper,
            initial_value: initialValue
        }
    );
}


// Area Under Curve
async function runAreaUnderCurve() {

    const functionInput =
        document.getElementById("area-function").value;

    const lower =
        parseFloat(
            document.getElementById("area-lower").value
        );

    const upper =
        parseFloat(
            document.getElementById("area-upper").value
        );

    await callIntegrationAPI(
        "/integration/area-under-curve",
        {
            function: functionInput,
            lower_bound: lower,
            upper_bound: upper
        }
    );
}


// Area Between Curves
async function runAreaBetweenCurves() {

    const upperFunction =
        document.getElementById("upper-function").value;

    const lowerFunction =
        document.getElementById("lower-function").value;

    const lower =
        parseFloat(
            document.getElementById("between-lower").value
        );

    const upper =
        parseFloat(
            document.getElementById("between-upper").value
        );

    await callIntegrationAPI(
        "/integration/area-between-curves",
        {
            upper_function: upperFunction,
            lower_function: lowerFunction,
            lower_bound: lower,
            upper_bound: upper
        }
    );
}
document
    .getElementById("calculateButton")
    .addEventListener("click", function () {

        const topic =
            document.getElementById("topic").value;

        switch (topic) {

            case "basic-integration":
                runBasicIntegration();
                break;

            case "definite-integral":
                runDefiniteIntegral();
                break;

            case "fundamental-theorem":
                runFundamentalTheorem();
                break;

            case "substitution":
                runSubstitution();
                break;

            case "integration-by-parts":
                runIntegrationByParts();
                break;

            case "applications":
                runApplications();
                break;

            case "area-under-curve":
                runAreaUnderCurve();
                break;

            case "area-between-curves":
                runAreaBetweenCurves();
                break;

            case "approximating-area":
                runApproximatingArea();
                break;

            default:
                displayResult({
                    error: "Please select a valid topic."
                });
        }
    });
