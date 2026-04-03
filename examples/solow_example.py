from manim import Create, Scene, Text, Write, UP
from manim_ec import SolowDiagram


class IncreaseSavings(Scene):
    """Higher savings rate shifts sf(k) up → higher steady-state capital."""
    def construct(self):
        diagram = SolowDiagram(numbered_eq=True)
        self.play(Create(diagram))
        self.wait()

        label = Text("Increase in savings rate: s ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.increase_savings(s=0.5, show_arrows=True):
            self.play(anim)
            self.wait(0.5)


class PopulationGrowth(Scene):
    """Higher population growth steepens break-even → lower steady-state capital."""
    def construct(self):
        diagram = SolowDiagram(numbered_eq=True)
        self.play(Create(diagram))
        self.wait()

        label = Text("Population growth: n ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.population_growth(n=0.1, show_arrows=True):
            self.play(anim)
            self.wait(0.5)
