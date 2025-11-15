from manim import *


class LinearRegressionScene(Scene):
    def construct(self):
        # 0. Title
        #title = Text("Linear Regression", font_size=36).to_edge(UP)
        #self.play(Write(title))

        # 1. Setup - Create Axes and Data
        # We create a number plane
        axes = NumberPlane(
            x_range=(-1, 10, 1),
            y_range=(-1, 10, 1),
            x_length=7,
            y_length=7,
            axis_config={"include_tip": False, "color": GRAY},
        ).add_coordinates()
        axes.to_edge(LEFT, buff=1.5)

        # Our hard-coded data points
        data_points = [
            (1, 2), (2, 3), (3, 3.5), (4, 5.5),
            (5, 5), (6, 7), (7, 6.5), (8, 8)
        ]

        # Create Dot mobjects for each point
        dots = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in data_points])
        data_label = Text("Original Data", font_size=24).next_to(dots, UP, buff=0.5)

        self.play(Create(axes), FadeIn(dots), Write(data_label))
        self.wait(1)

        # --------------------------------------------------
        # Phase 1: Training ("Finding the Line")
        # --------------------------------------------------
        train_title = Text("Find the 'Best-Fit' Line", font_size=28).to_edge(RIGHT, buff=1.5).align_to(UP)
        #train_subtitle = Text("Find the 'Best-Fit' Line", font_size=20).next_to(train_title, DOWN, buff=0.2)
        self.play(Write(train_title))

        # Show a "bad" line first
        # --- CORRECTED LINE ---
        bad_line = axes.plot(lambda x: 0.5 * x + 1, x_range=[0, 9], color=RED_E)
        self.play(Create(bad_line))
        self.wait(1)

        # This is our "correct" best-fit line
        # --- CORRECTED LINE ---
        best_fit_line = axes.plot(lambda x: 0.85 * x + 1, x_range=[0, 9], color=GREEN)

        # "Train" by transforming the bad line into the good one
        self.play(Transform(bad_line, best_fit_line))
        self.wait(1)

        # --------------------------------------------------
        # Phase 2: Inference ("Making a Prediction")
        # --------------------------------------------------
        infer_title = Text("Predict Y for a new X", font_size=28).move_to(train_title)
        #infer_subtitle = Text("Predict Y for a new X", font_size=20).next_to(infer_title, DOWN, buff=0.2)
        self.play(Transform(train_title, infer_title))

        # Create a new X query
        new_x = 4.5
        new_x_dot = Dot(axes.c2p(new_x, 0), color=YELLOW)
        new_x_label = Text("New X", font_size=20).next_to(new_x_dot, DOWN)
        self.play(FadeIn(new_x_dot), Write(new_x_label))

        # Project from X up to the line
        predicted_y = 0.85 * new_x + 1
        vert_line = DashedLine(
            axes.c2p(new_x, 0),
            axes.c2p(new_x, predicted_y),
            color=YELLOW
        )
        self.play(Create(vert_line))

        # Project from the line over to the Y axis
        horiz_line = DashedLine(
            axes.c2p(new_x, predicted_y),
            axes.c2p(0, predicted_y),
            color=YELLOW
        )
        self.play(Create(horiz_line))

        # Show the final predicted dot and value
        pred_dot = Dot(axes.c2p(0, predicted_y), color=RED)
        pred_label = Text(f"Pred Y: {predicted_y:.1f}", font_size=20).next_to(pred_dot, LEFT)

        self.play(FadeIn(pred_dot), Write(pred_label))
        self.wait(3)