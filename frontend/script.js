const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
const button = document.getElementById("calculateButton");
const input = document.getElementById("function");
const result = document.getElementById("result");

if (!button || !input || !result) {
    console.error("Missing Calculate button, function input, or result element.");
    return;
}


// Video player placeholder
let video = document.getElementById("integrationVideo");

if (!video) {
    const heading = document.createElement("h3");
    heading.textContent = "Manim Animation";

    video = document.createElement("video");
    video.id = "integrationVideo";
    video.controls = true;
    video.style.width = "100%";
    video.style.maxWidth = "900px";
    video.style.display = "block";
    video.style.marginTop = "12px";

    const message = document.createElement("p");
    message.id = "videoMessage";
    message.textContent =
        "A video will appear here when equation-specific Manim generation is connected.";

    canvas.insertAdjacentElement("afterend", heading);
    heading.insertAdjacentElement("afterend", video);
    video.insertAdjacentElement("afterend", message);
}

function compileFunction(expression) {
    const allowed = new Set([
        "x", "sin", "cos", "tan", "exp",
        "log", "sqrt", "abs", "pi", "E"
    ]);

    const names = expression.match(/[a-zA-Z_]+/g) || [];

    for (const name of names) {
        if (!allowed.has(name)) {
            throw new Error("Unsupported function or variable: " + name);
        }
    }

    if (!/^[0-9a-zA-Z_+\-*/().,\s^]+$/.test(expression)) {
        throw new Error("Enter a valid expression, such as x^2 or sin(x).");
    }

    const jsExpression = expression
        .replace(/\^/g, "**")
        .replace(/\bsin\b/g, "Math.sin")
        .replace(/\bcos\b/g, "Math.cos")
        .replace(/\btan\b/g, "Math.tan")
        .replace(/\bexp\b/g, "Math.exp")
        .replace(/\blog\b/g, "Math.log")
        .replace(/\bsqrt\b/g, "Math.sqrt")
        .replace(/\babs\b/g, "Math.abs")
        .replace(/\bpi\b/g, "Math.PI")
        .replace(/\bE\b/g, "Math.E");

    return new Function("x", '"use strict"; return (' + jsExpression + ");");
}

function drawGraph(expression) {
    const fn = compileFunction(expression);
    const width = canvas.width;
    const height = canvas.height;
    const cx = width / 2;
    const cy = height / 2;
   const scaleX = width / 8;
const scaleY = height / 10;

    ctx.clearRect(0, 0, width, height);

    // Grid
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 1;

    for (let x = 0; x <= width; x += 50) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
    }

    for (let y = 0; y <= height; y += 50) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }

    // Axes
    ctx.strokeStyle = "#333333";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, cy);
    ctx.lineTo(width, cy);
    ctx.moveTo(cx, 0);
    ctx.lineTo(cx, height);
    ctx.stroke();

    ctx.fillStyle = "#333333";
    ctx.font = "15px Arial";
    ctx.fillText("y", cx + 8, 18);
    ctx.fillText("x", width - 18, cy - 8);

    // Animate the curve
    let px = 0;
    let previousY = null;

    function animate() {
        const end = Math.min(px + 6, width);

        ctx.beginPath();
        ctx.strokeStyle = "#1769aa";
        ctx.lineWidth = 3;

        while (px < end) {
            const x = (px - cx) / scaleX;
            let y;

            try {
                y = Number(fn(x));
            } catch {
                y = NaN;
            }

            if (!Number.isFinite(y) || Math.abs(y) > 1000) {
                previousY = null;
                px++;
                continue;
            }

            const py = cy - y * scaleY;

            if (previousY === null || Math.abs(py - previousY) > height) {
                ctx.moveTo(px, py);
            } else {
                ctx.lineTo(px, py);
            }

            previousY = py;
            px++;
        }

        ctx.stroke();

        if (px < width) {
            requestAnimationFrame(animate);
        }
    }

    animate();
}

function toLatex(value) {
    return String(value)
        .replace(/\*\*/g, "^")
        .replace(/\^([a-zA-Z0-9]+)/g, "^{$1}")
        .replace(/\*/g, " \\cdot ")
        .replace(/\bpi\b/g, "\\pi")
        .replace(/\bsqrt\(([^()]*)\)/g, "\\sqrt{$1}")
        .replace(/\b(sin|cos|tan|log|exp)\b/g, "\\$1");
}

async function renderLatex() {
    if (window.MathJax && window.MathJax.typesetPromise) {
        await window.MathJax.typesetPromise([result]);
    }
}

button.addEventListener("click", async () => {
    const expression = input.value.trim();

    if (!expression) {
        result.textContent = "Please enter a function first.";
        return;
    }

    button.disabled = true;
    result.textContent = "Calculating...";

    try {
        // Validate the graph expression
        compileFunction(expression);

        // Calculate the integral using FastAPI
        const response = await fetch(
            API_BASE_URL + "/integration/basic-integration",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    function: expression
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail || data)
            );
        }

        const functionLatex = toLatex(data.function || expression);
        const antiLatex = toLatex(data.antiderivative);
        const resultLatex = toLatex(data.result);

        result.innerHTML =
            "<p>Entered function: \\(f(x) = " + functionLatex + "\\)</p>" +
            "<p>Integral: \\(\\int " + functionLatex + "\\,dx\\)</p>" +
            "<p>Antiderivative: \\(" + antiLatex + "\\)</p>" +
            "<p>Result: \\(" + resultLatex + "\\)</p>";

        await renderLatex();

        // Generate a Manim video for the entered equation
const videoMessage = document.getElementById("videoMessage");

if (videoMessage) {
    videoMessage.textContent = "Generating video... Please wait.";
}

video.pause();
video.removeAttribute("src");
video.load();

const videoResponse = await fetch(
    API_BASE_URL + "/integration/generate-video",
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            function: expression
        })
    }
);

const videoData = await videoResponse.json();

if (!videoResponse.ok) {
    throw new Error(
        "Video generation failed: " +
        (videoData.detail || "Unknown error")
    );
}

// Display the generated video in the existing player
video.src = API_BASE_URL + videoData.video_url;
video.load();

try {
    await video.play();
} catch (error) {
    // Autoplay may be blocked by the browser.
    // The user can still press Play on the video.
}

if (videoMessage) {
    videoMessage.textContent =
        "Video generated for: " + expression;
}
    } catch (error) {
        result.textContent = "Calculation failed: " + error.message;
        console.error("MathViz error:", error);
    } finally {
        button.disabled = false;
    }
});


});
