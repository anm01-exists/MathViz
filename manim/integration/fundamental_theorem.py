from manim import *


class FundamentalTheorem(Scene):

    def construct(self):

        # Title
        title = Text(
            "Fundamental Theorem of Calculus",
            font_size=34
        )

        self.play(Write(title))
        self.wait(1)

        self.play(
            title.animate.to_edge(UP)
        )

        # Main idea
        statement = Text(
            "Integration and differentiation are inverse processes",
            font_size=26
        )

        self.play(Write(statement))
        self.wait(2)

        self.play(
            statement.animate.next_to(title, DOWN)
        )

        # Axes
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={
                "include_ticks": False
            }
        )

        self.play(Create(axes))

        # Original function
        curve = axes.plot(
            lambda x: x ** 2,
            x_range=[-1, 3.2]
        )

        self.play(Create(curve))
        self.wait(2)

        # Function label
        function_text = Text(
            "Original function: x²",
            font_size=26
        )

        function_text.to_edge(DOWN)

        self.play(
            Write(function_text)
        )

        self.wait(2)

        # Remove graph
        self.play(
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(function_text)
        )

        # Integration
        integration_text = Text(
            "Integrate: x²  →  x³/3 + C",
            font_size=32
        )

        self.play(
            Write(integration_text)
        )

        self.wait(2)

        # Differentiation
        differentiation_text = Text(
            "Differentiate: x³/3  →  x²",
            font_size=32
        )

        self.play(
            Transform(
                integration_text,
                differentiation_text
            )
        )

        self.wait(2)

        # Final idea
        final_text = Text(
            "Integration and differentiation are inverse processes",
            font_size=28
        )

        self.play(
            Transform(
                integration_text,
                final_text
            )
        )

        self.wait(3)