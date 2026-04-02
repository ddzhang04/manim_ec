from manim import Create, Scene, Text, Write, UP
from manim_ec import LinkedISLM_ADAS


class LinkedMonetaryExpansion(Scene):
    """Monetary expansion shown simultaneously in IS-LM and AD-AS."""
    def construct(self):
        linked = LinkedISLM_ADAS(numbered_eq=True, show_arrows=True)
        self.play(Create(linked))
        self.wait()

        label = Text("Monetary expansion: Ms ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in linked.monetary_expansion(ms=5, m=30):
            self.play(anim)
            self.wait(0.5)


class LinkedFiscalExpansion(Scene):
    """Fiscal expansion shown simultaneously in IS-LM and AD-AS."""
    def construct(self):
        linked = LinkedISLM_ADAS(numbered_eq=True, show_arrows=True)
        self.play(Create(linked))
        self.wait()

        label = Text("Fiscal expansion: G ↑", font_size=28).to_edge(UP)
        self.play(Write(label))

        for anim in linked.fiscal_expansion(a=13, m=30):
            self.play(anim)
            self.wait(0.5)
