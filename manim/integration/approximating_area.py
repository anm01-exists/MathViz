from manim import *


class ApproximatingArea(Scene):

    def construct(self):

        # Title
        title = Text(
            "Approximating Areas",
            font_size=36
        )

        self.play(Write(title))
        self.wait(1)

        self.play(
            title.animate.to_edge(UP)
        )

        # Explanation
        explanation = Text(
            "We can approximate area using rectangles",
            font_size=28
        )

        self.play(Write(explanation))
        self.wait(2)

        self.play(
            explanation.animate.next_to(title, DOWN)
        )

        # Axes
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

        # Curve
        curve = axes.plot(
            lambda x: x ** 2,
            x_range=[0, 3]
        )

        self.play(Create(curve))
        self.wait(2)

        # Left rectangles
        left_rectangles = axes.get_riemann_rectangles(
            curve,
            x_range=[0, 3],
            dx=0.5,
            input_sample_type="left"
        )

        self.play(
            FadeIn(left_rectangles)
        )

        self.wait(2)

        left_text = Text(
            "Left endpoint approximation",
            font_size=25
        )

        left_text.to_edge(DOWN)

        self.play(
            Write(left_text)
        )

        self.wait(2)

        # Replace with right rectangles
        right_rectangles = axes.get_riemann_rectangles(
            curve,
            x_range=[0, 3],
            dx=0.5,
            input_sample_type="right"
        )

        self.play(
            FadeOut(left_text),
            Transform(
                left_rectangles,
                right_rectangles
            )
        )

        self.wait(2)

        right_text = Text(
            "Right endpoint approximation",
            font_size=25
        )

        right_text.to_edge(DOWN)

        self.play(
            Write(right_text)
        )

        self.wait(2)

        # Final explanation
        final = Text(
            "More rectangles → Better approximation",
            font_size=30
        )

        self.play(
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(left_rectangles),
            FadeOut(right_text),
            Transform(explanation, final)
        )

        self.wait(3)