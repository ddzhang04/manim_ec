from manim import Create, Scene, Text, Write, UP
from manim_ec import ADASDiagram


class AdverseSupplyShockDefault(Scene):
    """Adverse supply shock with default (non-numbered) equilibrium labels."""
    def construct(self):
        diagram = ADASDiagram(m=20, v=1, sras_price=4, lras_y=5)
        self.play(Create(diagram))
        self.wait()

        label = Text("Adverse supply shock: costs ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.adverse_supply_shock(sras_price=6, show_arrows=True):
            self.play(anim)
            self.wait(0.5)
