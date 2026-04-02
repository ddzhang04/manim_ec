from manim import BLUE, RED

from .base import EconDiagram


class ISLMDiagram(EconDiagram):
    """IS-LM model diagram.

    IS curve (goods market equilibrium):
        Y = a - b*r  =>  r = a/b - Y/b

    LM curve (money market equilibrium):
        Ms = k*Y - h*r  =>  r = (k*Y - Ms) / h

    Parameters:
        a: Autonomous spending (default 10)
        b: Interest sensitivity of investment (default 2)
        ms: Real money supply (default 5)
        k: Income sensitivity of money demand (default 0.5)
        h: Interest sensitivity of money demand (default 1)
    """

    def __init__(
        self,
        a=10,
        b=2,
        ms=5,
        k=0.5,
        h=1,
        show_equilibrium=True,
        **kwargs,
    ):
        super().__init__(x_label="Y", y_label="r", **kwargs)

        self._a = a
        self._b = b
        self._ms = ms
        self._k = k
        self._h = h

        is_func = self._make_is_func(a, b)
        lm_func = self._make_lm_func(ms, k, h)

        self.is_curve = self.add_curve(
            "is", is_func, x_range=[0, 10], color=BLUE, label_text="IS"
        )
        self.lm_curve = self.add_curve(
            "lm", lm_func, x_range=[0, 10], color=RED, label_text="LM"
        )

        if show_equilibrium:
            self.mark_equilibrium("is", "lm", label_x="Y*", label_y="r*")

    @staticmethod
    def _make_is_func(a, b):
        """r = a/b - Y/b"""
        return lambda y: a / b - y / b

    @staticmethod
    def _make_lm_func(ms, k, h):
        """r = (k*Y - Ms) / h"""
        return lambda y: (k * y - ms) / h

    def shift_is(self, a=None, b=None):
        """Animate IS shifting due to changes in autonomous spending or interest sensitivity."""
        self._a = a if a is not None else self._a
        self._b = b if b is not None else self._b
        new_func = self._make_is_func(self._a, self._b)
        return self.get_shift_animation("is", new_func)

    def shift_lm(self, ms=None, k=None, h=None):
        """Animate LM shifting due to changes in money supply or money demand parameters."""
        self._ms = ms if ms is not None else self._ms
        self._k = k if k is not None else self._k
        self._h = h if h is not None else self._h
        new_func = self._make_lm_func(self._ms, self._k, self._h)
        return self.get_shift_animation("lm", new_func)
