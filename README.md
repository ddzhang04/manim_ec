# manim-ec

Animated economics diagrams built on [Manim Community](https://www.manim.community/).

## Installation

```bash
pip install manim-ec
```

Requires Python 3.11+ and a working Manim installation (see [Manim docs](https://docs.manim.community/en/stable/installation.html)).

For development:

```bash
git clone https://github.com/ddzhang04/manim_ec.git
cd manim_ec
uv sync
```

## Quick start

```python
from manim import Create, Scene
from manim_ec import ADASDiagram

class MyScene(Scene):
    def construct(self):
        diagram = ADASDiagram()
        self.play(Create(diagram))
        self.wait()

        for anim in diagram.positive_demand_shock(m=30, show_arrows=True):
            self.play(anim)
            self.wait(0.5)
```

```bash
manim render -ql my_scene.py MyScene
```

---

## Diagrams

### SupplyDemandDiagram

Basic supply and demand with equilibrium.

```python
SupplyDemandDiagram(
    demand_func=lambda q: 8 - 0.5 * q,   # inverse demand P(Q)
    supply_func=lambda q: 2 + 0.5 * q,   # inverse supply P(Q)
    show_equilibrium=True,
)
```

Shift curves with `get_shift_animation()`:

```python
diagram.get_shift_animation("demand", new_func, show_arrows=True)
diagram.get_shift_animation("supply", new_func, show_arrows=True)
```

---

### ADASDiagram

AD-AS model with demand/supply shocks and long-run adjustment.

AD is derived from the quantity theory: `P = MV/Y`.

SRAS is flat by default (Keynesian). Pass `sras_slope` for the upward-sloping
Mankiw formulation: `P = Pe + slope * (Y - Y_bar)`.

```python
ADASDiagram(
    m=20,              # money supply
    v=1,               # velocity
    sras_price=4,      # expected price level Pe
    sras_slope=None,   # None = flat, positive = upward-sloping
    lras_y=5,          # potential output Y_bar
    sras_only=False,   # hide LRAS
    lras_only=False,   # hide SRAS
)
```

#### Shifting curves

```python
diagram.shift_ad(m=30, show_arrows=True)
diagram.shift_sras(sras_price=6)
diagram.shift_lras(new_y=7)
```

#### Shock methods

These return a list of animations to play in sequence. They shift AD or SRAS
and optionally animate long-run adjustment back to potential output.

```python
diagram.positive_demand_shock(m=30, long_run=True, show_arrows=True)
diagram.negative_demand_shock(m=12)
diagram.adverse_supply_shock(sras_price=6)
diagram.positive_supply_shock(sras_price=2)
```

#### Upward-sloping SRAS

```python
diagram = ADASDiagram(sras_slope=0.5)

# Shifts change Pe (expected price), curve slides up/down keeping same slope
for anim in diagram.positive_demand_shock(m=30, show_arrows=True):
    self.play(anim)
```

---

### ISLMDiagram

IS-LM model with fiscal and monetary policy shifts.

```python
ISLMDiagram(
    a=9.5,   # autonomous spending
    b=1.5,   # investment sensitivity to interest rate
    ms=2,    # real money supply
    k=1,     # income sensitivity of money demand
    h=1,     # interest sensitivity of money demand
)
```

#### Shifting curves

```python
diagram.shift_is(a=13, show_arrows=True)
diagram.shift_lm(ms=5, show_arrows=True)
```

#### Policy methods

```python
diagram.monetary_expansion(ms=5, show_arrows=True)
diagram.monetary_contraction(ms=1)
diagram.fiscal_expansion(a=13)
diagram.fiscal_contraction(a=6)
```

---

### SolowDiagram

Solow growth model: `y = k^a`, savings `sf(k)`, break-even `(d+n+g)k`.

```python
SolowDiagram(
    s=0.3,       # savings rate
    alpha=0.5,   # capital share
    delta=0.1,   # depreciation
    n=0.05,      # population growth
    g=0.05,      # technology growth
    show_production=True,
)
```

#### Shifting curves

```python
diagram.shift_savings(s=0.5, show_arrows=True)
diagram.shift_breakeven(delta=0.15, n=0.08)
```

#### Shock methods

```python
diagram.increase_savings(s=0.5, show_arrows=True)
diagram.decrease_savings(s=0.15)
diagram.population_growth(n=0.1)
diagram.increase_depreciation(delta=0.2)
```

#### Consumption and investment shares

Show braces annotating c and i at a given capital level:

```python
diagram.show_shares()            # at steady state k*
diagram.show_shares(k=3)         # at a specific k
diagram.hide_shares()
```

Slide the braces along the curve to visualize how shares change:

```python
diagram.animate_shares_along(k_start=1, k_end=8, run_time=4)
```

Shares update automatically when you shift curves while they are visible.

#### Golden rule

```python
diagram.show_golden_rule()       # mark k where consumption is maximized
diagram.hide_golden_rule()
```

---

### LinkedISLM_ADAS

Side-by-side IS-LM and AD-AS that shift simultaneously.

```python
LinkedISLM_ADAS(
    numbered_eq=True,
    show_arrows=True,
    spacing=1.0,
)
```

#### Policy methods

```python
linked.monetary_expansion(ms=5, m=30)
linked.monetary_contraction(ms=1, m=10)
linked.fiscal_expansion(a=13, m=30)
linked.fiscal_contraction(a=6, m=12)
linked.adverse_supply_shock(sras_price=6)
```

---

## Common options

These options work across all diagram classes.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `show_equilibrium` | `True` | Mark initial equilibrium with dot and dashed lines |
| `numbered_eq` | `False` | Subscripted labels (P1, Y1 -> P2, Y2) that persist across shifts |
| `show_arrows` | `False` | Arrows on axes showing direction of equilibrium change |
| `x_range` / `y_range` | `[0, 10, 1]` | Axis range as `[min, max, step]` |
| `x_length` / `y_length` | `6` / `4` | Axis display size in Manim units |

## Examples

Ready-to-run scenes are in [`examples/`](examples/):

```bash
manim render -ql examples/ad_as_example.py SlopedSRAS
manim render -ql examples/solow_example.py SharesAlongCurve
manim render -ql examples/is_lm_example.py MonetaryExpansion
manim render -ql examples/linked_example.py LinkedMonetaryExpansion
```

## License

MIT
