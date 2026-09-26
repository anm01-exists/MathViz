import os
import json
from manim import *


def load_json_from_env():
    path = os.getenv("MATHVIZ_INPUT_JSON")

    if not path:
        raise RuntimeError("MATHVIZ_INPUT_JSON is not set.")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------
# GLOBAL STYLE
# ---------------------------------------------------------

Text.set_default(color=BLACK)
Tex.set_default(color=BLACK)
MathTex.set_default(color=BLACK)


class WhatIsALimit(Scene):

    def construct(self):

        # ---------------------------------------------------------
        # BACKGROUND
        # ---------------------------------------------------------

        self.camera.background_color = "#FAF9F6"

        # =========================================================
        # SECTION 1 — TITLE
        # =========================================================

        title = Text(
            "What is a Limit?",
            font_size=48
        )

        subtitle = Text(
            "Understanding the idea of approaching a value",
            font_size=26
        )

        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)

        self.clear()

        # =========================================================
        # SECTION 2 — BASIC IDEA
        # =========================================================

        title = Text(
            "The Basic Idea",
            font_size=38
        ).to_edge(UP)

        statement = Text(
            "A limit asks:",
            font_size=32
        )

        question1 = Text(
            "What value does a function approach",
            font_size=30
        )

        question2 = Text(
            "as x gets closer and closer to a number?",
            font_size=30
        )

        statement.next_to(title, DOWN, buff=0.8)
        question1.next_to(statement, DOWN, buff=0.4)
        question2.next_to(question1, DOWN, buff=0.2)

        self.play(Write(title))
        self.play(Write(statement))
        self.play(Write(question1))
        self.play(Write(question2))

        self.wait(3)

        self.clear()

        # =========================================================
        # SECTION 3 — GRAPH
        # =========================================================

        title = Text(
            "Let's see it on a graph",
            font_size=36
        ).to_edge(UP)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 7, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "font_size": 20,
                "color": BLACK
            }
        ).shift(DOWN * 0.4)

        x_label = MathTex("x").next_to(
            axes.x_axis,
            RIGHT,
            buff=0.15
        )

        y_label = MathTex("f(x)").next_to(
            axes.y_axis,
            UP,
            buff=0.15
        )

        graph = axes.plot(
            lambda x: x + 2,
            x_range=[0.2, 4.8],
            color=GREEN
        )

        function = MathTex(
            "f(x)=x+2"
        ).scale(0.9)

        function.to_corner(UR)

        self.play(Write(title))
        self.play(Create(axes))
        self.play(
            Write(x_label),
            Write(y_label)
        )
        self.play(Create(graph))
        self.play(Write(function))

        self.wait(3)

        self.clear()

        # =========================================================
        # SECTION 4 — TARGET POINT
        # =========================================================

        title = Text(
            "Suppose we are interested in x = 2",
            font_size=34
        ).to_edge(UP)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 7, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "font_size": 20,
                "color": BLACK
            }
        ).shift(DOWN * 0.4)

        graph = axes.plot(
            lambda x: x + 2,
            x_range=[0.2, 4.8],
            color=GREEN
        )

        vertical = DashedLine(
            axes.c2p(2, 0),
            axes.c2p(2, 4),
            color=BLACK
        )

        horizontal = DashedLine(
            axes.c2p(0, 4),
            axes.c2p(2, 4),
            color=BLACK
        )

        point = Dot(
            axes.c2p(2, 4),
            radius=0.11,
            color=RED
        )

        x_value = MathTex(
            "x=2"
        ).scale(0.9)

        y_value = MathTex(
            "f(x)=4"
        ).scale(0.9)

        x_value.next_to(
            axes.c2p(2, 0),
            DOWN,
            buff=0.2
        )

        y_value.next_to(
            axes.c2p(0, 4),
            LEFT,
            buff=0.2
        )

        self.play(Write(title))
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Create(vertical))
        self.play(Create(horizontal))

        self.play(
            Write(x_value),
            Write(y_value)
        )

        self.play(GrowFromCenter(point))

        self.wait(3)

        self.clear()

        # =========================================================
        # SECTION 5 — APPROACH FROM LEFT
        # =========================================================

        title = Text(
            "Approaching x = 2 from the LEFT",
            font_size=34
        ).to_edge(UP)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 7, 1],
            x_length=7.5,
            y_length=4.8,
            axis_config={
                "include_numbers": True,
                "font_size": 20,
                "color": BLACK
            }
        ).shift(DOWN * 0.35)

        graph = axes.plot(
            lambda x: x + 2,
            x_range=[0.2, 4.8],
            color=GREEN
        )

        self.play(Write(title))
        self.play(Create(axes))
        self.play(Create(graph))

        positions = [
            (1.2, 3.2),
            (1.6, 3.6),
            (1.9, 3.9),
            (1.99, 3.99)
        ]

        dot = Dot(
            axes.c2p(
                positions[0][0],
                positions[0][1]
            ),
            radius=0.11,
            color=BLUE
        )

        self.play(FadeIn(dot))

        for x, y in positions[1:]:

            self.play(
                dot.animate.move_to(
                    axes.c2p(x, y)
                ),
                run_time=1
            )

        direction = MathTex(
            "x\\to2^-"
        ).scale(1.1)

        result = MathTex(
            "f(x)\\to4"
        ).scale(1.1)

        explanation = Text(
            "From the left, the function gets closer to 4.",
            font_size=25
        )

        direction.to_edge(LEFT).shift(DOWN * 2.8)

        result.next_to(
            direction,
            RIGHT,
            buff=0.5
        )

        explanation.to_edge(DOWN)

        self.play(
            Write(direction),
            Write(result)
        )

        self.play(
            Write(explanation)
        )

        self.wait(3)

        self.clear()

        # =========================================================
        # SECTION 6 — APPROACH FROM RIGHT
        # =========================================================

        title = Text(
            "Approaching x = 2 from the RIGHT",
            font_size=34
        ).to_edge(UP)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 7, 1],
            x_length=7.5,
            y_length=4.8,
            axis_config={
                "include_numbers": True,
                "font_size": 20,
                "color": BLACK
            }
        ).shift(DOWN * 0.35)

        graph = axes.plot(
            lambda x: x + 2,
            x_range=[0.2, 4.8],
            color=GREEN
        )

        self.play(Write(title))
        self.play(Create(axes))
        self.play(Create(graph))

        positions = [
            (3.2, 5.2),
            (2.5, 4.5),
            (2.1, 4.1),
            (2.01, 4.01)
        ]

        dot = Dot(
            axes.c2p(
                positions[0][0],
                positions[0][1]
            ),
            radius=0.11,
            color=BLUE
        )

        self.play(FadeIn(dot))

        for x, y in positions[1:]:

            self.play(
                dot.animate.move_to(
                    axes.c2p(x, y)
                ),
                run_time=1
            )

        direction = MathTex(
            "x\\to2^+"
        ).scale(1.1)

        result = MathTex(
            "f(x)\\to4"
        ).scale(1.1)

        explanation = Text(
            "From the right, the function also gets closer to 4.",
            font_size=25
        )

        direction.to_edge(LEFT).shift(DOWN * 2.8)

        result.next_to(
            direction,
            RIGHT,
            buff=0.5
        )

        explanation.to_edge(DOWN)

        self.play(
            Write(direction),
            Write(result)
        )

        self.play(
            Write(explanation)
        )

        self.wait(3)

        self.clear()

        # =========================================================
        # SECTION 7 — LEFT AND RIGHT LIMITS
        # =========================================================

        title = Text(
            "Left-hand and Right-hand Limits",
            font_size=34
        ).to_edge(UP)

        left = MathTex(
            "\\lim_{x\\to2^-} f(x)=4"
        ).scale(1.2)

        right = MathTex(
            "\\lim_{x\\to2^+} f(x)=4"
        ).scale(1.2)

        left.move_to(UP * 0.8)
        right.move_to(DOWN * 0.8)

        self.play(Write(title))

        self.play(
            Write(left)
        )

        self.play(
            Write(right)
        )

        self.wait(2)

        condition = Text(
            "Both sides approach the same value.",
            font_size=28
        ).to_edge(DOWN)

        self.play(
            Write(condition)
        )

        self.wait(3)

        self.clear()

        # =========================================================
        # SECTION 8 — TWO-SIDED LIMIT
        # =========================================================

        title = Text(
            "Therefore, the two-sided limit exists",
            font_size=34
        ).to_edge(UP)

        limit = MathTex(
            "\\boxed{\\lim_{x\\to2}f(x)=4}"
        ).scale(1.5)

        explanation = Text(
            "The left-hand and right-hand limits are equal.",
            font_size=25
        ).to_edge(DOWN)

        self.play(
            Write(title)
        )

        self.play(
            Write(limit)
        )

        self.play(
            Write(explanation)
        )

        self.wait(4)

        self.clear()

        # =========================================================
        # SECTION 9 — MORE INTERESTING EXAMPLE
        # =========================================================

        title = Text(
            "A More Interesting Example",
            font_size=36
        ).to_edge(UP)

        function = MathTex(
            "f(x)=\\frac{x^2-4}{x-2}"
        ).scale(1.3)

        question = Text(
            "What happens as x approaches 2?",
            font_size=28
        )

        function.move_to(UP * 0.8)

        question.next_to(
            function,
            DOWN,
            buff=0.5
        )

        self.play(
            Write(title)
        )

        self.play(
            Write(function)
        )

        self.play(
            Write(question)
        )

        self.wait(3)

        self.clear()

        # =========================================================
        # SECTION 10 — FACTORING
        # =========================================================

        title = Text(
            "Simplify the expression",
            font_size=36
        ).to_edge(UP)

        step1 = MathTex(
            "\\frac{x^2-4}{x-2}"
        ).scale(1.2)

        step2 = MathTex(
            "=\\frac{(x-2)(x+2)}{x-2}"
        ).scale(1.2)

        step3 = MathTex(
            "=x+2,\\qquad x\\ne2"
        ).scale(1.2)

        step1.move_to(UP * 1.2)
        step2.move_to(ORIGIN)
        step3.move_to(DOWN * 1.2)

        self.play(
            Write(title)
        )

        self.play(
            Write(step1)
        )

        self.wait(1)

        self.play(
            Write(step2)
        )

        self.wait(1)

        self.play(
            Write(step3)
        )

        self.wait(3)

        self.clear()

        # =========================================================
        # SECTION 11 — HOLE ON GRAPH
        # =========================================================

        title = Text(
            "The graph has a hole at x = 2",
            font_size=34
        ).to_edge(UP)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 7, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "font_size": 20,
                "color": BLACK
            }
        ).shift(DOWN * 0.35)

        graph = axes.plot(
            lambda x: x + 2,
            x_range=[0.2, 4.8],
            color=GREEN
        )

        hole = Circle(
            radius=0.12,
            color=BLACK,
            stroke_width=4
        )

        hole.move_to(
            axes.c2p(2, 4)
        )

        explanation1 = Text(
            "The function is undefined at x = 2.",
            font_size=25
        )

        explanation2 = Text(
            "But the graph still approaches 4.",
            font_size=25
        )

        explanation1.to_edge(DOWN).shift(UP * 0.45)

        explanation2.to_edge(DOWN).shift(DOWN * 0.1)

        self.play(
            Write(title)
        )

        self.play(
            Create(axes)
        )

        self.play(
            Create(graph)
        )

        self.play(
            Create(hole)
        )

        self.play(
            Write(explanation1)
        )

        self.play(
            Write(explanation2)
        )

        self.wait(4)

        self.clear()

        # =========================================================
        # SECTION 12 — FINAL LIMIT
        # =========================================================

        title = Text(
            "So the limit is...",
            font_size=38
        ).to_edge(UP)

        final_limit = MathTex(
            "\\boxed{"
            "\\lim_{x\\to2}"
            "\\frac{x^2-4}{x-2}"
            "=4"
            "}"
        ).scale(1.4)

        final_limit.move_to(ORIGIN)

        note = Text(
            "The limit depends on what happens near x = 2.",
            font_size=27
        ).to_edge(DOWN)

        self.play(
            Write(title)
        )

        self.play(
            Write(final_limit)
        )

        self.play(
            Write(note)
        )

        self.wait(4)

        self.clear()

        # =========================================================
        # SECTION 13 — FINAL SUMMARY
        # =========================================================

        title = Text(
            "Remember These 3 Ideas",
            font_size=38
        ).to_edge(UP)

        point1 = Text(
            "1. x gets closer to a value",
            font_size=28
        )

        point2 = Text(
            "2. f(x) gets closer to another value",
            font_size=28
        )

        point3 = Text(
            "3. If both sides agree, the two-sided limit exists",
            font_size=28
        )

        points = VGroup(
            point1,
            point2,
            point3
        ).arrange(
            DOWN,
            buff=0.45
        )

        points.move_to(ORIGIN)

        self.play(
            Write(title)
        )

        for point in points:
            self.play(
                Write(point)
            )
            self.wait(1)

        self.wait(4)

