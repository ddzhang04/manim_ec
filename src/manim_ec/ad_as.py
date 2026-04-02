from manim import BLUE, GREEN, RED, AnimationGroup, Line, Transform, UP

from .base import EconDiagram

# Default long-run adjustment duration (seconds)
_LR_RUN_TIME = 3


class ADASDiagram(EconDiagram):
    """Aggregate Demand — Aggregate Supply diagram.

    AD is derived from the quantity theory of money: MV = PY, so P = MV/Y.
    SRAS is a horizontal line at a given price level (Keynesian short run).
    LRAS is a vertical line at potential output.

    Parameters:
        m: Money supply (default 20)
        v: Velocity of money (default 1)
        sras_price: Short-run price level (default 4)
        lras_y: Potential output / natural rate of output (default 5)
    """

    def __init__(
        self,
        m=20,
        v=1,
        sras_price=4,
        lras_y=5,
        show_equilibrium=True,
        **kwargs,
    ):
        super().__init__(x_label="Y", y_label="P", **kwargs)

        self._m = m
        self._v = v
        self._sras_price = sras_price

        ad_func = self._make_ad_func(m, v)
        sras_func = self._make_sras_func(sras_price)

        self.ad = self.add_curve(
            "ad", ad_func, x_range=[0.5, 10], color=BLUE, label_text="AD"
        )
        self.sras = self.add_curve(
            "sras", sras_func, x_range=[0, 10], color=RED, label_text="SRAS"
        )
        self.lras = self.add_vertical_line(
            "lras", lras_y, color=GREEN, label_text="LRAS"
        )
        self._lras_y = lras_y

        if show_equilibrium:
            self.mark_equilibrium("ad", "sras", label_x="Y*", label_y="P*")

    @staticmethod
    def _make_ad_func(m, v):
        """P = MV / Y (quantity theory of money)."""
        mv = m * v
        return lambda y: mv / y

    @staticmethod
    def _make_sras_func(price):
        """Flat SRAS at a given price level."""
        return lambda y: price

    @property
    def _lr_price(self):
        """Long-run equilibrium price: P = MV / Y_potential."""
        return (self._m * self._v) / self._lras_y

    def shift_ad(self, m=None, v=None, run_time=1):
        """Animate AD shifting due to changes in M and/or V."""
        self._m = m if m is not None else self._m
        self._v = v if v is not None else self._v
        new_func = self._make_ad_func(self._m, self._v)
        return self.get_shift_animation(
            "ad", new_func, new_x_range=[0.5, 10], run_time=run_time
        )

    def shift_sras(self, sras_price, run_time=1):
        """Animate SRAS shifting to a new price level."""
        self._sras_price = sras_price
        new_func = self._make_sras_func(sras_price)
        return self.get_shift_animation("sras", new_func, run_time=run_time)

    def shift_lras(self, new_y, run_time=1):
        """Animate LRAS moving to a new potential output."""
        old_line = self.curves["lras"]
        y_min = self.axes.y_range[0]
        y_max = self.axes.y_range[1]
        new_line = Line(
            self.axes.c2p(new_y, y_min),
            self.axes.c2p(new_y, y_max),
            color=old_line.get_color(),
        )
        self.curves["lras"] = new_line
        self._lras_y = new_y

        anims = [Transform(old_line, new_line, run_time=run_time)]

        if "lras" in self._curve_labels:
            old_label = self._curve_labels["lras"]
            new_label = old_label.copy().next_to(new_line, UP, buff=0.15)
            anims.append(Transform(old_label, new_label, run_time=run_time))

        return AnimationGroup(*anims)

    def long_run_adjust(self, run_time=_LR_RUN_TIME):
        """SRAS slowly shifts to restore long-run equilibrium.

        After a shock moves output away from LRAS, SRAS gradually adjusts
        to P = MV / Y_potential, bringing the economy back to potential output.
        The animation is slow by default (3s) to show the gradual adjustment.
        """
        return self.shift_sras(self._lr_price, run_time=run_time)

    # ---- Demand shocks ----

    def positive_demand_shock(self, m=None, v=None, long_run=True,
                              lr_run_time=_LR_RUN_TIME):
        """Positive demand shock (e.g. increase in M or V).

        Short run: AD shifts right → output rises above potential, price unchanged.
        Long run: SRAS slowly shifts up → output returns to potential at higher price.

        Returns a list of animations to play in sequence.
        """
        anims = [self.shift_ad(m=m, v=v)]
        if long_run:
            anims.append(self.long_run_adjust(run_time=lr_run_time))
        return anims

    def negative_demand_shock(self, m=None, v=None, long_run=True,
                              lr_run_time=_LR_RUN_TIME):
        """Negative demand shock (e.g. decrease in M or V).

        Short run: AD shifts left → output falls below potential, price unchanged.
        Long run: SRAS slowly shifts down → output returns to potential at lower price.

        Returns a list of animations to play in sequence.
        """
        anims = [self.shift_ad(m=m, v=v)]
        if long_run:
            anims.append(self.long_run_adjust(run_time=lr_run_time))
        return anims

    # ---- Supply shocks ----

    def adverse_supply_shock(self, sras_price, long_run=True,
                             lr_run_time=_LR_RUN_TIME):
        """Adverse supply shock (e.g. oil price spike, cost push).

        Short run: SRAS shifts up → price rises, output falls (stagflation).
        Long run: SRAS slowly shifts back down as economy self-corrects.

        Returns a list of animations to play in sequence.
        """
        anims = [self.shift_sras(sras_price)]
        if long_run:
            anims.append(self.long_run_adjust(run_time=lr_run_time))
        return anims

    def positive_supply_shock(self, sras_price, long_run=True,
                              lr_run_time=_LR_RUN_TIME):
        """Positive supply shock (e.g. technology improvement, cheaper inputs).

        Short run: SRAS shifts down → price falls, output rises.
        Long run: SRAS slowly shifts back up as economy self-corrects.

        Returns a list of animations to play in sequence.
        """
        anims = [self.shift_sras(sras_price)]
        if long_run:
            anims.append(self.long_run_adjust(run_time=lr_run_time))
        return anims
