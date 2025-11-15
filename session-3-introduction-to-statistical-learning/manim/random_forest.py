from manim import *
import random


class RandomForestScene(Scene):
    def construct(self):
        # 0. Title
        title = Text("Random Forest Algorithm: Simple Visual", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 1. Original Data
        # CORRECTED TABLE:
        data_table = Table(
            [["1", "a", "A"],
             ["2", "b", "B"],
             ["3", "a", "A"],
             ["4", "c", "A"],
             ["5", "b", "B"],
             ["6", "c", "A"]],
            col_labels=[Text("X1"), Text("X2"), Text("Y")],
            line_config={"stroke_width": 1, "color": GRAY}
        ).scale(0.4)
        data_label = Text("Original Data", font_size=24).next_to(data_table, DOWN)
        data_group = VGroup(data_table, data_label).shift(LEFT * 4)

        self.play(Create(data_table), Write(data_label))
        self.wait(1)

        # 2. Bootstrapping (Bagging)
        bagging_label = Text("1. Bootstrap Sampling", font_size=28).next_to(title, DOWN, buff=1.0).shift(RIGHT * 3)
        self.play(Write(bagging_label))

        # Create 3 sample tables
        # CORRECTED TABLE 1:
        sample_1 = Table(
            [["1", "a", "A"],
             ["3", "a", "A"],
             ["1", "a", "A"],
             ["6", "c", "A"]],
            col_labels=[Text("X1"), Text("X2"), Text("Y")],
            line_config={"stroke_width": 1, "color": BLUE}
        ).scale(0.3)

        # CORRECTED TABLE 2:
        sample_2 = Table(
            [["5", "b", "B"],
             ["2", "b", "B"],
             ["4", "c", "A"],
             ["5", "b", "B"]],
            col_labels=[Text("X1"), Text("X2"), Text("Y")],
            line_config={"stroke_width": 1, "color": GREEN}
        ).scale(0.3)

        # CORRECTED TABLE 3:
        sample_3 = Table(
            [["4", "c", "A"],
             ["1", "a", "A"],
             ["3", "a", "A"],
             ["2", "b", "B"]],
            col_labels=[Text("X1"), Text("X2"), Text("Y")],
            line_config={"stroke_width": 1, "color": ORANGE}
        ).scale(0.3)

        samples = VGroup(sample_1, sample_2, sample_3).arrange(DOWN, buff=0.5).next_to(bagging_label, DOWN, buff=0.5)

        # Animate arrows from data to samples
        arrows = VGroup()
        for sample in samples:
            arrow = Arrow(data_group.get_right(), sample.get_left(), buff=0.1, stroke_width=3)
            arrows.add(arrow)

        self.play(Create(arrows), FadeIn(samples))
        self.wait(1)

        # 3. Build Trees
        tree_label = Text("2. Build Decision Trees", font_size=28).next_to(samples, RIGHT, buff=1.5).align_to(
            bagging_label, UP)
        self.play(Write(tree_label))

        # Create 3 simple tree diagrams
        tree_1 = self.create_simple_tree(BLUE)
        tree_2 = self.create_simple_tree(GREEN)
        tree_3 = self.create_simple_tree(ORANGE)

        trees = VGroup(tree_1, tree_2, tree_3).arrange(DOWN, buff=1.2).next_to(tree_label, DOWN, buff=0.7)

        # Animate arrows from samples to trees
        tree_arrows = VGroup()
        for i in range(3):
            arrow = Arrow(samples[i].get_right(), trees[i].get_left(), buff=0.1, stroke_width=3)
            tree_arrows.add(arrow)

        self.play(Create(tree_arrows), Create(trees))
        self.wait(1)

        # 4. Get Predictions
        pred_1 = Text("Pred: 'A'", color=RED_A, font_size=24).next_to(tree_1, RIGHT, buff=0.5)
        pred_2 = Text("Pred: 'B'", color=BLUE_A, font_size=24).next_to(tree_2, RIGHT, buff=0.5)
        pred_3 = Text("Pred: 'A'", color=RED_A, font_size=24).next_to(tree_3, RIGHT, buff=0.5)
        predictions = VGroup(pred_1, pred_2, pred_3)

        self.play(Write(predictions))
        self.wait(1)

        # 5. Voting
        vote_label = Text("3. Majority Vote", font_size=28).next_to(data_group, DOWN, buff=2.0).align_to(data_group,
                                                                                                         LEFT)
        final_box = Rectangle(width=4, height=2, color=YELLOW).next_to(vote_label, DOWN, buff=0.5)
        final_label = Text("Final Prediction", font_size=24).next_to(final_box, DOWN)

        self.play(Write(vote_label), Create(final_box), Write(final_label))

        # Animate predictions moving to the vote box
        self.play(
            pred_1.animate.move_to(final_box.get_center() + UP * 0.5 + LEFT * 1),
            pred_2.animate.move_to(final_box.get_center()),
            pred_3.animate.move_to(final_box.get_center() + UP * 0.5 + RIGHT * 1)
        )
        self.wait(1)

        # Show final result
        final_result = Text("'A'", color=RED_A, font_size=36).move_to(final_box.get_center()).shift(DOWN * 0.4)

        # Highlight the "A" votes and fade the "B" vote
        self.play(
            FadeOut(pred_2),
            pred_1.animate.move_to(final_box.get_center() + DOWN * 0.4 + LEFT * 0.5),
            pred_3.animate.move_to(final_box.get_center() + DOWN * 0.4 + RIGHT * 0.5),
        )
        # Transform the A's into the final result
        self.play(Transform(VGroup(pred_1, pred_3), final_result))
        self.wait(3)

    # Helper function to create a simple tree mobject
    def create_simple_tree(self, color):
        root = Circle(radius=0.2, color=color, fill_opacity=0.5)
        l1_node1 = Circle(radius=0.15, color=color, fill_opacity=0.5)
        l1_node2 = Circle(radius=0.15, color=color, fill_opacity=0.5)

        nodes = VGroup(l1_node1, l1_node2).arrange(RIGHT, buff=0.5).next_to(root, DOWN, buff=0.5)

        line1 = Line(root.get_bottom(), l1_node1.get_top())
        line2 = Line(root.get_bottom(), l1_node2.get_top())

        # Leaves
        leaf1 = Square(side_length=0.2, color=GRAY).next_to(l1_node1, DOWN, buff=0.3)
        leaf2 = Square(side_length=0.2, color=GRAY).next_to(l1_node1, DOWN, buff=0.3).shift(RIGHT * 0.3)
        leaf3 = Square(side_length=0.2, color=GRAY).next_to(l1_node2, DOWN, buff=0.3)

        line3 = Line(l1_node1.get_bottom(), leaf1.get_top())
        line4 = Line(l1_node1.get_bottom(), leaf2.get_top())
        line5 = Line(l1_node2.get_bottom(), leaf3.get_top())

        tree = VGroup(root, nodes, line1, line2, leaf1, leaf2, leaf3, line3, line4, line5)
        return tree.scale(0.8)


class RandomForestAnalogy(Scene):
    def construct(self):
        # --------------------------------------------------
        # Phase 1: Training ("Growing the Forest")
        # --------------------------------------------------

        # Title for the training phase
        # title = Text("Phase 1: Training", font_size=32).to_edge(UP)
        # subtitle = Text("The 'Forest' is grown from data", font_size=24).next_to(title, DOWN, buff=0.1)
        # self.play(Write(title), Write(subtitle))
        self.camera.background_color = "#1e1e1e"
        # Create a grid of 9 "trees"
        forest = VGroup()
        for i in range(9):
            # Use a slightly different green for variety
            color = random.choice([GREEN_C, GREEN_D, GREEN_E])
            tree = self.create_simple_tree(color)
            forest.add(tree)

        # Arrange the trees in a 3x3 grid
        forest.arrange_in_grid(rows=3, cols=3, buff=1.2)
        forest.scale(0.8)

        # "Grow" the forest. This is the "training" visualization.
        self.play(
            LaggedStart(
                *[GrowFromCenter(tree) for tree in forest],
                lag_ratio=0.15
            )
        )
        self.wait(1)

        # --------------------------------------------------
        # Phase 2: Inference ("Asking the Forest")
        # --------------------------------------------------

        # Update title for the inference phase
        # new_title = Text("Phase 2: Inference (Prediction)", font_size=32).to_edge(UP)
        # new_subtitle = Text("A new query is sent to all trees", font_size=24).next_to(new_title, DOWN, buff=0.1)
        # self.play(
        #     Transform(title, new_title),
        #     Transform(subtitle, new_subtitle)
        # )

        # Create a "query" (a new data point)
        query = Star(n=5, color=YELLOW, fill_opacity=1).scale(0.5)
        query.next_to(forest, UP, buff=1.0)
        self.play(FadeIn(query, scale=1.5))
        self.wait(0.5)

        # Send the query to all trees (like neurons firing)
        query_arrows = VGroup()
        for tree in forest:
            arrow = Arrow(query.get_bottom(), tree.get_top(), buff=0.2, stroke_width=3,
                          max_tip_length_to_length_ratio=0.1)
            query_arrows.add(arrow)

        self.play(Create(query_arrows))

        # All trees "activate" or "fire" in response
        self.play(
            LaggedStart(
                *[Indicate(tree, color=YELLOW, scale_factor=1.2) for tree in forest],
                lag_ratio=0.05
            ),
            FadeOut(query)  # Query has been "sent"
        )
        self.play(FadeOut(query_arrows))  # Clean up arrows

        # Each tree "votes"
        # We'll pre-define the votes (e.g., 6 vote 'A', 3 vote 'B')
        votes_list = ["A", "A", "B", "A", "B", "A", "A", "B", "A"]
        vote_colors = {"A": RED_E, "B": BLUE_E}

        vote_mobjects = VGroup()
        for i, tree in enumerate(forest):
            vote_text = votes_list[i]
            vote_color = vote_colors[vote_text]
            vote = Text(vote_text, color=vote_color, font_size=32).next_to(tree, DOWN, buff=0.2)
            vote_mobjects.add(vote)

        self.play(Write(vote_mobjects))
        self.wait(1)

        # --------------------------------------------------
        # Phase 3: Aggregation ("The Majority Vote")
        # --------------------------------------------------

        # new_subtitle_2 = Text("The votes are counted (Majority wins)", font_size=24).next_to(new_title, DOWN, buff=0.1)
        # self.play(Transform(subtitle, new_subtitle_2))

        # Create a "Final Answer" box
        final_box = Rectangle(width=3, height=1.5, color=YELLOW).to_edge(DOWN, buff=1.5)
        final_label = Text("Final Answer", font_size=24).next_to(final_box, UP)

        self.play(Create(final_box), Write(final_label))
        self.wait(0.5)

        # Animate votes moving to the box
        # We'll separate them by vote type
        group_A = VGroup()
        group_B = VGroup()

        for vote in vote_mobjects:
            if vote.text == "A":
                group_A.add(vote)
            else:
                group_B.add(vote)

        # Fade out the minority vote and move the majority vote
        final_result = Text("A", color=RED_E, font_size=48).move_to(final_box.get_center())

        self.play(
            FadeOut(group_B, shift=DOWN * 0.5),
            group_A.animate.move_to(final_box.get_center())
        )

        # Transform the majority votes into the single final answer
        self.play(
            Transform(group_A, final_result),
            FadeOut(forest)  # Fade out the forest to focus on the result
        )

        self.wait(3)

    # Helper function to create a simple graphical "tree"
    def create_simple_tree(self, color):
        # A green triangle for the leaves
        canopy = Triangle(fill_opacity=1, color=color, stroke_width=0).scale(0.5)
        canopy.set_sheen(0.1, DR)

        # A brown rectangle for the trunk
        trunk = Rectangle(height=0.4, width=0.1, fill_opacity=1, color=DARK_BROWN, stroke_width=0)
        trunk.next_to(canopy, DOWN, buff=0)

        tree = VGroup(canopy, trunk)
        return tree