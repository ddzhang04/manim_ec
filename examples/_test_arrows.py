from manim import Create, Scene
from manim_ec import ADASDiagram


class ShortRunOnly(Scene):
    def construct(self):
        d = ADASDiagram(m=20, v=1, sras_price=4, lras_y=5)
        self.play(Create(d))
        self.wait()

        old = d._get_eq_coords()
        print(f"OLD eq: x={old[0]:.2f}, y={old[1]:.2f}")

        anim = d.shift_sras(6, show_arrows=True)

        new = d._get_eq_coords()
        print(f"NEW eq: x={new[0]:.2f}, y={new[1]:.2f}")

        arrows = d._axis_arrows
        print(f"Arrow count: {len(arrows)}")
        for i, a in enumerate(arrows):
            print(f"  Arrow {i}: {type(a).__name__}, tips={len(a.get_tips())}, "
                  f"start={a.get_start()}, end={a.get_end()}")

        self.play(anim)
        self.wait(2)
