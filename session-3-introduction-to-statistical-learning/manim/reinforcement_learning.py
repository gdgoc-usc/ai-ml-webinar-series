from manim import *


class ReinforcementLearningScene(Scene):
    def construct(self):
        # 0. Title and Environment Setup
        title = Text("Reinforcement Learning", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Create the "environment": a simple grid path
        grid = VGroup(*[Square(side_length=1.0) for _ in range(5)])
        grid.arrange(RIGHT, buff=0).shift(DOWN * 0.5)

        # Define Start, Hazard, and Goal
        start_pos = grid[0].get_center()
        hazard_pos = grid[2].get_center()
        goal_pos = grid[4].get_center()

        hazard = Text("X", color=RED, font_size=48).move_to(hazard_pos)
        goal = Star(color=GREEN, fill_opacity=1).scale(0.4).move_to(goal_pos)

        env_labels = VGroup(
            Text("Start", font_size=20).next_to(grid[0], DOWN),
            Text("Hazard!", font_size=20).next_to(grid[2], DOWN),
            Text("Goal!", font_size=20).next_to(grid[4], DOWN)
        )

        self.play(Create(grid), Write(hazard), Write(goal), Write(env_labels))
        self.wait(1)

        # --------------------------------------------------
        # Phase 1: Exploration (Trial 1 - Failure)
        # --------------------------------------------------
        subtitle = Text("Trial 1: Exploration", font_size=28).next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Create the "Agent"
        agent = Circle(radius=0.25, color=BLUE, fill_opacity=1).move_to(start_pos)
        agent_label = Text("Agent", font_size=20).next_to(agent, UP)
        self.play(FadeIn(agent), Write(agent_label))

        # Agent moves into the hazard
        self.play(agent.animate.move_to(hazard_pos), FadeOut(agent_label))

        # Receives negative reward
        reward = Text("-10", color=RED, font_size=36).next_to(agent, UP)
        self.play(Write(reward))
        self.wait(1)

        # Reset for next trial
        self.play(FadeOut(reward), agent.animate.move_to(start_pos))

        # --------------------------------------------------
        # Phase 2: Learning (Policy is Updated)
        # --------------------------------------------------
        new_subtitle = Text("Policy is Updated...", font_size=28).move_to(subtitle)

        # Show a "brain" or "policy table" update
        policy_table = Table(
            [["S0", "→ +1"],
             ["S1", "→ -10"],  # State 1 has a bad action
             ["S2", "→ +20"],
             ["S3", "→ +5"]],
            row_labels=[Text("S0"), Text("S1"), Text("S2"), Text("S3")],
            col_labels=[Text("State"), Text("Value")]
        ).scale(0.3).to_edge(RIGHT, buff=1.0)

        self.play(Transform(subtitle, new_subtitle), FadeIn(policy_table))

        # "Update" the bad value
        new_row = Table([["S1", "→ -50"]]).scale(0.3).move_to(policy_table.get_rows()[2])
        self.play(Transform(policy_table.get_rows()[2], new_row), run_time=1.5)
        self.wait(1)

        # --------------------------------------------------
        # Phase 3: Exploitation (Trial 2 - Success)
        # --------------------------------------------------
        new_subtitle = Text("Trial 2: Exploitation (Optimal Path)", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle), FadeOut(policy_table))

        # Agent now knows to avoid the hazard. We'll add a "jump" to show a new policy.
        # It takes an "Up" and "Over" path
        path = ArcBetweenPoints(start_pos + UP * 0.5, goal_pos + UP * 0.5, angle=-PI / 1.5)

        self.play(MoveAlongPath(agent, path), run_time=2.0)

        # Receives positive reward
        reward = Text("+20", color=GREEN, font_size=36).next_to(agent, UP)
        self.play(Write(reward))

        self.play(Indicate(agent, color=GREEN), Indicate(goal, color=GREEN))
        self.wait(3)


from manim import *


