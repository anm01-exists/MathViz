from manim import *

class TestManim(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait(2)