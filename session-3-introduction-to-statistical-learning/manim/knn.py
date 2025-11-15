from manim import *
import numpy as np  # Make sure numpy is imported


class KNNScene(Scene):
    def construct(self):
        # 0. Title
        title = Text("K-Nearest Neighbors (KNN)", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 1. Setup - Create two clusters of classified data

        # --- ADJUSTED PARAMETERS for TIGHTER CLUSTERS ---
        cluster_A = VGroup(*[Dot(color=BLUE_D) for _ in range(15)])
        cluster_A.arrange_in_grid(rows=4, cols=4, buff=0.15).scale(0.6)  # Tighter buff and scale
        cluster_A.shift(LEFT * 2 + DOWN * 0.5)  # Moved further left

        # Add less randomness
        for dot in cluster_A:
            dot.shift(np.random.rand(3) * 0.3)

        cluster_B = VGroup(*[Dot(color=RED_D) for _ in range(15)])
        cluster_B.arrange_in_grid(rows=4, cols=4, buff=0.15).scale(0.6)  # Tighter buff and scale
        cluster_B.shift(RIGHT * 2 + UP * 0.5)  # Moved further right

        # Add less randomness
        for dot in cluster_B:
            dot.shift(np.random.rand(3) * 0.3)
        # --- END OF ADJUSTMENTS ---

        class_A_label = Text("Class A", color=BLUE_D, font_size=24).next_to(cluster_A, DOWN, buff=0.5)
        class_B_label = Text("Class B", color=RED_D, font_size=24).next_to(cluster_B, UP, buff=0.5)

        self.play(FadeIn(cluster_A), FadeIn(cluster_B),
                  Write(class_A_label), Write(class_B_label))
        self.wait(1)

        # --------------------------------------------------
        # Phase 1: New Point Arrives
        # --------------------------------------------------
        subtitle = Text("A new point appears...", font_size=28).next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # This is our new, unclassified query point
        # --- ADJUSTED: Star is much smaller ---
        query_point = Star(color=WHITE).scale(0.4).move_to(RIGHT * 0.3 + DOWN * 0.5)

        self.play(FadeIn(query_point, scale=1.5))
        self.wait(1)

        # --------------------------------------------------
        # Phase 2: Find K-Nearest Neighbors (K=5)
        # --------------------------------------------------
        new_subtitle = Text("Find K=5 Nearest Neighbors", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle))

        # --- ADJUSTED: Smaller circle radius ---
        k_circle = Circle(radius=1.8, color=YELLOW).move_to(query_point.get_center())
        self.play(Create(k_circle))

        # --- ADJUSTED: Picked neighbors that are now on the inner edges ---
        # (Points 3, 7, 11 are on the right edge of the 4x4 grid)
        neighbors_A = VGroup(cluster_A[3], cluster_A[7], cluster_A[11])
        # (Points 0, 4 are on the left edge of the 4x4 grid)
        neighbors_B = VGroup(cluster_B[0], cluster_B[4])
        all_neighbors = VGroup(neighbors_A, neighbors_B)

        self.play(
            neighbors_A.animate.set_color(BLUE_A),
            neighbors_B.animate.set_color(RED_A),
            LaggedStart(*[Indicate(d, color=YELLOW) for d in all_neighbors], lag_ratio=0.1)
        )
        self.wait(1)

        # --------------------------------------------------
        # Phase 3: Neighbors "Vote"
        # --------------------------------------------------
        # --- ADJUSTED: Text reflects new 3/2 split ---
        new_subtitle = Text("Neighbors 'Vote' (3 Blue, 2 Red)", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle))

        # Show the votes "firing" at the query point
        self.play(Indicate(query_point, color=BLUE_A), run_time=0.3)
        self.play(Indicate(query_point, color=RED_A), run_time=0.3)
        self.play(Indicate(query_point, color=BLUE_A), run_time=0.3)
        self.play(Indicate(query_point, color=RED_A), run_time=0.3)
        self.play(Indicate(query_point, color=BLUE_A), run_time=0.3)
        self.wait(1)

        # --------------------------------------------------
        # Phase 4: Final Classification
        # --------------------------------------------------
        new_subtitle = Text("Final Class: BLUE (Majority Wins!)", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle))

        # The query point takes on the color of the majority class
        self.play(
            query_point.animate.set_color(BLUE_D),
            FadeOut(k_circle)
        )
        self.wait(3)