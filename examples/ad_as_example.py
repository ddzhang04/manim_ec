from manim import Create, FadeOut, Scene, Text, Write, UP
from manim_ec import ADASDiagram


class PositiveDemandShock(Scene):
    """M increases → AD right → SRAS slowly adjusts up."""
    def construct(self):
        diagram = ADASDiagram(m=20, v=1, sras_price=4, lras_y=5)
        self.play(Create(diagram))
        self.wait()

        label = Text("Positive demand shock: M ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.positive_demand_shock(m=30):
            self.play(anim)
            self.wait(0.5)


class NegativeDemandShock(Scene):
    """M decreases → AD left → SRAS slowly adjusts down."""
    def construct(self):
        diagram = ADASDiagram(m=20, v=1, sras_price=4, lras_y=5)
        self.play(Create(diagram))
        self.wait()

        label = Text("Negative demand shock: M ↓", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.negative_demand_shock(m=12):
            self.play(anim)
            self.wait(0.5)


class AdverseSupplyShock(Scene):
    """Oil price spike → SRAS up → slowly self-corrects back."""
    def construct(self):
        diagram = ADASDiagram(m=20, v=1, sras_price=4, lras_y=5,
                              numbered_eq=True)
        self.play(Create(diagram))
        self.wait()

        label = Text("Adverse supply shock: costs ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.adverse_supply_shock(sras_price=6, show_arrows=True):
            self.play(anim)
            self.wait(0.5)


class PositiveSupplyShock(Scene):
    """Tech improvement → SRAS down → slowly self-corrects back."""
    def construct(self):
        diagram = ADASDiagram(m=20, v=1, sras_price=4, lras_y=5)
        self.play(Create(diagram))
        self.wait()

        label = Text("Positive supply shock: costs ↓", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.positive_supply_shock(sras_price=2):
            self.play(anim)
            self.wait(0.5)
