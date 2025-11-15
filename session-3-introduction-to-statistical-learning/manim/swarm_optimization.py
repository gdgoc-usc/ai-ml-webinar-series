from manim import *
import numpy as np


class SwarmOptimizationScene(Scene):
    def construct(self):
        # 0. Title and Environment Setup
        title = Text("Swarm Optimization (PSO)", font_size=36).to_edge(UP)
        self.play(Write(title), run_time=0.33)

        # Create a "search space" (a simple plane)
        axes = NumberPlane(
            x_range=(-8, 8, 1),
            y_range=(-5, 5, 1),
            x_length=12,
            y_length=7,
            axis_config={"include_tip": False, "color": GREY_B},
        ).add_coordinates()

        # Define the "Global Optimum" - the target
        optimum_pos = axes.c2p(5, 2)
        optimum = Star(color=GREEN, fill_opacity=1).scale(0.4).move_to(optimum_pos)
        optimum_label = Text("Optimum", font_size=20).next_to(optimum, DOWN)

        self.play(Create(axes), FadeIn(optimum), Write(optimum_label), run_time=0.33)
        self.wait(1)

        # --------------------------------------------------
        # Phase 1: Initialize Swarm (Particles)
        # --------------------------------------------------
        subtitle = Text("Iteration 1: Particles Explore", font_size=28).next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Create 5 particles (agents) at random spots
        particles = VGroup(*[
            Dot(color=WHITE, radius=0.1).move_to(axes.c2p(np.random.uniform(-7, 0), np.random.uniform(-4, 4)))
            for _ in range(5)
        ])
        self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in particles], lag_ratio=0.1))

        # --------------------------------------------------
        # Phase 2: Update Velocities
        # --------------------------------------------------
        new_subtitle = Text("Particles update based on 'best' positions", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle))

        # 1. Show "Personal Best" (pbest)
        # We'll create "ghosts" of their best positions
        pbest_markers = VGroup(*[
            Dot(color=BLUE, radius=0.05, fill_opacity=0.5).move_to(p.get_center() + RIGHT * 0.5)
            for p in particles
        ])
        pbest_arrows = VGroup(*[
            Arrow(p.get_center(), pb.get_center(), buff=0.1, max_tip_length_to_length_ratio=0.1)
            for p, pb in zip(particles, pbest_markers)
        ])
        pbest_label = Text("Personal Best", color=BLUE, font_size=20).to_edge(RIGHT, buff=1.0).shift(UP * 1)

        self.play(Write(pbest_label), Create(pbest_markers), Create(pbest_arrows))
        self.wait(1)

        # 2. Show "Global Best" (gbest)
        # The gbest is the pbest closest to the optimum (we'll just pick one)
        gbest_marker = Star(color=YELLOW, fill_opacity=0.7).scale(0.3).move_to(pbest_markers[2].get_center())
        gbest_arrows = VGroup(*[
            Arrow(p.get_center(), gbest_marker.get_center(), buff=0.1, color=YELLOW, max_tip_length_to_length_ratio=0.1)
            for p in particles
        ])
        gbest_label = Text("Global Best", color=YELLOW, font_size=20).next_to(pbest_label, DOWN)

        self.play(Write(gbest_label), FadeIn(gbest_marker, scale=1.5), Create(gbest_arrows))
        self.wait(1.5)

        # --------------------------------------------------
        # Phase 3: Move Particles & Converge
        # --------------------------------------------------
        new_subtitle = Text("Iteration 2: Particles Converge", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle),
                  FadeOut(pbest_markers, pbest_arrows, gbest_arrows, pbest_label, gbest_label))

        # Particles move towards a mix of pbest and gbest (and their own momentum)
        # We'll just animate them all moving towards the global optimum
        self.play(
            particles.animate.move_to(optimum_pos).shift(LEFT * 1.5),
            FadeOut(gbest_marker)  # GBest is now the optimum
        )
        self.wait(1)

        # Final convergence
        new_subtitle = Text("Iteration 3: Convergence", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle))

        self.play(particles.animate.move_to(optimum_pos))
        self.play(Indicate(particles, color=GREEN), Indicate(optimum, color=GREEN))
        self.wait(3)