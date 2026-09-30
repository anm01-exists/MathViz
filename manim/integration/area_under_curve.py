from manim import *


class AreaUnderCurve(Scene):

    def construct(self):

        # Title
        title = Text(
            "Area Under a Curve",
            font_size=36
        )

        self.play(Write(title))
        self.wait(1)

        self.play(
            title.animate.to_edge(UP)
        )

        # Explanation
        explanation = Text(
            "The area under a curve can be found using integration",
            font_size=26
        )

        self.play(Write(explanation))
        self.wait(2)

        self.play(
            explanation.animate.next_to(title, DOWN)
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
            x_range=[0, 3]
        )

        self.play(Create(curve))
        self.wait(2)

        # Shade area
        area = axes.get_area(
            curve,
            x_range=[0, 3]
        )

        self.play(
            FadeIn(area)
        )

        self.wait(2)

        # Area description
        area_text = Text(
            "Shaded region = Area under the curve",
            font_size=26
        )

        area_text.to_edge(DOWN)

        self.play(
            Write(area_text)
        )

        self.wait(2)

        # Final result
        result = Text(
            "For y = x² from 0 to 3, Area = 9",
            font_size=30
        )

        self.play(
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(area),
            FadeOut(area_text),
            Transform(explanation, result)
        )

        self.wait(3)