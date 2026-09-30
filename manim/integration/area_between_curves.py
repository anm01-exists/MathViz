from manim import *


class AreaBetweenCurves(Scene):

    def construct(self):

        # Title
        title = Text(
            "Area Between Two Curves",
            font_size=36
        )

        self.play(Write(title))
        self.wait(1)

        self.play(
            title.animate.to_edge(UP)
        )

        # Explanation
        explanation = Text(
            "Area between y = x and y = x²",
            font_size=28
        )

        self.play(Write(explanation))
        self.wait(2)

        self.play(
            explanation.animate.next_to(title, DOWN)
        )

        # Axes
        axes = Axes(
            x_range=[0, 1.5, 1],
            y_range=[0, 2, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "include_ticks": False
            }
        )

        self.play(Create(axes))

        # Upper curve: y = x
        upper_curve = axes.plot(
            lambda x: x,
            x_range=[0, 1]
        )

        # Lower curve: y = x²
        lower_curve = axes.plot(
            lambda x: x ** 2,
            x_range=[0, 1]
        )

        self.play(
            Create(upper_curve),
            Create(lower_curve)
        )

        self.wait(2)

        # Shade region between curves
        area = axes.get_area(
            upper_curve,
            x_range=[0, 1],
            bounded_graph=lower_curve
        )

        self.play(
            FadeIn(area)
        )

        self.wait(2)

        # Explanation
        area_text = Text(
            "Shaded region = Area between the curves",
            font_size=25
        )

        area_text.to_edge(DOWN)

        self.play(
            Write(area_text)
        )

        self.wait(2)

        # Final result
        result = Text(
            "Area = 1/6 square units",
            font_size=34
        )

        self.play(
            FadeOut(axes),
            FadeOut(upper_curve),
            FadeOut(lower_curve),
            FadeOut(area),
            FadeOut(area_text),
            Transform(explanation, result)
        )

        self.wait(3)