class RLGridWorldScene(Scene):
    def construct(self):
        # 0. Title
        title = Text("Reinforcement Learning", font_size=36).to_edge(UP)
        self.play(Write(title), run_time=0.33)

        # --------------------------------------------------
        # Phase 1: Setup the Environment
        # --------------------------------------------------
        subtitle = Text("The Environment", font_size=28).next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=0.33)

        # Create a 4x4 grid
        grid = VGroup(*[
            VGroup(*[Square(side_length=1.2) for _ in range(4)])
                      .arrange(RIGHT, buff=0)
            for _ in range(4)
        ]).arrange(DOWN, buff=0)

        # --- THIS IS THE CORRECTED LINE ---
        grid.scale(0.9).move_to(DOWN * 0.5)
        # --- END OF CORRECTION ---

        self.play(Create(grid), run_time=0.33)

        # Define key locations (cells)
        # Manim's indexing: grid[row][col]
        start_cell = grid[3][0]
        goal_cell = grid[0][3]
        hazard_cells = [grid[1][1], grid[1][2], grid[2][2]]

        # Add Start, Goal, and Hazard markers
        start = Text("S", font_size=24, color=WHITE).move_to(start_cell.get_center())
        goal = Star(color=GREEN, fill_opacity=1).scale(0.4).move_to(goal_cell.get_center())
        hazards = VGroup(*[
            Text("X", font_size=36, color=RED).move_to(cell.get_center())
            for cell in hazard_cells
        ])

        self.play(Write(start), Write(goal), Write(hazards), run_time=0.33)
        self.wait(0.33)

        # Create the Agent
        agent = Circle(radius=0.25, color=BLUE, fill_opacity=1).move_to(start_cell.get_center())
        self.play(FadeIn(agent), run_time=0.33)
        self.wait(0.33)

        # --------------------------------------------------
        # Phase 2: Trial 1 (Exploration & Failure)
        # --------------------------------------------------
        new_subtitle = Text("Trial 1: Exploration (Random Moves)", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle), run_time=0.33)

        # Path: (3,0) -> (2,0) -> (2,1) -> (2,2) [HIT HAZARD]
        path_1 = [
            grid[2][0].get_center(),
            grid[2][1].get_center(),
            grid[2][2].get_center()  # Hazard
        ]

        for pos in path_1:
            self.play(agent.animate.move_to(pos), run_time=0.13)

            # Show negative reward
        reward = Text("-10", color=RED, font_size=36).next_to(agent, UP)
        self.play(Write(reward), run_time=0.33)
        self.wait(0.33)

        # Reset
        self.play(FadeOut(reward), agent.animate.move_to(start_cell.get_center()), run_time=0.33)
        self.wait(0.33)

        # --------------------------------------------------
        # Phase 3: "Learning"
        # --------------------------------------------------
        new_subtitle = Text("...Policy Table is Updated...", font_size=28).move_to(subtitle)

        # Flash the bad path to show it's "learned"
        bad_path_group = VGroup(*[grid[2][0], grid[2][1], grid[2][2]])
        self.play(Transform(subtitle, new_subtitle),
                  Flash(bad_path_group, color=RED, line_length=0.2), run_time=0.33)
        self.wait(0.5)

        # --------------------------------------------------
        # Phase 4: Trial 2 (Exploitation & Success)
        # --------------------------------------------------
        new_subtitle = Text("Trial 2: Exploitation (Optimal Path)", font_size=28).move_to(subtitle)
        self.play(Transform(subtitle, new_subtitle), run_time=0.33)

        # The optimal path
        optimal_path = [
            grid[3][1].get_center(),
            grid[3][2].get_center(),
            grid[3][3].get_center(),
            grid[2][3].get_center(),
            grid[1][3].get_center(),
            grid[0][3].get_center()  # Goal
        ]

        # Show the path first
        path_line = VGroup()
        last_pos = start_cell.get_center()
        for pos in optimal_path:
            path_line.add(Line(last_pos, pos, color=GREEN, stroke_width=3))
            last_pos = pos

        self.play(Create(path_line), run_time=0.33)

        # Move the agent along the path
        for pos in optimal_path:
            self.play(agent.animate.move_to(pos), run_tine=0.1)

            # Show positive reward
        reward = Text("+20", color=GREEN, font_size=36).next_to(agent, UP)
        self.play(Write(reward), run_time=0.33)

        self.play(Indicate(agent, color=GREEN), Indicate(goal, color=GREEN), run_time=0.33)
        self.wait(1)