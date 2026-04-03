from manim import BLUE, GREEN, RED

from .base import EconDiagram


class SolowDiagram(EconDiagram):
    """Solow growth model diagram.

    Production function: y = k^α
    Savings/investment: sf(k) = s·k^α
    Break-even investment: (δ + n + g)·k

    Steady state where sf(k*) = (δ + n + g)·k*.

    Parameters:
        s: Savings rate (default 0.3)
        alpha: Capital share / production function exponent (default 0.5)
        delta: Depreciation rate (default 0.05)
        n: Population growth rate (default 0.02)
        g: Technological growth rate (default 0.03)
    """

    def __init__(
        self,
        s=0.3,
        alpha=0.5,
        delta=0.1,
        n=0.05,
        g=0.05,
        show_equilibrium=True,
        numbered_eq=False,
        show_production=True,
        **kwargs,
    ):
        kwargs.setdefault("x_range", [0, 10, 1])
        kwargs.setdefault("y_range", [0, 4, 1])
        super().__init__(x_label="k", y_label="y", **kwargs)

        self._s = s
        self._alpha = alpha
        self._delta = delta
        self._n = n
        self._g = g

        if show_production:
            prod_func = self._make_prod_func(alpha)
            self.production = self.add_curve(
                "production", prod_func, x_range=[0.01, 10],
                color=GREEN, label_text="f(k)",
            )

        savings_func = self._make_savings_func(s, alpha)
        breakeven_func = self._make_breakeven_func(delta, n, g)

        self.savings = self.add_curve(
            "savings", savings_func, x_range=[0.01, 10],
            color=BLUE, label_text="sf(k)",
        )
        self.breakeven = self.add_curve(
            "breakeven", breakeven_func, x_range=[0, 10],
            color=RED, label_text="(δ+n+g)k",
        )

        if show_equilibrium:
            self.mark_equilibrium("savings", "breakeven",
                                  label_x="k", label_y="y",
                                  numbered=numbered_eq)

    @staticmethod
    def _make_prod_func(alpha):
        """y = k^α"""
        return lambda k: k ** alpha

    @staticmethod
    def _make_savings_func(s, alpha):
        """sf(k) = s·k^α"""
        return lambda k: s * (k ** alpha)

    @staticmethod
    def _make_breakeven_func(delta, n, g):
        """(δ + n + g)·k"""
        rate = delta + n + g
        return lambda k: rate * k

    def shift_savings(self, s=None, run_time=1, show_arrows=False):
        """Animate savings curve shifting due to change in savings rate."""
        self._s = s if s is not None else self._s
        new_func = self._make_savings_func(self._s, self._alpha)
        return self.get_shift_animation(
            "savings", new_func, run_time=run_time, show_arrows=show_arrows,
        )

    def shift_breakeven(self, delta=None, n=None, g=None, run_time=1,
                        show_arrows=False):
        """Animate break-even line shifting due to changes in δ, n, or g."""
        self._delta = delta if delta is not None else self._delta
        self._n = n if n is not None else self._n
        self._g = g if g is not None else self._g
        new_func = self._make_breakeven_func(self._delta, self._n, self._g)
        return self.get_shift_animation(
            "breakeven", new_func, run_time=run_time, show_arrows=show_arrows,
        )

    # ---- Common shocks ----

    def increase_savings(self, s, show_arrows=False):
        """Higher savings rate → sf(k) shifts up → higher steady-state k."""
        return [self.shift_savings(s=s, show_arrows=show_arrows)]

    def decrease_savings(self, s, show_arrows=False):
        """Lower savings rate → sf(k) shifts down → lower steady-state k."""
        return [self.shift_savings(s=s, show_arrows=show_arrows)]

    def population_growth(self, n, show_arrows=False):
        """Higher population growth → break-even steeper → lower steady-state k."""
        return [self.shift_breakeven(n=n, show_arrows=show_arrows)]

    def increase_depreciation(self, delta, show_arrows=False):
        """Higher depreciation → break-even steeper → lower steady-state k."""
        return [self.shift_breakeven(delta=delta, show_arrows=show_arrows)]
