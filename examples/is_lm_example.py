from manim import Create, Scene
from manim_ec import ISLMDiagram


class ISLMScene(Scene):
    def construct(self):
        # IS: r = a/b - Y/b = 5 - 0.5Y
        # LM: r = (kY - Ms)/h = 0.5Y - 5
        # Equilibrium: 5 - 0.5Y = 0.5Y - 5 => Y=10... too high
        # Use defaults: a=10, b=2, ms=5, k=0.5, h=1
        diagram = ISLMDiagram()
        self.play(Create(diagram))
        self.wait()

        # Monetary expansion: increase money supply from 5 to 8
        # LM shifts right/down => lower r, higher Y
        self.play(diagram.shift_lm(ms=8))
        self.wait()
