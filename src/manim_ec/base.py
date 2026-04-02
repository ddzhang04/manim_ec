import numpy as np
from manim import (
    Axes,
    AnimationGroup,
    DashedLine,
    Dot,
    Text,
    Transform,
    VGroup,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    WHITE,
    YELLOW,
)


def find_intersection(func_a, func_b, x_range):
    """Find the x where func_a(x) == func_b(x) by sampling."""
    xs = np.linspace(x_range[0] + 0.01, x_range[1] - 0.01, 1000)
    diffs = np.array([func_a(x) - func_b(x) for x in xs])
    sign_changes = np.where(np.diff(np.sign(diffs)))[0]
    if len(sign_changes) == 0:
        return None
    idx = sign_changes[0]
    # linear interpolation between the two bracketing samples
    x0, x1 = xs[idx], xs[idx + 1]
    d0, d1 = diffs[idx], diffs[idx + 1]
    x_cross = x0 - d0 * (x1 - x0) / (d1 - d0)
    return x_cross


class EconDiagram(VGroup):
    """Base class for economics diagrams built on manim Axes."""

    def __init__(self, x_label="X", y_label="Y",
                 x_range=None, y_range=None,
                 x_length=6, y_length=4, **kwargs):
        super().__init__(**kwargs)

        x_range = x_range or [0, 10, 1]
        y_range = y_range or [0, 10, 1]

        self.axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config={"include_numbers": False},
        )

        self.axis_labels = VGroup(
            Text(x_label, font_size=24).next_to(self.axes.x_axis, RIGHT),
            Text(y_label, font_size=24).next_to(self.axes.y_axis, UP),
        )

        self.curves = {}
        self._curve_funcs = {}
        self._curve_x_ranges = {}
        self._curve_labels = {}
        self._eq_group = VGroup()
        self._eq_curve_names = None
        self._eq_label_x = ""
        self._eq_label_y = ""

        self.add(self.axes, self.axis_labels)

    def add_curve(self, name, func, x_range, color, label_text=None):
        """Plot a curve on the axes and store it by name."""
        curve = self.axes.plot(func, x_range=x_range, color=color)
        self.curves[name] = curve
        self._curve_funcs[name] = func
        self._curve_x_ranges[name] = x_range
        self.add(curve)

        if label_text:
            label = Text(label_text, font_size=20, color=color)
            label.next_to(curve.get_end(), RIGHT, buff=0.15)
            self._curve_labels[name] = label
            self.add(label)

        return curve

    def add_vertical_line(self, name, x, color, label_text=None):
        """Add a vertical line at a given x position."""
        y_min = self.axes.y_range[0]
        y_max = self.axes.y_range[1]
        start = self.axes.c2p(x, y_min)
        end = self.axes.c2p(x, y_max)
        from manim import Line
        line = Line(start, end, color=color)
        self.curves[name] = line
        self.add(line)

        if label_text:
            label = Text(label_text, font_size=20, color=color)
            label.next_to(line, UP, buff=0.15)
            self._curve_labels[name] = label
            self.add(label)

        return line

    def _build_eq_group(self, curve_a, curve_b, label_x="", label_y=""):
        """Build equilibrium mobjects for the intersection of two curves."""
        func_a = self._curve_funcs[curve_a]
        func_b = self._curve_funcs[curve_b]
        x_range = self.axes.x_range

        x_eq = find_intersection(func_a, func_b, x_range)
        if x_eq is None:
            return None

        y_eq = func_a(x_eq)
        point = self.axes.c2p(x_eq, y_eq)

        dot = Dot(point, color=YELLOW, radius=0.06)

        h_line = DashedLine(
            self.axes.c2p(0, y_eq), point, color=WHITE, dash_length=0.08
        )
        v_line = DashedLine(
            self.axes.c2p(x_eq, 0), point, color=WHITE, dash_length=0.08
        )

        eq_group = VGroup(dot, h_line, v_line)

        if label_x:
            lx = Text(label_x, font_size=18).next_to(
                self.axes.c2p(x_eq, 0), DOWN, buff=0.15
            )
            eq_group.add(lx)
        if label_y:
            ly = Text(label_y, font_size=18).next_to(
                self.axes.c2p(0, y_eq), LEFT, buff=0.15
            )
            eq_group.add(ly)

        return eq_group

    def mark_equilibrium(self, curve_a, curve_b, label_x="", label_y=""):
        """Mark the intersection of two curves with a dot and dashed lines."""
        self._eq_curve_names = (curve_a, curve_b)
        self._eq_label_x = label_x
        self._eq_label_y = label_y

        eq_group = self._build_eq_group(curve_a, curve_b, label_x, label_y)
        if eq_group is None:
            return None

        self._eq_group = eq_group
        self.add(eq_group)
        return eq_group

    def get_shift_animation(self, curve_name, new_func, new_x_range=None,
                            run_time=1):
        """Return a Transform animation that shifts a curve to a new function."""
        old_curve = self.curves[curve_name]
        x_range = new_x_range or self._curve_x_ranges[curve_name]
        new_curve = self.axes.plot(
            new_func, x_range=x_range, color=old_curve.get_color()
        )

        self._curve_funcs[curve_name] = new_func
        self.curves[curve_name] = new_curve

        anims = [Transform(old_curve, new_curve, run_time=run_time)]

        if curve_name in self._curve_labels:
            old_label = self._curve_labels[curve_name]
            new_label = old_label.copy().next_to(new_curve.get_end(), RIGHT, buff=0.15)
            anims.append(Transform(old_label, new_label, run_time=run_time))

        # Animate equilibrium to the new intersection
        if self._eq_curve_names and curve_name in self._eq_curve_names:
            new_eq = self._build_eq_group(
                *self._eq_curve_names, self._eq_label_x, self._eq_label_y
            )
            if new_eq is not None:
                old_eq = self._eq_group
                anims.append(Transform(old_eq, new_eq, run_time=run_time))

        return AnimationGroup(*anims)
