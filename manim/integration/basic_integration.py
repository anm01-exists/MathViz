from manim import *


class BasicIntegration(Scene):

    def construct(self):

        # Title
        title = Text(
            "Basic Integration",
            font_size=36
        )

        self.play(Write(title))
        self.wait(1)

        # Move title to top
        self.play(
            title.animate.to_edge(UP)
        )

        # Formula
        formula = Text(
            "Integral of x² dx = x³/3 + C",
            font_size=32
        )

        self.play(Write(formula))
        self.wait(2)

        # Move formula below title
        self.play(
            formula.animate.next_to(title, DOWN)
        )

        # Create axes WITHOUT numbers
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={
                "include_ticks": False
            },
        )

        self.play(Create(axes))

        # Curve y = x²
        curve = axes.plot(
            lambda x: x ** 2,
            x_range=[-1, 3.2]
        )

        self.play(Create(curve))
        self.wait(2)

        # Explanation
        explanation = Text(
            "Integration gives an antiderivative",
            font_size=26
        )

        explanation.to_edge(DOWN)

        self.play(Write(explanation))
        self.wait(2)

        # Final result
        final = Text(
            "Result: x³/3 + C",
            font_size=36
        )

        self.play(
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(explanation),
            Transform(formula, final)
        )

        self.wait(3)