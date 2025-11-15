from manim import *
import numpy as np


class ClassificationScene(Scene):
    def construct(self):
        self.camera.background_color = "#202020"  # Dark grey background

        # 1. Title
        title = Text("Classification", font_size=48, color=BLUE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Generate Data Points (Two Classes, no axes)
        np.random.seed(0)
        num_points = 25

        # Class A (e.g., Apples - Red)
        # We define their positions relative to a center point
        class_A_center = RIGHT * 2 + DOWN * 0.5
        class_A_points = VGroup()
        for _ in range(num_points):
            offset = np.random.normal(scale=0.8, size=3)  # Random x,y,z offset
            offset[2] = 0  # Ensure it's 2D
            class_A_points.add(Dot(class_A_center + offset, color=RED_E, radius=0.08))

        # Class B (e.g., Oranges - Orange)
        class_B_center = LEFT * 2 + UP * 0.5
        class_B_points = VGroup()
        for _ in range(num_points):
            offset = np.random.normal(scale=0.8, size=3)
            offset[2] = 0
            class_B_points.add(Dot(class_B_center + offset, color=ORANGE, radius=0.08))

        self.play(FadeIn(class_A_points, shift=UP), FadeIn(class_B_points, shift=DOWN))
        self.wait(1)

        # 3. Draw Decision Boundary (Vertical Line)
        decision_boundary_line = Line(
            UP * 3.5,
            DOWN * 3.5,
            color=WHITE,
            stroke_width=4,
            z_index=2
        ).move_to(ORIGIN)

        db_label = Text("Decision Boundary", font_size=24, color=WHITE).next_to(decision_boundary_line, UP + RIGHT,
                                                                                buff=0.1)

        self.play(Create(decision_boundary_line), Write(db_label))
        self.wait(1)

        # 4. Classify a New Point
        new_point_pos = RIGHT * 1.0 + UP * 2.0  # Clearly on the "Red" side
        new_point_mobj = Dot(new_point_pos, color=YELLOW, radius=0.15, z_index=3)
        new_point_label = Text("New Fruit", font_size=20, color=YELLOW).next_to(new_point_mobj, RIGHT, buff=0.1)

        self.play(FadeIn(new_point_mobj, scale=0.5), Write(new_point_label))
        self.wait(1)

        # 5. Illustrate classification by changing color
        self.play(
            new_point_mobj.animate.set_color(RED_E),
            new_point_label.animate.become(
                Text("Classified as Apple", font_size=20, color=RED_E).next_to(new_point_mobj, RIGHT, buff=0.1))
        )
        self.wait(2)


class RegressionScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"  # Dark grey background

        # 1. Title
        title = Text("Regression", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Axes Setup
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=6,
            axis_config={"color": GREY_A},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
        ).shift(DOWN * 0.5)

        # Add labels for the "features" and "target"
        x_label = Text("Size (sq ft)", font_size=20, color=GREY_B).next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Price ($100k)", font_size=20, color=GREY_B).next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI / 2)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # 3. Generate Data Points (House prices based on size)
        np.random.seed(1)
        num_houses = 30

        house_sizes = np.random.uniform(1, 9, num_houses)
        # True relationship: price = 0.7 * size + 1.5 + noise
        house_prices = 0.7 * house_sizes + 1.5 + np.random.normal(0, 0.8, num_houses)

        house_points = VGroup(*[
            Dot(axes.c2p(s, p), color=WHITE, radius=0.06) for s, p in zip(house_sizes, house_prices)
        ])

        self.play(FadeIn(house_points, shift=DOWN))
        self.wait(1)

        # 4. Draw Regression Line (Line of Best Fit)
        regression_line = axes.plot(lambda x: 0.75 * x + 1.0, color=YELLOW, stroke_width=4, z_index=2)
        reg_label = Text("Regression Line", font_size=24, color=YELLOW).next_to(regression_line, UP + LEFT, buff=0.1)

        self.play(Create(regression_line), Write(reg_label))
        self.wait(1)

        # 5. Predict for a New House
        new_house_size = 6.0  # A house of 6 sq ft
        predicted_price = 0.75 * new_house_size + 1.0  # Prediction from our line

        new_house_dot = Dot(axes.c2p(new_house_size, 0), color=BLUE, radius=0.15, z_index=3)
        size_label = Text(f"New House (Size: {new_house_size:.1f})", font_size=20, color=BLUE).next_to(new_house_dot,
                                                                                                       DOWN, buff=0.1)

        # Animate the dot moving up to the regression line
        projection_line = DashedLine(
            axes.c2p(new_house_size, 0),
            axes.c2p(new_house_size, predicted_price),
            color=BLUE
        )
        predicted_price_label = Text(f"Predicted Price: {predicted_price:.1f}", font_size=20, color=BLUE).next_to(
            new_house_dot, RIGHT, buff=0.1)
        predicted_price_label.shift(UP * 0.5)  # Shift up to not overlap dot initially

        self.play(
            FadeIn(new_house_dot, scale=0.5),
            Write(size_label)
        )
        self.wait(0.5)

        self.play(
            new_house_dot.animate.move_to(axes.c2p(new_house_size, predicted_price)),
            Create(projection_line),
            Write(predicted_price_label)
        )
        self.wait(2)