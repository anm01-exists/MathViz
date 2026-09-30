from manim import *


class Substitution(Scene):

    def construct(self):

        # Title
        title = Text(
            "Integration by Substitution",
            font_size=36
        )

        self.play(Write(title))
        self.wait(1)

        self.play(
            title.animate.to_edge(UP)
        )

        # Original integral
        original = Text(
            "Integral of 2x(x² + 1)³ dx",
            font_size=30
        )

        self.play(Write(original))
        self.wait(2)

        # Step 1
        step1 = Text(
            "Let u = x² + 1",
            font_size=30
        )

        self.play(
            original.animate.to_edge(UP)
        )

        self.play(Write(step1))
        self.wait(2)

        # Step 2
        step2 = Text(
            "Then du = 2x dx",
            font_size=30
        )

        self.play(
            step1.animate.next_to(original, DOWN)
        )

        self.play(Write(step2))
        self.wait(2)

        # Step 3
        step3 = Text(
            "Integral becomes: Integral of u³ du",
            font_size=30
        )

        self.play(
            step2.animate.next_to(step1, DOWN)
        )

        self.play(Write(step3))
        self.wait(2)

        # Step 4
        step4 = Text(
            "Integrate: u⁴/4 + C",
            font_size=30
        )

        self.play(
            step3.animate.next_to(step2, DOWN)
        )

        self.play(Write(step4))
        self.wait(2)

        # Final answer
        final = Text(
            "Substitute back: (x² + 1)⁴/4 + C",
            font_size=30
        )

        self.play(
            FadeOut(original),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            Transform(step4, final)
        )

        self.wait(3)