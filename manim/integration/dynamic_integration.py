import os
import sympy as sp
from manim import *


class DynamicIntegration(Scene):
    def construct(self):
        function_input = os.environ.get("MATHVIZ_FUNCTION", "x**2")
        x = sp.symbols("x")

        expression = sp.sympify(function_input)
        antiderivative = sp.integrate(expression, x)

        title = Text("MathViz - Integration", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        function_latex = sp.latex(expression)
        integral_latex = sp.latex(antiderivative)

        formula = MathTex(
            rf"f(x) = {function_latex}",
            font_size=36
        )
        formula.next_to(title, DOWN, buff=0.3)
        self.play(Write(formula))

        integral_formula = MathTex(
            rf"\int {function_latex}\,dx = {integral_latex} + C",
            font_size=32
        )
        integral_formula.next_to(formula, DOWN, buff=0.3)
        self.play(Write(integral_formula))

        numeric_function = sp.lambdify(x, expression, modules=["numpy"])

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-5, 10, 1],
            x_length=8,
            y_length=3.5,
            tips=False
        )
        axes.shift(DOWN * 1.5)

        graph = axes.plot(
            lambda t: float(numeric_function(t)),
            x_range=[-3, 3]
        )

        self.play(Create(axes))
        self.play(Create(graph), run_time=3)
        self.wait(2)