class LimitFromJSON(Scene):
    def construct(self):
        import json
        from sympy import sympify, symbols, factor, simplify, latex

        # Background
        self.camera.background_color = "#FFF8E7"

        # --------------------------------
        # READ SOLVER OUTPUT
        # --------------------------------
        with open("examples/limit_example.json", "r") as f:
            data = json.load(f)

        expression = data["expression"]
        variable = data["variable"]
        point = data["point"]
        result = data["result"]

        x = symbols(variable)
        expr = sympify(expression)

        factored = factor(expr)
        simplified = simplify(expr)

        # --------------------------------
        # TITLE
        # --------------------------------
        title = Text(
            "Evaluating a Limit",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # --------------------------------
        # ORIGINAL PROBLEM
        # --------------------------------
        heading = Text(
            "Find the limit",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        problem = MathTex(
            rf"\lim_{{{variable}\to{point}}}"
            rf"{latex(expr)}",
            font_size=48,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(problem))
        self.wait(3)

        # --------------------------------
        # DIRECT SUBSTITUTION
        # --------------------------------
        substitution = MathTex(
            rf"\lim_{{{variable}\to{point}}}"
            r"\frac{2^2-4}{2-2}",
            font_size=48,
            color=BLACK
        )

        self.play(
            ReplacementTransform(problem, substitution)
        )
        self.wait(3)

        # --------------------------------
        # INDETERMINATE FORM
        # --------------------------------
        zero = MathTex(
            r"\frac{0}{0}",
            font_size=60,
            color=RED
        )

        explanation = Text(
            "This is an indeterminate form",
            font_size=28,
            color=BLACK
        ).to_edge(DOWN)

        self.play(
            ReplacementTransform(substitution, zero)
        )

        self.play(Write(explanation))
        self.wait(3)

        # --------------------------------
        # FACTORIZATION
        # --------------------------------
        self.play(
            FadeOut(zero),
            FadeOut(explanation),
            FadeOut(heading)
        )

        factor_heading = Text(
            "Factor the expression",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        factored_tex = MathTex(
            latex(factored),
            font_size=48,
            color=BLACK
        )

        self.play(Write(factor_heading))
        self.play(Write(factored_tex))
        self.wait(3)

        # --------------------------------
        # SIMPLIFICATION
        # --------------------------------
        simplify_note = Text(
            "Cancel the common factor",
            font_size=28,
            color=BLACK
        ).to_edge(DOWN)

        simplified_tex = MathTex(
            latex(simplified),
            font_size=60,
            color=BLACK
        )

        self.play(Write(simplify_note))

        self.play(
            ReplacementTransform(
                factored_tex,
                simplified_tex
            )
        )

        self.wait(3)

        # --------------------------------
        # SUBSTITUTE AGAIN
        # --------------------------------
        self.play(FadeOut(simplify_note))

        final_substitution = MathTex(
            rf"{point}+2",
            font_size=60,
            color=BLACK
        )

        self.play(
            ReplacementTransform(
                simplified_tex,
                final_substitution
            )
        )

        self.wait(2)

        # --------------------------------
        # FINAL ANSWER
        # --------------------------------
        answer = MathTex(
            rf"\boxed{{{result}}}",
            font_size=72,
            color=GREEN
        )

        self.play(
            ReplacementTransform(
                final_substitution,
                answer
            )
        )

        self.wait(4)

        # --------------------------------
        # GRAPH
        # --------------------------------
        self.play(FadeOut(factor_heading))
        self.play(FadeOut(answer))

        graph_title = Text(
            "Graphical Interpretation",
            font_size=32,
            color=BLACK
        ).to_edge(UP)

        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[0, 7, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": BLACK}
        )

        graph = axes.plot(
            lambda t: t + 2,
            x_range=[-1, 5],
            color=GREEN
        )

        hole = Circle(
            radius=0.09,
            color=RED,
            stroke_width=4
        ).move_to(
            axes.c2p(point, float(result))
        )

        label = MathTex(
            rf"({point},{result})",
            font_size=28,
            color=BLACK
        ).next_to(hole, UP)

        self.play(Write(graph_title))
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Create(hole))
        self.play(Write(label))

        self.wait(4)

        # --------------------------------
        # FINAL CONCLUSION
        # --------------------------------
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(graph),
            FadeOut(hole),
            FadeOut(label)
        )

        final = MathTex(
            rf"\boxed{{\displaystyle\lim_{{{variable}\to{point}}}"
            rf"{latex(expr)}={result}}}",
            font_size=42,
            color=BLACK
        )

        self.play(Write(final))
        self.wait(5)
class OneSidedLimitFromJSON(Scene):
     def construct(self):
        import json

        self.camera.background_color = "#FFF8E7"

        # -----------------------------
        # READ JSON
        # -----------------------------
        with open("examples/one_sided_limit_example.json", "r") as f:
            data = json.load(f)

        expression = data["expression"]
        variable = data["variable"]
        point = data["point"]

        left_result = data["left"]["result"]
        right_result = data["right"]["result"]

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "One-Sided Limits",
            font_size=44,
            color=BLACK
        )

        subtitle = MathTex(
            r"\text{Approaching a point from one side}",
            font_size=30,
            color=BLACK
        )

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(3)

        self.play(
            FadeOut(title),
            FadeOut(subtitle)
        )

        # -----------------------------
        # ORIGINAL PROBLEM
        # -----------------------------
        heading = Text(
            "Consider the function",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        function = MathTex(
            r"f(x)=\frac{1}{x}",
            font_size=52,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(function))
        self.wait(3)

        self.play(
            FadeOut(heading),
            FadeOut(function)
        )

        # -----------------------------
        # LEFT-HAND LIMIT
        # -----------------------------
        left_heading = Text(
            "Approaching from the LEFT",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        left_limit = MathTex(
            r"\lim_{x\to0^-}\frac{1}{x}",
            font_size=52,
            color=BLACK
        )

        self.play(Write(left_heading))
        self.play(Write(left_limit))
        self.wait(3)

        left_answer = MathTex(
            r"=-\infty",
            font_size=60,
            color=RED
        ).next_to(left_limit, DOWN)

        self.play(Write(left_answer))
        self.wait(3)

        # -----------------------------
        # RIGHT-HAND LIMIT
        # -----------------------------
        self.play(
            FadeOut(left_heading),
            FadeOut(left_limit),
            FadeOut(left_answer)
        )

        right_heading = Text(
            "Approaching from the RIGHT",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        right_limit = MathTex(
            r"\lim_{x\to0^+}\frac{1}{x}",
            font_size=52,
            color=BLACK
        )

        self.play(Write(right_heading))
        self.play(Write(right_limit))
        self.wait(3)

        right_answer = MathTex(
            r"=+\infty",
            font_size=60,
            color=GREEN
        ).next_to(right_limit, DOWN)

        self.play(Write(right_answer))
        self.wait(3)

        # -----------------------------
        # GRAPH
        # -----------------------------
        self.play(
            FadeOut(right_heading),
            FadeOut(right_limit),
            FadeOut(right_answer)
        )

        graph_title = Text(
            "Graphical Interpretation",
            font_size=32,
            color=BLACK
        ).to_edge(UP)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-6, 6, 2],
            x_length=8,
            y_length=6,
            axis_config={"color": BLACK}
        )

        left_graph = axes.plot(
            lambda x: 1 / x,
            x_range=[-4, -0.15],
            color=RED
        )

        right_graph = axes.plot(
            lambda x: 1 / x,
            x_range=[0.15, 4],
            color=GREEN
        )

        vertical_line = DashedLine(
            axes.c2p(0, -6),
            axes.c2p(0, 6),
            color=BLACK
        )

        self.play(Write(graph_title))
        self.play(Create(axes))
        self.play(Create(left_graph))
        self.play(Create(right_graph))
        self.play(Create(vertical_line))

        self.wait(4)

        # -----------------------------
        # COMPARISON
        # -----------------------------
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(left_graph),
            FadeOut(right_graph),
            FadeOut(vertical_line)
        )

        comparison_title = Text(
            "Compare the two one-sided limits",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        comparison = VGroup(
            MathTex(
                r"\lim_{x\to0^-}\frac{1}{x}=-\infty",
                font_size=40,
                color=RED
            ),
            MathTex(
                r"\lim_{x\to0^+}\frac{1}{x}=+\infty",
                font_size=40,
                color=GREEN
            )
        ).arrange(DOWN, buff=0.5)

        self.play(Write(comparison_title))
        self.play(Write(comparison))
        self.wait(4)

        # -----------------------------
        # FINAL CONCLUSION
        # -----------------------------
        self.play(
            FadeOut(comparison_title),
            FadeOut(comparison)
        )

        conclusion = VGroup(
            Text(
                "The two sides are different.",
                font_size=32,
                color=BLACK
            ),
            MathTex(
                r"\therefore\quad \lim_{x\to0}\frac{1}{x}"
                r"\text{ does not exist}",
                font_size=42,
                color=RED
            )
        ).arrange(DOWN, buff=0.5)

        self.play(Write(conclusion))
        self.wait(5)
class TwoSidedLimitFromJSON(Scene):
    def construct(self):
        import json

        self.camera.background_color = "#FFF8E7"

        # -----------------------------
        # READ JSON
        # -----------------------------
        with open("examples/two_sided_limit_example.json", "r") as f:
            data = json.load(f)

        variable = data["variable"]
        point = data["point"]
        expression = data["expression"]

        left_result = data["left_result"]
        right_result = data["right_result"]
        exists = data["exists"]

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "Two-Sided Limits",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # -----------------------------
        # PROBLEM
        # -----------------------------
        heading = Text(
            "Consider the limit",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        problem = MathTex(
            rf"\lim_{{{variable}\to{point}}}\frac{{1}}{{{variable}}}",
            font_size=52,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(problem))
        self.wait(3)

        self.play(
            FadeOut(heading),
            FadeOut(problem)
        )

        # -----------------------------
        # LEFT-HAND LIMIT
        # -----------------------------
        left_heading = Text(
            "Left-Hand Limit",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        left = MathTex(
            rf"\lim_{{{variable}\to{point}^-}}\frac{{1}}{{{variable}}}"
            rf"={left_result}",
            font_size=46,
            color=RED
        )

        self.play(Write(left_heading))
        self.play(Write(left))
        self.wait(3)

        # -----------------------------
        # RIGHT-HAND LIMIT
        # -----------------------------
        self.play(
            FadeOut(left_heading),
            FadeOut(left)
        )

        right_heading = Text(
            "Right-Hand Limit",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        right = MathTex(
            rf"\lim_{{{variable}\to{point}^+}}\frac{{1}}{{{variable}}}"
            rf"={right_result}",
            font_size=46,
            color=GREEN
        )

        self.play(Write(right_heading))
        self.play(Write(right))
        self.wait(3)

        # -----------------------------
        # COMPARISON
        # -----------------------------
        self.play(
            FadeOut(right_heading),
            FadeOut(right)
        )

        compare_title = Text(
            "Compare the two sides",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        left_compare = MathTex(
            rf"LHL={left_result}",
            font_size=42,
            color=RED
        )

        right_compare = MathTex(
            rf"RHL={right_result}",
            font_size=42,
            color=GREEN
        )

        comparison = VGroup(
            left_compare,
            right_compare
        ).arrange(DOWN, buff=0.5)

        self.play(Write(compare_title))
        self.play(Write(comparison))
        self.wait(3)

        # -----------------------------
        # RESULT
        # -----------------------------
        self.play(
            FadeOut(compare_title),
            FadeOut(comparison)
        )

        if exists:
            result_text = VGroup(
                Text(
                    "LHL = RHL",
                    font_size=36,
                    color=GREEN
                ),
                MathTex(
                    r"\therefore\quad \text{The two-sided limit exists}",
                    font_size=38,
                    color=BLACK
                )
            ).arrange(DOWN, buff=0.5)
        else:
            result_text = VGroup(
                Text(
                    "LHL ≠ RHL",
                    font_size=36,
                    color=RED
                ),
                MathTex(
                    r"\therefore\quad \text{The two-sided limit does not exist}",
                    font_size=36,
                    color=BLACK
                )
            ).arrange(DOWN, buff=0.5)

        self.play(Write(result_text))
        self.wait(4)

        # -----------------------------
        # GRAPH
        # -----------------------------
        self.play(FadeOut(result_text))

        graph_title = Text(
            "Graphical Interpretation",
            font_size=32,
            color=BLACK
        ).to_edge(UP)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-6, 6, 2],
            x_length=8,
            y_length=6,
            axis_config={"color": BLACK}
        )

        left_graph = axes.plot(
            lambda x: 1 / x,
            x_range=[-4, -0.15],
            color=RED
        )

        right_graph = axes.plot(
            lambda x: 1 / x,
            x_range=[0.15, 4],
            color=GREEN
        )

        vertical = DashedLine(
            axes.c2p(0, -6),
            axes.c2p(0, 6),
            color=BLACK
        )

        self.play(Write(graph_title))
        self.play(Create(axes))
        self.play(Create(left_graph))
        self.play(Create(right_graph))
        self.play(Create(vertical))

        self.wait(4)

        # -----------------------------
        # FINAL
        # -----------------------------
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(left_graph),
            FadeOut(right_graph),
            FadeOut(vertical)
        )

        if exists:
            final = MathTex(
                rf"\boxed{{\lim_{{{variable}\to{point}}}"
                rf"\frac{{1}}{{{variable}}}={left_result}}}",
                font_size=44,
                color=BLACK
            )
        else:
            final = VGroup(
                MathTex(
                    rf"\lim_{{{variable}\to{point}}}"
                    rf"\frac{{1}}{{{variable}}}",
                    font_size=44,
                    color=BLACK
                ),
                Text(
                    "does not exist",
                    font_size=34,
                    color=RED
                )
            ).arrange(DOWN, buff=0.4)

        self.play(Write(final))
        self.wait(5)
class LimitAtInfinityFromJSON(Scene):
    def construct(self):
        import json

        self.camera.background_color = "#FFF8E7"

        # -----------------------------
        # READ JSON
        # -----------------------------
        with open("examples/infinity_limit_example.json", "r") as f:
            data = json.load(f)

        variable = data["variable"]
        result = data["result"]

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "Limits at Infinity",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # -----------------------------
        # PROBLEM
        # -----------------------------
        heading = Text(
            "Find the limit",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        problem = MathTex(
            rf"\lim_{{{variable}\to\infty}}\frac{{1}}{{{variable}}}",
            font_size=52,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(problem))
        self.wait(3)

        # -----------------------------
        # IDEA
        # -----------------------------
        self.play(FadeOut(heading), FadeOut(problem))

        idea = Text(
            "As x becomes larger, 1/x becomes smaller.",
            font_size=30,
            color=BLACK
        )

        self.play(Write(idea))
        self.wait(3)
        self.play(FadeOut(idea))

        # -----------------------------
        # VALUES
        # -----------------------------
        values_title = Text(
            "Watch what happens as x increases",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        values = VGroup(
            MathTex(r"x=10 \quad\Rightarrow\quad \frac{1}{x}=0.1",
                    font_size=38, color=BLACK),
            MathTex(r"x=100 \quad\Rightarrow\quad \frac{1}{x}=0.01",
                    font_size=38, color=BLACK),
            MathTex(r"x=1000 \quad\Rightarrow\quad \frac{1}{x}=0.001",
                    font_size=38, color=BLACK)
        ).arrange(DOWN, buff=0.5)

        self.play(Write(values_title))

        for value in values:
            self.play(Write(value))
            self.wait(2)

        self.wait(2)

        self.play(
            FadeOut(values_title),
            FadeOut(values)
        )

        # -----------------------------
        # GRAPH
        # -----------------------------
        graph_title = Text(
            "Graphical Interpretation",
            font_size=32,
            color=BLACK
        ).to_edge(UP)

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-1, 5, 1],
            x_length=9,
            y_length=5,
            axis_config={"color": BLACK}
        )

        graph = axes.plot(
            lambda x: 1 / x,
            x_range=[0.2, 10],
            color=GREEN
        )

        x_axis = DashedLine(
            axes.c2p(0, 0),
            axes.c2p(10, 0),
            color=RED
        )

        asymptote_label = MathTex(
            r"y=0",
            font_size=30,
            color=RED
        ).next_to(
            axes.c2p(8, 0),
            DOWN
        )

        self.play(Write(graph_title))
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Create(x_axis))
        self.play(Write(asymptote_label))

        self.wait(4)

        # -----------------------------
        # FINAL ANSWER
        # -----------------------------
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(graph),
            FadeOut(x_axis),
            FadeOut(asymptote_label)
        )

        final = VGroup(
            MathTex(
                rf"\lim_{{{variable}\to\infty}}\frac{{1}}{{{variable}}}",
                font_size=48,
                color=BLACK
            ),
            MathTex(
                r"=0",
                font_size=70,
                color=GREEN
            )
        ).arrange(DOWN, buff=0.4)

        self.play(Write(final))
        self.wait(5)
