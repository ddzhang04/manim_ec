from manim import Create, FadeOut, Scene, Text, Write, UP
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


class SharesAlongCurve(Scene):
    """Slide the c/i braces along the curve to show how shares change with k."""
    def construct(self):
        diagram = SolowDiagram(numbered_eq=True)
        self.play(Create(diagram))
        self.wait()

        label = Text("c and i shares at different k",
                      font_size=28).to_edge(UP)
        self.play(Write(label))

        # Show shares at a low k, then slide to high k
        self.play(diagram.show_shares(k=1))
        self.wait(0.5)

        self.play(diagram.animate_shares_along(k_start=1, k_end=8, run_time=4))
        self.wait()

        # Slide back to steady state
        k_star = diagram._steady_state_k()
        self.play(diagram.animate_shares_along(k_start=8, k_end=k_star, run_time=2))
        self.wait()


class SharesWithShifts(Scene):
    """Show c/i shares updating as s, n, g, δ change."""
    def construct(self):
        diagram = SolowDiagram(numbered_eq=True)
        self.play(Create(diagram))
        self.wait()

        # Show shares at steady state
        self.play(diagram.show_shares())
        self.wait()

        # Increase savings rate — more i, less c
        label = Text("s ↑ : more investment, less consumption",
                      font_size=24).to_edge(UP)
        self.play(Write(label))
        self.play(diagram.shift_savings(s=0.5, show_arrows=True))
        self.wait()
        self.play(FadeOut(label))

        # Increase population growth — breakeven steepens
        label2 = Text("n ↑ : breakeven steeper, lower k*",
                       font_size=24).to_edge(UP)
        self.play(Write(label2))
        self.play(diagram.shift_breakeven(n=0.12, show_arrows=True))
        self.wait()
        self.play(FadeOut(label2))

        # Increase depreciation
        label3 = Text("δ ↑ : more depreciation, lower k*",
                       font_size=24).to_edge(UP)
        self.play(Write(label3))
        self.play(diagram.shift_breakeven(delta=0.2, show_arrows=True))
        self.wait()
        self.play(FadeOut(label3))

        # Decrease savings back
        label4 = Text("s ↓ : less saving, even lower k*",
                       font_size=24).to_edge(UP)
        self.play(Write(label4))
        self.play(diagram.shift_savings(s=0.2, show_arrows=True))
        self.wait()


class GoldenRule(Scene):
    """Show the golden-rule capital level that maximizes consumption."""
    def construct(self):
        diagram = SolowDiagram()
        self.play(Create(diagram))
        self.wait()

        label = Text("Golden rule: max consumption", font_size=28).to_edge(UP)
        self.play(Write(label))

        self.play(diagram.show_golden_rule())
        self.wait()

        k_gold = diagram._golden_rule_k()
        self.play(diagram.show_shares(k=k_gold))
        self.wait(2)
