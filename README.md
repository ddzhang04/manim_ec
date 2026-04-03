# manim-ec

Animated economics diagrams built on [Manim Community](https://www.manim.community/). Create publication-quality animations of core macro and micro models with a few lines of Python.

## Models

| Diagram | Class | Key curves |
|---------|-------|------------|
| Supply & Demand | `SupplyDemandDiagram` | S, D with equilibrium |
| AD-AS | `ADASDiagram` | AD, SRAS, LRAS with demand/supply shocks + long-run adjustment |
| IS-LM | `ISLMDiagram` | IS, LM with monetary & fiscal policy shifts |
| Solow Growth | `SolowDiagram` | f(k), sf(k), (δ+n+g)k with savings & depreciation shocks |
| Linked IS-LM / AD-AS | `LinkedISLM_ADAS` | Side-by-side IS-LM and AD-AS that shift simultaneously |

## Installation

```bash
pip install manim-ec
```

Or for development:

```bash
git clone https://github.com/ddzhang04/manim_ec.git
cd manim_ec
uv sync
```

## Quick start

```python
from manim import Create, Scene, Write, Text, UP
from manim_ec import ADASDiagram

class AdverseSupplyShock(Scene):
    def construct(self):
        diagram = ADASDiagram(numbered_eq=True)
        self.play(Create(diagram))
        self.wait()

        for anim in diagram.adverse_supply_shock(sras_price=6, show_arrows=True):
            self.play(anim)
            self.wait(0.5)
```

```bash
manim render -ql my_scene.py AdverseSupplyShock
```

## Features

**Equilibrium markers** — automatic intersection detection with dashed projection lines and labeled axes.

**Numbered equilibria** — pass `numbered_eq=True` to get subscripted labels (P₁/Y₁ → P₂/Y₂) that persist across shifts so you can see before and after.

**Axis arrows** — pass `show_arrows=True` to any shift method to draw arrows on the axes showing the direction of change.

**Long-run adjustment** — AD-AS demand and supply shocks support `long_run=True` (default) to animate SRAS gradually returning to potential output.

**Linked diagrams** — `LinkedISLM_ADAS` places IS-LM and AD-AS side by side. Policy shifts animate both diagrams simultaneously.

## Examples

All examples are in the `examples/` directory:

```bash
# AD-AS shocks
manim render -ql examples/ad_as_example.py AdverseSupplyShock

# IS-LM monetary expansion
manim render -ql examples/is_lm_example.py MonetaryExpansion

# Solow savings increase
manim render -ql examples/solow_example.py IncreaseSavings

# Linked IS-LM + AD-AS
manim render -ql examples/linked_example.py LinkedMonetaryExpansion
```

## API reference

### Common options (all diagrams)

| Parameter | Description |
|-----------|-------------|
| `show_equilibrium=True` | Mark the initial equilibrium with dot + dashed lines |
| `numbered_eq=False` | Use subscripted labels (P₁, Y₁) instead of P*, Y* |
| `show_arrows=False` | Draw axis arrows showing direction of equilibrium change |
| `x_range`, `y_range` | Override axis ranges (e.g. `[0, 10, 1]`) |
| `x_length`, `y_length` | Override axis display size |

### ADASDiagram

```python
ADASDiagram(m=20, v=1, sras_price=4, lras_y=5,
            sras_only=False, lras_only=False)

# Shift individual curves
diagram.shift_ad(m=30, show_arrows=True)
diagram.shift_sras(sras_price=6)
diagram.shift_lras(new_y=7)

# Convenience shock methods (return list of animations)
diagram.positive_demand_shock(m=30, long_run=True, show_arrows=True)
diagram.negative_demand_shock(m=12)
diagram.adverse_supply_shock(sras_price=6)
diagram.positive_supply_shock(sras_price=2)
```

### ISLMDiagram

```python
ISLMDiagram(a=9.5, b=1.5, ms=2, k=1, h=1)

diagram.shift_is(a=13, show_arrows=True)
diagram.shift_lm(ms=5)

diagram.monetary_expansion(ms=5, show_arrows=True)
diagram.monetary_contraction(ms=1)
diagram.fiscal_expansion(a=13)
diagram.fiscal_contraction(a=6)
```

### SolowDiagram

```python
SolowDiagram(s=0.3, alpha=0.5, delta=0.1, n=0.05, g=0.05,
             show_production=True)

diagram.shift_savings(s=0.5, show_arrows=True)
diagram.shift_breakeven(delta=0.15, n=0.08)

diagram.increase_savings(s=0.5, show_arrows=True)
diagram.decrease_savings(s=0.15)
diagram.population_growth(n=0.1)
diagram.increase_depreciation(delta=0.2)
```

### LinkedISLM_ADAS

```python
LinkedISLM_ADAS(numbered_eq=True, show_arrows=True, spacing=1.0)

linked.monetary_expansion(ms=5, m=30)
linked.monetary_contraction(ms=1, m=10)
linked.fiscal_expansion(a=13, m=30)
linked.fiscal_contraction(a=6, m=12)
linked.adverse_supply_shock(sras_price=6)
```

## License

MIT