class ContinuityFromJSON(Scene):
    def construct(self):
        import json

        self.camera.background_color = "#FFF8E7"

        # -----------------------------
        # READ JSON
        # -----------------------------
        with open("examples/continuity_example.json", "r") as f:
            data = json.load(f)

        variable = data["variable"]
        point = data["point"]
        expression = data["expression"]
        function_value = data["function_value"]
        limit_value = data["limit_value"]
        continuous = data["is_continuous"]

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "Continuity of a Function",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # -----------------------------
        # FUNCTION
        # -----------------------------
        heading = Text(
            "Consider the function",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        function = MathTex(
            rf"f({variable})={expression}",
            font_size=52,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(function))
        self.wait(3)

        self.play(
            FadeOut(heading),
            FadeOut(function)
        )

        # -----------------------------
        # CONDITION 1
        # -----------------------------
        condition_title = Text(
            "Condition 1: Find the function value",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        function_value_tex = MathTex(
            rf"f({point})={function_value}",
            font_size=52,
            color=BLACK
        )

        self.play(Write(condition_title))
        self.play(Write(function_value_tex))
        self.wait(3)

        self.play(
            FadeOut(condition_title),
            FadeOut(function_value_tex)
        )

        # -----------------------------
        # CONDITION 2
        # -----------------------------
        limit_title = Text(
            "Condition 2: Find the limit",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        limit_tex = MathTex(
            rf"\lim_{{{variable}\to{point}}} f({variable})"
            rf"={limit_value}",
            font_size=48,
            color=BLACK
        )

        self.play(Write(limit_title))
        self.play(Write(limit_tex))
        self.wait(3)

        self.play(
            FadeOut(limit_title),
            FadeOut(limit_tex)
        )

        # -----------------------------
        # COMPARISON
        # -----------------------------
        compare_title = Text(
            "Compare the two values",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        comparison = VGroup(
            MathTex(
                rf"f({point})={function_value}",
                font_size=42,
                color=BLACK
            ),
            MathTex(
                rf"\lim_{{{variable}\to{point}}}f({variable})"
                rf"={limit_value}",
                font_size=42,
                color=BLACK
            )
        ).arrange(DOWN, buff=0.5)

        self.play(Write(compare_title))
        self.play(Write(comparison))
        self.wait(3)

        self.play(
            FadeOut(compare_title),
            FadeOut(comparison)
        )

        # -----------------------------
        # CONTINUITY RESULT
        # -----------------------------
        if continuous:
            result = VGroup(
                Text(
                    "The values are equal.",
                    font_size=32,
                    color=BLACK
                ),
                MathTex(
                    r"\therefore\quad"
                    rf"\boxed{{\text{{Continuous at }}x={point}}}",
                    font_size=40,
                    color=GREEN
                )
            ).arrange(DOWN, buff=0.5)
        else:
            result = VGroup(
                Text(
                    "The values are different.",
                    font_size=32,
                    color=BLACK
                ),
                MathTex(
                    r"\therefore\quad"
                    rf"\boxed{{\text{{Not continuous at }}x={point}}}",
                    font_size=38,
                    color=RED
                )
            ).arrange(DOWN, buff=0.5)

        self.play(Write(result))
        self.wait(4)

        # -----------------------------
        # GRAPH
        # -----------------------------
        self.play(FadeOut(result))

        graph_title = Text(
            "Graphical Interpretation",
            font_size=32,
            color=BLACK
        ).to_edge(UP)

        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[0, 7, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": BLACK}
        )

        graph = axes.plot(
            lambda t: t**2,
            x_range=[-1, 2.6],
            color=GREEN
        )

        point_dot = Dot(
            axes.c2p(point, float(function_value)),
            color=RED
        )

        point_label = MathTex(
            rf"({point},{function_value})",
            font_size=28,
            color=BLACK
        ).next_to(point_dot, UP)

        self.play(Write(graph_title))
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Create(point_dot))
        self.play(Write(point_label))

        self.wait(4)

        # -----------------------------
        # FINAL
        # -----------------------------
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(graph),
            FadeOut(point_dot),
            FadeOut(point_label)
        )

        final = MathTex(
            rf"\boxed{{f({point})="
            rf"\lim_{{{variable}\to{point}}}f({variable})"
            rf"={function_value}}}",
            font_size=42,
            color=BLACK
        )

        self.play(Write(final))
        self.wait(5)
class DerivativeFromJSON(Scene):

    def construct(self):
        import json
        import os

        from sympy import sympify, symbols, lambdify, diff, latex

        self.camera.background_color = "#FFF8E7"

        # -------------------------------------------------
        # READ THE JSON PROVIDED BY THE BACKEND
        # -------------------------------------------------

        json_path = os.environ.get("MATHVIZ_INPUT_JSON")

        if not json_path:
            json_path = "examples/derivative_example.json"

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        expression = data["expression"]
        variable = data["variable"]
        derivative = data["derivative"]

        x = symbols(variable)

        expr = sympify(expression)
        derivative_expr = sympify(derivative)

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = Text(
            "Understanding Derivatives",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # -------------------------------------------------
        # FUNCTION
        # -------------------------------------------------

        heading = Text(
            "Start with the function",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        function = MathTex(
            rf"f({variable})={latex(expr)}",
            font_size=48,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(function))
        self.wait(3)

        self.play(
            FadeOut(heading),
            FadeOut(function)
        )

        # -------------------------------------------------
        # WHAT DOES DERIVATIVE MEAN?
        # -------------------------------------------------

        meaning = VGroup(
            Text(
                "The derivative tells us the",
                font_size=30,
                color=BLACK
            ),
            Text(
                "instantaneous rate of change",
                font_size=34,
                color=GREEN
            )
        ).arrange(DOWN, buff=0.3)

        self.play(Write(meaning))
        self.wait(3)
        self.play(FadeOut(meaning))

        # -------------------------------------------------
        # GRAPH
        # -------------------------------------------------

        graph_title = Text(
            "Geometrically, it represents the slope",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        # Create numerical functions
        f = lambdify(x, expr, "numpy")
        df = lambdify(x, derivative_expr, "numpy")

        # Use a safe graph region
        x_min = -3
        x_max = 3

        sample_x = [-3, -2, -1, 0, 1, 2, 3]

        try:
            sample_y = [
                float(f(v))
                for v in sample_x
                if abs(float(f(v))) < 100
            ]
        except Exception:
            sample_y = [0, 1, 2, 3]

        if not sample_y:
            sample_y = [0, 1, 2, 3]

        y_min = min(sample_y)
        y_max = max(sample_y)

        if y_min == y_max:
            y_min -= 2
            y_max += 2

        padding = max(2, (y_max - y_min) * 0.2)

        axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[
                y_min - padding,
                y_max + padding,
                max(1, round((y_max - y_min) / 5, 1))
            ],
            x_length=8,
            y_length=5.5,
            axis_config={"color": BLACK}
        )

        curve = axes.plot(
            f,
            x_range=[x_min, x_max],
            color=GREEN
        )

        self.play(Write(graph_title))
        self.play(Create(axes))
        self.play(Create(curve))
        self.wait(3)

        # -------------------------------------------------
        # TANGENT AT x = 1
        # -------------------------------------------------

        x0 = 1

        try:
            y0 = float(f(x0))
            slope = float(df(x0))
        except Exception:
            y0 = float(expr.subs(x, x0))
            slope = float(derivative_expr.subs(x, x0))

        point = Dot(
            axes.c2p(x0, y0),
            color=RED
        )

        tangent = axes.plot(
            lambda t: slope * (t - x0) + y0,
            x_range=[x_min, x_max],
            color=RED
        )

        tangent_label = MathTex(
            rf"\text{{tangent slope}}={latex(derivative_expr.subs(x, x0))}",
            font_size=28,
            color=BLACK
        ).to_corner(UR)

        self.play(Create(point))
        self.play(Create(tangent))
        self.play(Write(tangent_label))
        self.wait(4)

        # -------------------------------------------------
        # DERIVATIVE CALCULATION
        # -------------------------------------------------

        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(point),
            FadeOut(tangent),
            FadeOut(tangent_label)
        )

        calculation_title = Text(
            "Calculate the derivative",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        original = MathTex(
            rf"f({variable})={latex(expr)}",
            font_size=44,
            color=BLACK
        )

        self.play(Write(calculation_title))
        self.play(Write(original))
        self.wait(2)

        derivative_tex = MathTex(
            rf"f'({variable})={latex(derivative_expr)}",
            font_size=52,
            color=GREEN
        )

        self.play(
            ReplacementTransform(original, derivative_tex)
        )

        self.wait(4)

        # -------------------------------------------------
        # FINAL
        # -------------------------------------------------

        self.play(FadeOut(calculation_title))

        final = VGroup(
            MathTex(
                rf"\boxed{{f'({variable})={latex(derivative_expr)}}}",
                font_size=52,
                color=BLACK
            ),
            Text(
                "The derivative gives the slope of the curve.",
                font_size=28,
                color=BLACK
            )
        ).arrange(DOWN, buff=0.5)

        self.play(
            ReplacementTransform(
                derivative_tex,
                final[0]
            )
        )

        self.play(Write(final[1]))
        self.wait(5)
        
class TangentLineFromJSON(Scene):
    def construct(self):
        import json
        from sympy import symbols, sympify, latex

        self.camera.background_color = "#FFF8E7"

        # -----------------------------
        # READ JSON
        # -----------------------------
        with open("examples/tangent_line_example.json", "r") as f:
            data = json.load(f)

        variable = data["variable"]
        point = float(data["point"])
        function_value = float(data["function_value"])
        slope = float(data["slope"])
        tangent_line = sympify(data["tangent_line"])

        x = symbols(variable)

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "Tangent Line",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # -----------------------------
        # FUNCTION
        # -----------------------------
        heading = Text(
            "Start with the function",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        function = MathTex(
            r"f(x)=x^2",
            font_size=52,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(function))
        self.wait(3)

        self.play(
            FadeOut(heading),
            FadeOut(function)
        )

        # -----------------------------
        # GRAPH
        # -----------------------------
        graph_title = Text(
            "Choose the point x = 1",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[0, 8, 2],
            x_length=8,
            y_length=6,
            axis_config={"color": BLACK}
        )

        curve = axes.plot(
            lambda t: t**2,
            x_range=[-2, 2.7],
            color=GREEN
        )

        point_dot = Dot(
            axes.c2p(point, function_value),
            color=RED
        )

        point_label = MathTex(
            r"(1,1)",
            font_size=28,
            color=BLACK
        ).next_to(point_dot, UR)

        self.play(Write(graph_title))
        self.play(Create(axes))
        self.play(Create(curve))
        self.play(Create(point_dot))
        self.play(Write(point_label))
        self.wait(3)

        # -----------------------------
        # DERIVATIVE / SLOPE
        # -----------------------------
        slope_text = MathTex(
            r"f'(x)=2x",
            font_size=42,
            color=BLACK
        ).to_corner(UL)

        slope_value = MathTex(
            r"f'(1)=2",
            font_size=42,
            color=RED
        ).next_to(slope_text, DOWN)

        self.play(Write(slope_text))
        self.play(Write(slope_value))
        self.wait(3)

        # -----------------------------
        # TANGENT LINE
        # -----------------------------
        tangent = axes.plot(
            lambda t: slope * (t - point) + function_value,
            x_range=[-1.5, 2.5],
            color=RED
        )

        tangent_label = MathTex(
            r"y=2x-1",
            font_size=34,
            color=RED
        ).to_corner(UR)

        self.play(Create(tangent))
        self.play(Write(tangent_label))
        self.wait(4)

        # -----------------------------
        # EXPLANATION
        # -----------------------------
        explanation = Text(
            "The derivative gives the slope of the tangent.",
            font_size=27,
            color=BLACK
        ).to_edge(DOWN)

        self.play(Write(explanation))
        self.wait(4)

        # -----------------------------
        # FINAL
        # -----------------------------
        self.play(
            FadeOut(graph_title),
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(point_dot),
            FadeOut(point_label),
            FadeOut(slope_text),
            FadeOut(slope_value),
            FadeOut(tangent),
            FadeOut(tangent_label),
            FadeOut(explanation)
        )

        final = VGroup(
            MathTex(
                r"f'(1)=2",
                font_size=48,
                color=BLACK
            ),
            MathTex(
                r"\boxed{y=2x-1}",
                font_size=58,
                color=GREEN
            )
        ).arrange(DOWN, buff=0.5)

        self.play(Write(final))
        self.wait(5)
class PowerRuleFromJSON(Scene):
    def construct(self):
        import json

        self.camera.background_color = "#FFF8E7"

        # Read solver output
        with open("examples/power_rule_example.json", "r") as f:
            data = json.load(f)

        derivative = data["derivative"]

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "The Power Rule",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # -----------------------------
        # ORIGINAL FUNCTION
        # -----------------------------
        heading = Text(
            "Differentiate the function",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        original = MathTex(
            r"f(x)=x^5",
            font_size=58,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(original))
        self.wait(3)

        # -----------------------------
        # POWER RULE
        # -----------------------------
        self.play(
            FadeOut(heading),
            FadeOut(original)
        )

        rule_title = Text(
            "Power Rule",
            font_size=32,
            color=BLACK
        ).to_edge(UP)

        rule = MathTex(
            r"\frac{d}{dx}(x^n)=nx^{n-1}",
            font_size=52,
            color=BLACK
        )

        self.play(Write(rule_title))
        self.play(Write(rule))
        self.wait(4)

        # -----------------------------
        # APPLY THE RULE
        # -----------------------------
        self.play(
            FadeOut(rule_title),
            FadeOut(rule)
        )

        apply_title = Text(
            "Apply the rule to x⁵",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        step1 = MathTex(
            r"\frac{d}{dx}(x^5)",
            font_size=54,
            color=BLACK
        )

        step2 = MathTex(
            r"5x^{5-1}",
            font_size=54,
            color=BLACK
        )

        self.play(Write(apply_title))
        self.play(Write(step1))
        self.wait(2)

        self.play(
            TransformMatchingTex(step1, step2)
        )
        self.wait(3)

        # -----------------------------
        # SIMPLIFY
        # -----------------------------
        step3 = MathTex(
            rf"5x^4",
            font_size=64,
            color=GREEN
        )

        self.play(
            TransformMatchingTex(step2, step3)
        )
        self.wait(4)

        # -----------------------------
        # EXPLANATION
        # -----------------------------
        explanation = VGroup(
            Text(
                "Bring the exponent down",
                font_size=28,
                color=BLACK
            ),
            Text(
                "and subtract 1 from the exponent.",
                font_size=28,
                color=BLACK
            )
        ).arrange(DOWN, buff=0.25).to_edge(DOWN)

        self.play(Write(explanation))
        self.wait(4)

        # -----------------------------
        # FINAL ANSWER
        # -----------------------------
        self.play(
            FadeOut(apply_title),
            FadeOut(explanation)
        )

        final = MathTex(
            rf"\boxed{{f'(x)={derivative}}}",
            font_size=60,
            color=BLACK
        )

        self.play(
            ReplacementTransform(step3, final)
        )
        self.wait(5)
class SumRuleFromJSON(Scene):
    def construct(self):
        import json

        self.camera.background_color = "#FFF8E7"

        # Read solver output
        with open("examples/sum_rule_example.json", "r") as f:
            data = json.load(f)

        derivative = data["derivative"]

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "The Sum Rule",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # -----------------------------
        # ORIGINAL FUNCTION
        # -----------------------------
        heading = Text(
            "Differentiate the function",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        original = MathTex(
            r"f(x)=x^3+x^2",
            font_size=54,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(original))
        self.wait(3)

        self.play(
            FadeOut(heading),
            FadeOut(original)
        )

        # -----------------------------
        # SUM RULE
        # -----------------------------
        rule_title = Text(
            "Sum Rule",
            font_size=32,
            color=BLACK
        ).to_edge(UP)

        rule = MathTex(
            r"\frac{d}{dx}[f(x)+g(x)]"
            r"="
            r"\frac{d}{dx}f(x)+\frac{d}{dx}g(x)",
            font_size=42,
            color=BLACK
        )

        self.play(Write(rule_title))
        self.play(Write(rule))
        self.wait(4)

        self.play(
            FadeOut(rule_title),
            FadeOut(rule)
        )

        # -----------------------------
        # SPLIT THE TERMS
        # -----------------------------
        step_title = Text(
            "Differentiate each term separately",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        split = MathTex(
            r"\frac{d}{dx}(x^3+x^2)"
            r"="
            r"\frac{d}{dx}(x^3)"
            r"+"
            r"\frac{d}{dx}(x^2)",
            font_size=44,
            color=BLACK
        )

        self.play(Write(step_title))
        self.play(Write(split))
        self.wait(4)

        # -----------------------------
        # DIFFERENTIATE
        # -----------------------------
        differentiated = MathTex(
            r"3x^2+2x",
            font_size=60,
            color=GREEN
        )

        self.play(
            ReplacementTransform(split, differentiated)
        )
        self.wait(4)

        explanation = Text(
            "Differentiate each term, then add the results.",
            font_size=28,
            color=BLACK
        ).to_edge(DOWN)

        self.play(Write(explanation))
        self.wait(4)

        # -----------------------------
        # FINAL ANSWER
        # -----------------------------
        self.play(
            FadeOut(step_title),
            FadeOut(explanation)
        )

        final = MathTex(
            rf"\boxed{{f'(x)={derivative}}}",
            font_size=58,
            color=BLACK
        )

        self.play(
            ReplacementTransform(
                differentiated,
                final
            )
        )

        self.wait(5)
class ProductRuleFromJSON(Scene):
    def construct(self):
        import json

        self.camera.background_color = "#FFF8E7"

        with open("examples/product_rule_example.json", "r") as f:
            data = json.load(f)

        derivative = data["derivative"]

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "The Product Rule",
            font_size=44,
            color=BLACK
        )

        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # -----------------------------
        # ORIGINAL FUNCTION
        # -----------------------------
        heading = Text(
            "Differentiate the product",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        original = MathTex(
            r"f(x)=x^2(x+1)",
            font_size=54,
            color=BLACK
        )

        self.play(Write(heading))
        self.play(Write(original))
        self.wait(3)

        self.play(FadeOut(heading), FadeOut(original))

        # -----------------------------
        # RULE
        # -----------------------------
        rule_title = Text(
            "Product Rule",
            font_size=32,
            color=BLACK
        ).to_edge(UP)

        rule = MathTex(
            r"(uv)'=u'v+uv'",
            font_size=58,
            color=BLACK
        )

        self.play(Write(rule_title))
        self.play(Write(rule))
        self.wait(4)

        self.play(FadeOut(rule_title), FadeOut(rule))

        # -----------------------------
        # IDENTIFY u AND v
        # -----------------------------
        identify_title = Text(
            "Identify the two factors",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        factors = VGroup(
            MathTex(r"u=x^2", font_size=48, color=BLACK),
            MathTex(r"v=x+1", font_size=48, color=BLACK)
        ).arrange(DOWN, buff=0.4)

        self.play(Write(identify_title))
        self.play(Write(factors))
        self.wait(3)

        self.play(FadeOut(identify_title), FadeOut(factors))

        # -----------------------------
        # DIFFERENTIATE
        # -----------------------------
        derivative_title = Text(
            "Differentiate each factor",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        derivatives = VGroup(
            MathTex(r"u'=2x", font_size=48, color=BLACK),
            MathTex(r"v'=1", font_size=48, color=BLACK)
        ).arrange(DOWN, buff=0.4)

        self.play(Write(derivative_title))
        self.play(Write(derivatives))
        self.wait(3)

        self.play(FadeOut(derivative_title), FadeOut(derivatives))

        # -----------------------------
        # APPLY RULE
        # -----------------------------
        apply_title = Text(
            "Apply the Product Rule",
            font_size=30,
            color=BLACK
        ).to_edge(UP)

        applied = MathTex(
            r"(2x)(x+1)+(x^2)(1)",
            font_size=48,
            color=BLACK
        )

        self.play(Write(apply_title))
        self.play(Write(applied))
        self.wait(3)

        # -----------------------------
        # SIMPLIFY
        # -----------------------------
        simplified = MathTex(
            r"x(3x+2)",
            font_size=54,
            color=BLACK
        )

        final_form = MathTex(
            r"3x^2+2x",
            font_size=62,
            color=GREEN
        )

        self.play(ReplacementTransform(applied, simplified))
        self.wait(2)

        self.play(ReplacementTransform(simplified, final_form))
        self.wait(4)

        # -----------------------------
        # FINAL ANSWER
        # -----------------------------
        self.play(FadeOut(apply_title))

        final = VGroup(
            MathTex(
                rf"\boxed{{f'(x)={derivative}}}",
                font_size=56,
                color=BLACK
            ),
            Text(
                "Differentiate the first factor, multiply by the second,",
                font_size=24,
                color=BLACK
            ),
            Text(
                "then add the first factor multiplied by the derivative of the second.",
                font_size=24,
                color=BLACK
            )
        ).arrange(DOWN, buff=0.3)

        self.play(FadeOut(final_form))
        self.play(Write(final))
        self.wait(5)
class QuotientRuleFromJSON(Scene):
    def construct(self):
        data = load_json_from_env()

        expression = data["expression"]
        u = data["u"]
        v = data["v"]
        u_prime = data["u_prime"]
        v_prime = data["v_prime"]
        result = data["result"]

        self.camera.background_color = "#FFF8E7"

        title = Text("Quotient Rule", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Given function
        given = MathTex(
            rf"f(x) = \frac{{{u}}}{{{v}}}",
            font_size=42
        )
        self.play(Write(given))
        self.wait(1)

        # Formula
        formula = MathTex(
            r"\left(\frac{u}{v}\right)' = "
            r"\frac{vu' - uv'}{v^2}",
            font_size=40
        )
        formula.next_to(given, DOWN, buff=0.7)

        self.play(Write(formula))
        self.wait(2)

        # Identify u and v
        identify = VGroup(
            MathTex(rf"u = {u}", font_size=34),
            MathTex(rf"v = {v}", font_size=34)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        identify.next_to(formula, DOWN, buff=0.6)

        self.play(Write(identify))
        self.wait(2)

        self.clear()

        title = Text("Step 1: Differentiate u and v", font_size=38)
        title.to_edge(UP)

        derivatives = VGroup(
            MathTex(rf"u' = {u_prime}", font_size=38),
            MathTex(rf"v' = {v_prime}", font_size=38)
        ).arrange(DOWN, buff=0.4)

        self.play(Write(title))
        self.play(Write(derivatives))
        self.wait(2)

        self.clear()

        title = Text("Step 2: Apply the Quotient Rule", font_size=38)
        title.to_edge(UP)

        apply_rule = MathTex(
            rf"f'(x) = \frac{{({v})({u_prime}) - ({u})({v_prime})}}{{({v})^2}}",
            font_size=36
        )

        self.play(Write(title))
        self.play(Write(apply_rule))
        self.wait(3)

        self.clear()

        title = Text("Step 3: Simplify", font_size=38)
        title.to_edge(UP)

        final = MathTex(
            rf"f'(x) = {result}",
            font_size=42
        )

        self.play(Write(title))
        self.play(Write(final))
        self.wait(2)

        box = SurroundingRectangle(final)

        self.play(Create(box))
        self.wait(2)

        conclusion = Text(
            "The quotient rule gives the derivative.",
            font_size=28
        )
        conclusion.next_to(final, DOWN, buff=0.7)

        self.play(Write(conclusion))
        self.wait(3)
class ChainRuleFromJSON(Scene):
    def construct(self):
        data = load_json_from_env()

        expression = data["expression"]
        outer = data["outer_function"]
        inner = data["inner_function"]
        result = data["result"]

        self.camera.background_color = "#FFF8E7"

        # Title
        title = Text("Chain Rule", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Given function
        given = MathTex(
            rf"f(x) = ({inner})^{{{outer}}}",
            font_size=40
        )
        self.play(Write(given))
        self.wait(2)

        # Chain rule formula
        formula = MathTex(
            r"\frac{d}{dx}[f(g(x))] = f'(g(x))g'(x)",
            font_size=36
        )
        formula.next_to(given, DOWN, buff=0.7)

        self.play(Write(formula))
        self.wait(2)

        self.clear()

        # Step 1
        title = Text("Step 1: Identify inner and outer functions", font_size=34)
        title.to_edge(UP)

        step1 = VGroup(
            MathTex(rf"\text{{Inner function: }}\ u(x) = {inner}", font_size=34),
            MathTex(rf"\text{{Outer function: }}\ v(u) = u^{{{outer}}}", font_size=34)
        ).arrange(DOWN, buff=0.45)

        self.play(Write(title))
        self.play(Write(step1))
        self.wait(2)

        self.clear()

        # Step 2
        title = Text("Step 2: Differentiate the outer function", font_size=34)
        title.to_edge(UP)

        outer_derivative = MathTex(
            rf"\frac{{d}}{{du}}(u^{{{outer}}}) = {outer}u^{{{int(outer)-1}}}",
            font_size=38
        )

        self.play(Write(title))
        self.play(Write(outer_derivative))
        self.wait(2)

        self.clear()

        # Step 3
        title = Text("Step 3: Multiply by the inner derivative", font_size=34)
        title.to_edge(UP)

        inner_derivative = MathTex(
            rf"\frac{{d}}{{dx}}({inner}) = 2x",
            font_size=36
        )

        self.play(Write(title))
        self.play(Write(inner_derivative))
        self.wait(2)

        self.clear()

        # Step 4
        title = Text("Step 4: Apply the Chain Rule", font_size=34)
        title.to_edge(UP)

        apply_rule = MathTex(
            rf"f'(x) = {outer}({inner})^{{{int(outer)-1}}}(2x)",
            font_size=36
        )

        self.play(Write(title))
        self.play(Write(apply_rule))
        self.wait(2)

        self.clear()

        # Final result
        title = Text("Final Answer", font_size=38)
        title.to_edge(UP)

        final = MathTex(
            rf"f'(x) = {result}",
            font_size=44
        )

        self.play(Write(title))
        self.play(Write(final))
        self.wait(2)

        box = SurroundingRectangle(final)
        self.play(Create(box))
        self.wait(2)
class DerivativeApplicationsFromJSON(Scene):
    def construct(self):
        data = load_json_from_env()

        expression = data["expression"]
        first_derivative = data["first_derivative"]
        second_derivative = data["second_derivative"]
        critical_points = data["critical_points"]
        classifications = data["classifications"]

        self.camera.background_color = "#FFF8E7"

        # Title
        title = Text("Applications of Derivatives", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Given function
        function = MathTex(
            r"f(x) = x^3 - 3x",
            font_size=42
        )

        self.play(Write(function))
        self.wait(2)

        self.clear()

        # Step 1: First derivative
        title = Text("Step 1: Find the First Derivative", font_size=36)
        title.to_edge(UP)

        derivative = MathTex(
            r"f'(x) = 3x^2 - 3",
            font_size=42
        )

        self.play(Write(title))
        self.play(Write(derivative))
        self.wait(2)

        self.clear()

        # Step 2: Critical points
        title = Text("Step 2: Find the Critical Points", font_size=36)
        title.to_edge(UP)

        critical = MathTex(
            r"f'(x)=0",
            font_size=38
        )

        points = MathTex(
            r"x=-1,\quad x=1",
            font_size=42
        )

        group = VGroup(critical, points).arrange(
            DOWN,
            buff=0.5
        )

        self.play(Write(title))
        self.play(Write(group))
        self.wait(2)

        self.clear()

        # Step 3: Second derivative
        title = Text("Step 3: Use the Second Derivative", font_size=36)
        title.to_edge(UP)

        second = MathTex(
            r"f''(x)=6x",
            font_size=42
        )

        self.play(Write(title))
        self.play(Write(second))
        self.wait(2)

        self.clear()

        # Step 4: Classification
        title = Text("Step 4: Classify the Critical Points", font_size=34)
        title.to_edge(UP)

        maximum = MathTex(
            r"f''(-1)<0 \Rightarrow \text{Local Maximum}",
            font_size=32
        )

        minimum = MathTex(
            r"f''(1)>0 \Rightarrow \text{Local Minimum}",
            font_size=32
        )

        classification_group = VGroup(
            maximum,
            minimum
        ).arrange(
            DOWN,
            buff=0.5
        )

        self.play(Write(title))
        self.play(Write(classification_group))
        self.wait(3)

        self.clear()

        # Graph
        title = Text("Visualizing the Function", font_size=36)
        title.to_edge(UP)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-5, 5, 1],
            x_length=9,
            y_length=5,
            axis_config={"include_numbers": True}
        )

        graph = axes.plot(
            lambda x: x**3 - 3*x,
            x_range=[-2.2, 2.2],
        )

        max_point = axes.c2p(-1, 2)
        min_point = axes.c2p(1, -2)

        max_dot = Dot(max_point)
        min_dot = Dot(min_point)

        max_label = MathTex(
            r"\text{Local Max }(-1,2)",
            font_size=26
        ).next_to(max_dot, UP)

        min_label = MathTex(
            r"\text{Local Min }(1,-2)",
            font_size=26
        ).next_to(min_dot, DOWN)

        self.play(Write(title))
        self.play(Create(axes))
        self.play(Create(graph))
        self.play(Create(max_dot))
        self.play(Write(max_label))
        self.play(Create(min_dot))
        self.play(Write(min_label))
        self.wait(3)

        self.clear()

        # Final answer
        title = Text("Final Result", font_size=40)
        title.to_edge(UP)

        final = VGroup(
            MathTex(r"\text{Critical Points: }x=-1,\;1", font_size=34),
            MathTex(r"x=-1\rightarrow\text{Local Maximum}", font_size=32),
            MathTex(r"x=1\rightarrow\text{Local Minimum}", font_size=32)
        ).arrange(
            DOWN,
            buff=0.45
        )

        self.play(Write(title))
        self.play(Write(final))
        self.wait(3)