from manim import *


class Applications(Scene):

    def construct(self):

        # Title
        title = Text(
            "Applications of Integration",
            font_size=36
        )

        self.play(Write(title))
        self.wait(1)

        self.play(
            title.animate.to_edge(UP)
        )

        # Real-world idea
        idea = Text(
            "Integration can find displacement from velocity",
            font_size=28
        )

        self.play(Write(idea))
        self.wait(2)

        self.play(
            idea.animate.next_to(title, DOWN)
        )

        # Velocity
        velocity = Text(
            "Velocity = 2t + 3",
            font_size=32
        )

        self.play(Write(velocity))
        self.wait(2)

        self.play(
            velocity.animate.next_to(idea, DOWN)
        )

        # Integration step
        integration = Text(
            "Integrate velocity to find displacement",
            font_size=28
        )

        self.play(Write(integration))
        self.wait(2)

        self.play(
            integration.animate.next_to(velocity, DOWN)
        )

        # Displacement
        displacement = Text(
            "Displacement = t² + 3t + C",
            font_size=32
        )

        self.play(Write(displacement))
        self.wait(2)

        self.play(
            displacement.animate.next_to(integration, DOWN)
        )

        # Initial condition
        initial = Text(
            "If initial displacement = 0, then C = 0",
            font_size=26
        )

        self.play(Write(initial))
        self.wait(2)

        self.play(
            initial.animate.next_to(displacement, DOWN)
        )

        # Final result
        final = Text(
            "Displacement = t² + 3t",
            font_size=36
        )

        self.play(
            FadeOut(idea),
            FadeOut(velocity),
            FadeOut(integration),
            FadeOut(initial),
            Transform(displacement, final)
        )

        self.wait(3)