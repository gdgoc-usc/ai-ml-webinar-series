from manim import *
import random


# Define a helper function to create a "chromosome"
# This is a VGroup of 5 colored squares (genes)
def create_chromosome(colors, gene_size=0.5):
    chromosome = VGroup()
    for color in colors:
        gene = Square(side_length=gene_size, color=color, fill_opacity=1)
        chromosome.add(gene)
    # Arrange genes horizontally next to each other
    chromosome.arrange(RIGHT, buff=0)
    return chromosome


class GeneticAlgorithmScene(Scene):
    def construct(self):
        # 0. Title and Target
        title = Text("Genetic Algorithm", font_size=36).to_edge(UP)

        # This is our "perfect" individual
        target_colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
        target_chromosome = create_chromosome(target_colors)
        target_label = Text("Target:", font_size=24).next_to(target_chromosome, LEFT)

        target_group = VGroup(target_label, target_chromosome).to_edge(UP, buff=1.5)
        self.play(Write(title), FadeIn(target_group))

        gen_counter = Text("Generation: 1", font_size=28).to_edge(LEFT, buff=0.5).shift(UP * 1.0)
        self.play(Write(gen_counter))

        # --------------------------------------------------
        # Phase 1: Initial Population (Gen 1)
        # ----------------------------------z----------------

        # Create 4 random individuals for Generation 1
        pop_1 = [
            create_chromosome([RED, ORANGE, PURPLE, GREY, GREEN]),
            create_chromosome([PINK, GREEN, BLUE, WHITE, BLACK]),
            create_chromosome([MAROON, PURPLE, BLUE, YELLOW, WHITE]),
            create_chromosome([RED, GREEN, GREY, ORANGE, PINK])
        ]

        # VGroup them and arrange them vertically
        population = VGroup(*pop_1).arrange(DOWN, buff=0.4).shift(DOWN * 0.5)
        self.play(FadeIn(population))

        # --------------------------------------------------
        # Phase 2: Fitness & Selection
        # --------------------------------------------------
        step_label = Text("1. Fitness & Selection", font_size=24).to_edge(RIGHT, buff=1.0).align_to(gen_counter, UP)
        self.play(Write(step_label))

        # Show fitness scores (how many genes match the target)
        scores = [
            Text("Fit: 1/5", font_size=20).next_to(pop_1[0], RIGHT, buff=0.2),
            Text("Fit: 2/5", font_size=20).next_to(pop_1[1], RIGHT, buff=0.2),
            Text("Fit: 2/5", font_size=20).next_to(pop_1[2], RIGHT, buff=0.2),
            Text("Fit: 3/5", font_size=20).next_to(pop_1[3], RIGHT, buff=0.2)
        ]
        self.play(Write(VGroup(*scores)))

        # We select the "fittest" two as parents
        # We fade out the "unfit" ones
        self.play(
            FadeOut(pop_1[0], shift=LEFT), FadeOut(scores[0]),
            FadeOut(pop_1[2], shift=LEFT), FadeOut(scores[2]),
            # Move the "parents" to the center
            pop_1[1].animate.move_to(LEFT * 2 + DOWN * 0.5),
            pop_1[3].animate.move_to(LEFT * 2 + DOWN * 1.5),
            FadeOut(scores[1]), FadeOut(scores[3])
        )

        parent_A = pop_1[1]
        parent_B = pop_1[3]

        parent_labels = VGroup(
            Text("Parent A", font_size=20).next_to(parent_A, UP),
            Text("Parent B", font_size=20).next_to(parent_B, DOWN)
        )
        self.play(Write(parent_labels))
        self.wait(1)

        # --------------------------------------------------
        # Phase 3: Crossover
        # --------------------------------------------------
        new_step_label = Text("2. Crossover", font_size=24).move_to(step_label)
        self.play(Transform(step_label, new_step_label), FadeOut(parent_labels))

        # Define the children based on a "crossover" point (e.g., after gene 3)
        # Child 1 = Parent A[0:3] + Parent B[3:5]
        child_A_colors = [PINK, GREEN, BLUE] + [ORANGE, PURPLE]

        # Child 2 = Parent B[0:3] + Parent A[3:5]
        child_B_colors = [RED, GREEN, GREY] + [WHITE, BLACK]

        child_A = create_chromosome(child_A_colors).move_to(RIGHT * 2 + DOWN * 0.5)
        child_B = create_chromosome(child_B_colors).move_to(RIGHT * 2 + DOWN * 1.5)

        children_label = Text("Children", font_size=24).next_to(VGroup(child_A, child_B), UP, buff=0.5)

        # Show the crossover with highlights
        # Highlight Parent A's contribution to Child A
        self.play(Indicate(VGroup(parent_A[0], parent_A[1], parent_A[2]), color=YELLOW, scale_factor=1.2))
        # Highlight Parent B's contribution to Child A
        self.play(Indicate(VGroup(parent_B[3], parent_B[4]), color=YELLOW, scale_factor=1.2))

        # Fade in the first child
        self.play(FadeIn(child_A))
        self.wait(0.5)

        # Do the same for the second child
        self.play(Indicate(VGroup(parent_B[0], parent_B[1], parent_B[2]), color=TEAL, scale_factor=1.2))
        self.play(Indicate(VGroup(parent_A[3], parent_A[4]), color=TEAL, scale_factor=1.2))
        self.play(FadeIn(child_B))
        self.play(Write(children_label))
        self.wait(1)

        # --------------------------------------------------
        # Phase 4: Mutation
        # --------------------------------------------------
        new_step_label = Text("3. Mutation", font_size=24).move_to(step_label)
        self.play(Transform(step_label, new_step_label))

        # We'll mutate the 3rd gene of Child B (GREY -> BLUE)
        # This makes it a "good" mutation, as it now matches the target
        self.play(
            Flash(child_B[2], color=RED, line_length=0.2),
            child_B[2].animate.set_color(BLUE)
        )
        self.wait(1)

        # --------------------------------------------------
        # Phase 5: New Generation
        # --------------------------------------------------
        new_step_label = Text("New Generation!", font_size=24).move_to(step_label)
        new_gen_counter = Text("Generation: 2", font_size=28).move_to(gen_counter)

        self.play(
            Transform(step_label, new_step_label),
            Transform(gen_counter, new_gen_counter),
            FadeOut(parent_A),
            FadeOut(parent_B),
            FadeOut(children_label),
            # Move children to the center
            child_A.animate.move_to(LEFT * 2 + DOWN * 0.5),
            child_B.animate.move_to(LEFT * 2 + DOWN * 1.5),
        )

        # Show the new, *better* fitness scores
        # Child A: [PINK, GREEN, BLUE, ORANGE, MAGENTA] -> Fit: 3/5
        # Child B: [RED, GREEN, BLUE, WHITE, BLACK] -> Fit: 3/5

        new_scores = [
            Text("Fit: 3/5", font_size=20).next_to(child_A, RIGHT, buff=0.2),
            Text("Fit: 3/5", font_size=20).next_to(child_B, RIGHT, buff=0.2),
        ]

        self.play(Write(VGroup(*new_scores)))

        # Conclude
        conclusion = Text("...and the process repeats.", font_size=24).next_to(VGroup(child_A, child_B), DOWN, buff=1.0)
        self.play(Write(conclusion))
        self.wait(3)