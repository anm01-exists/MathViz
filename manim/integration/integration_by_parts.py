from manim import *


class IntegrationByParts(Scene):

    def construct(self):

        # Title
        title = Text(
            "Integration by Parts",
            font_size=36
        )

        self.play(Write(title))
        self.wait(1)

        self.play(
            title.animate.to_edge(UP)
        )

        # Formula
        formula = Text(
            "Integral u dv = uv - Integral v du",
            font_size=30
        )

        self.play(Write(formula))
        self.wait(2)

        self.play(
            formula.animate.next_to(title, DOWN)
        )

        # Example
        example = Text(
            "Example: Integral of x e^x dx",
            font_size=30
        )

        self.play(Write(example))
        self.wait(2)

        self.play(
            example.animate.next_to(formula, DOWN)
        )

        # Choose u
        step1 = Text(
            "Choose u = x",
            font_size=28
        )

        self.play(Write(step1))
        self.wait(1)

        self.play(
            step1.animate.next_to(example, DOWN)
        )

        # Choose dv
        step2 = Text(
            "Choose dv = e^x dx",
            font_size=28
        )

        self.play(Write(step2))
        self.wait(1)

        self.play(
            step2.animate.next_to(step1, DOWN)
        )

        # Find du and v
        step3 = Text(
            "du = dx        v = e^x",
            font_size=28
        )

        self.play(Write(step3))
        self.wait(2)

        self.play(
            step3.animate.next_to(step2, DOWN)
        )

        # Apply formula
        step4 = Text(
            "Result = x e^x - Integral e^x dx",
            font_size=28
        )

        self.play(Write(step4))
        self.wait(2)

        self.play(
            step4.animate.next_to(step3, DOWN)
        )

        # Final answer
        final = Text(
            "Final Answer: x e^x - e^x + C",
            font_size=32
        )

        self.play(
            FadeOut(formula),
            FadeOut(example),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            Transform(step4, final)
        )

        self.wait(3)