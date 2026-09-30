from manim import *


class DefiniteIntegral(Scene):

    def construct(self):

        # Title
        title = Text(
            "Definite Integral",
            font_size=36
        )

        self.play(Write(title))
        self.wait(1)

        self.play(
            title.animate.to_edge(UP)
        )

        # Integral explanation
        formula = Text(
            "Integral of x² from 0 to 3",
            font_size=30
        )

        self.play(Write(formula))
        self.wait(2)

        self.play(
            formula.animate.next_to(title, DOWN)
        )

        # Axes without numbers
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={
                "include_ticks": False
            }
        )

        self.play(Create(axes))

        # Curve y = x²
        curve = axes.plot(
            lambda x: x ** 2,
            x_range=[0, 3.2]
        )

        self.play(Create(curve))
        self.wait(1)

        # Area under curve
        area = axes.get_area(
            curve,
            x_range=[0, 3]
        )

        self.play(
            FadeIn(area)
        )

        self.wait(2)

        # Explanation
        explanation = Text(
            "The definite integral gives the area",
            font_size=26
        )

        explanation.to_edge(DOWN)

        self.play(
            Write(explanation)
        )

        self.wait(2)

        # Final result
        result = Text(
            "Area = 9 square units",
            font_size=34
        )

        self.play(
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(area),
            FadeOut(explanation),
            Transform(formula, result)
        )

        self.wait(3)