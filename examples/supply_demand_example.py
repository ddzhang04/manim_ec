from manim import Create, Scene
from manim_ec import SupplyDemandDiagram

class BasicSupplyDemand(Scene):
    def construct(self):
        diagram = SupplyDemandDiagram()
        self.play(Create(diagram))
        self.wait()
