from manim import Create, Scene, Text, Write, UP
from manim_ec import ISLMDiagram


class MonetaryExpansion(Scene):
    """Money supply increase → LM shifts right → lower r, higher Y."""
    def construct(self):
        diagram = ISLMDiagram(numbered_eq=True)
        self.play(Create(diagram))
        self.wait()

        label = Text("Monetary expansion: Ms ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.monetary_expansion(ms=5, show_arrows=True):
            self.play(anim)
            self.wait(0.5)


class FiscalExpansion(Scene):
    """Government spending increase → IS shifts right → higher r, higher Y."""
    def construct(self):
        diagram = ISLMDiagram(numbered_eq=True)
        self.play(Create(diagram))
        self.wait()

        label = Text("Fiscal expansion: G ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in diagram.fiscal_expansion(a=13, show_arrows=True):
            self.play(anim)
            self.wait(0.5)
