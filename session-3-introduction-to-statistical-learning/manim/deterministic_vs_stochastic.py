from manim import *
import numpy as np

class DeterministicVsStochasticFinal(Scene):
    def construct(self):

        # --------------------------------------------------
        # 0. Title
        # --------------------------------------------------
        title = Text("Deterministic vs. Stochastic Processes", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 1. Labels
        deterministic_label = Text(
            "Deterministic Process (Pendulum)", font_size=24, color=BLUE
        ).to_edge(UP, buff=1.5).shift(LEFT * 3.5)

        stochastic_label = Text(
            "Stochastic Process (SDE)", font_size=24, color=RED
        ).to_edge(UP, buff=1.5).shift(RIGHT * 3.5)

        self.play(Write(deterministic_label), Write(stochastic_label))

        # Separator line
        separator = Line(UP * 3.5, DOWN * 3.5, color=GREY)
        self.play(Create(separator))
        self.wait(0.5)

        # --------------------------------------------------
        # LEFT SIDE — Deterministic Pendulum
        # --------------------------------------------------
        pivot = Dot(point=LEFT * 3.5 + UP * 2, radius=0.08, color=WHITE)
        rod = Line(pivot.get_center(), pivot.get_center() + DOWN * 1.5 + LEFT * 0.5, color=GREY_A)
        bob = Circle(radius=0.2, color=BLUE, fill_opacity=1).move_to(rod.get_end())
        pendulum = VGroup(rod, bob)

        time_tracker = ValueTracker(0)

        def update_pendulum(mobject, initial_angle=PI / 4, period=2):
            t = time_tracker.get_value() % period
            angle = initial_angle * np.cos(2 * PI * t / period)
            bob_pos = pivot.get_center() + rotate_vector(DOWN * 1.5, angle)
            mobject.become(
                VGroup(
                    Line(pivot.get_center(), bob_pos, color=GREY_A),
                    Circle(radius=0.2, color=BLUE, fill_opacity=1).move_to(bob_pos)
                )
            )

        self.play(Create(pendulum))
        pendulum.add_updater(update_pendulum)
        self.add(pendulum)

        trace_label_det = Text("Always the same path", font_size=18, color=BLUE)\
            .next_to(pendulum, DOWN, buff=0.5).shift(LEFT * 1)
        self.play(Write(trace_label_det))

        path_det = TracedPath(bob.get_center, stroke_color=BLUE_A, stroke_width=2)
        self.add(path_det)

        self.play(time_tracker.animate.set_value(4), run_time=4, rate_func=linear)
        repeat_text = Text("Repeatable", font_size=22, color=BLUE).next_to(trace_label_det, DOWN)
        self.play(Write(repeat_text))
        self.play(time_tracker.animate.set_value(6), run_time=2, rate_func=linear)

        pendulum.remove_updater(update_pendulum)
        self.remove(path_det)
        self.wait(1)

        # --------------------------------------------------
        # RIGHT SIDE — Stochastic Process (Brownian Motion)
        # --------------------------------------------------

        # SDE Formula
        # sde_formula = MathTex(r"dX_t = dW_t", font_size=36, color=RED)\
        #     .move_to(RIGHT * 3.5 + UP * 2.5)
        # self.play(Write(sde_formula))

        # Axes for stochastic plot
        axes_stoch = Axes(
            x_range=[0, 10, 2],
            y_range=[-4, 4, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": GREY, "include_tip": False},
        ).move_to(RIGHT * 3.5 + DOWN * 0.5)

        axes_labels = axes_stoch.get_axis_labels(
            x_label=Text("t", font_size=20),
            y_label=Text("X_t", font_size=20),
        )

        self.play(Create(axes_stoch), Write(axes_labels))

        # Brownian motion generator
        def generate_brownian_path(n_steps, total_time):
            dt = total_time / n_steps
            dW = np.random.normal(scale=np.sqrt(dt), size=n_steps - 1)
            W = np.zeros(n_steps)
            W[1:] = np.cumsum(dW)
            x_vals = np.linspace(0, total_time, n_steps)
            return x_vals, W

        n_steps = 200
        total_time = 10
        path_colors = [ORANGE, YELLOW, PINK]

        # Draw 3 independent realizations
        for i in range(3):
            x_vals, y_vals = generate_brownian_path(n_steps, total_time)
            current_plot = axes_stoch.plot_line_graph(
                x_values=x_vals,
                y_values=y_vals,
                line_color=path_colors[i],
                add_vertex_dots=False
            )
            self.play(Create(current_plot, run_time=1.0))
            self.wait(0.3)

        trace_label_stoch = Text("Different path each time", font_size=18, color=RED)\
            .next_to(axes_stoch, DOWN, buff=0.5)
        self.play(Write(trace_label_stoch))

        unpredictable_text = Text("Unpredictable", font_size=22, color=RED)\
            .next_to(trace_label_stoch, DOWN)
        self.play(Write(unpredictable_text))

        self.wait(2)


class ChaosVsRandomness(Scene):
    def construct(self):
        # 0. Global Setup
        self.camera.background_color = "#1a1a2e"  # Dark space background
        animation_duration = 25.0

        # 1. Title and Layout
        title = Text("Complex Systems", font_size=36).to_edge(UP)

        # Labels for Sections
        chaotic_label = Text("Chaotic System (3-Body)", font_size=24, color=YELLOW).to_edge(UP, buff=1.5).shift(
            LEFT * 4.0)
        stochastic_label = Text("Stochastic System (SDE)", font_size=24, color=RED).to_edge(UP, buff=1.5).shift(
            RIGHT * 3.5)

        # Separator line
        separator = Line(UP * 3.5, DOWN * 3.5, color=GREY).move_to(ORIGIN)
        self.play(Write(title), Write(chaotic_label), Write(stochastic_label), Create(separator))
        self.wait(0.5)

        # --------------------------------------------------
        # LEFT SIDE: 3-Body Problem (Chaotic)
        # --------------------------------------------------

        G_3body = 0.5
        scene_shift = LEFT * 4.0  # Shift everything to the left side

        # Body 1
        m1 = 1.0
        p1 = np.array([0.0, 0.0, 0.0]) + scene_shift
        v1 = np.array([0.0, 0.0, 0.0])
        color1 = YELLOW

        # Body 2
        m2 = 0.5
        p2 = np.array([3.0, 0.0, 0.0]) + scene_shift
        v2 = np.array([0.0, 0.8, 0.0])
        color2 = BLUE_C

        # Body 3
        m3 = 0.3
        p3 = np.array([0.0, -2.0, 0.0]) + scene_shift
        v3 = np.array([0.7, 0.0, 0.0])
        color3 = GREEN_C

        # Create Mobjects for the bodies
        body1 = Dot(color=color1, radius=0.25).move_to(p1).set_z_index(3)
        body2 = Dot(color=color2, radius=0.15).move_to(p2).set_z_index(3)
        body3 = Dot(color=color3, radius=0.10).move_to(p3).set_z_index(3)
        self.add(body1, body2, body3)

        bodies_data = [
            {"mobj": body1, "pos": p1, "vel": v1, "mass": m1, "color": color1, "prev_pos": p1,
             "path_segments": VGroup().set_z_index(1)},
            {"mobj": body2, "pos": p2, "vel": v2, "mass": m2, "color": color2, "prev_pos": p2,
             "path_segments": VGroup().set_z_index(1)},
            {"mobj": body3, "pos": p3, "vel": v3, "mass": m3, "color": color3, "prev_pos": p3,
             "path_segments": VGroup().set_z_index(1)},
        ]

        for body_data in bodies_data:
            self.add(body_data["path_segments"])

        # Physics Updater for 3-Body
        def update_nbody_physics(mobj, dt):
            current_bodies_data = list(bodies_data)
            accelerations = [np.array([0.0, 0.0, 0.0])] * len(current_bodies_data)

            for i in range(len(current_bodies_data)):
                for j in range(len(current_bodies_data)):
                    if i != j:
                        body_i = current_bodies_data[i];
                        body_j = current_bodies_data[j]
                        r_vec = body_j["pos"] - body_i["pos"]
                        r_mag_sq = np.dot(r_vec, r_vec)
                        r_mag = np.sqrt(r_mag_sq)
                        epsilon = 0.1
                        if r_mag > epsilon:
                            accelerations[i] += (G_3body * body_j["mass"] / r_mag_sq) * (r_vec / r_mag)

            for i, body_data in enumerate(current_bodies_data):
                body_data["vel"] += accelerations[i] * dt
                body_data["pos"] += body_data["vel"] * dt
                body_data["mobj"].move_to(body_data["pos"])

        # Path Fading Updater (re-usable)
        def update_fading_path(segments_vgroup, dt, body_data, max_segments):
            current_pos = body_data["mobj"].get_center()
            if np.linalg.norm(current_pos - body_data["prev_pos"]) > 0.05:
                new_segment = Line(
                    body_data["prev_pos"], current_pos,
                    color=body_data["color"], stroke_width=2
                )
                segments_vgroup.add(new_segment)
                body_data["prev_pos"] = current_pos

            if len(segments_vgroup) > max_segments:
                segments_vgroup.remove(segments_vgroup[0])

            for i, segment in enumerate(segments_vgroup):
                segment.set_stroke(opacity=(i / max_segments))

        # Add 3-Body Updaters
        simulation_driver_3body = Dot().set_opacity(0)
        simulation_driver_3body.add_updater(update_nbody_physics)
        self.add(simulation_driver_3body)

        for body_data in bodies_data:
            body_data["path_segments"].add_updater(
                lambda m, dt, bd=body_data: update_fading_path(m, dt, bd, max_segments=40)
            )

        # --------------------------------------------------
        # RIGHT SIDE: SDE (Stochastic)
        # --------------------------------------------------

        # Create Axes for the plot
        axes_stoch = Axes(
            x_range=[0, 8.5, 2],  # Time from 0 to 8.33
            y_range=[-4, 4, 1],  # Value
            x_length=6,
            y_length=4,
            axis_config={"color": GREY, "include_tip": False},
        ).move_to(RIGHT * 3.5 + DOWN * 0.5)
        axes_labels = axes_stoch.get_axis_labels(x_label=Text("t", font_size=20), y_label=Text("X_t", font_size=20))
        self.play(Create(axes_stoch), Write(axes_labels))

        sde_start_pos = axes_stoch.c2p(0, 0)

        # Create the SDE particle
        sde_particle = Dot(color=RED, radius=0.08).move_to(sde_start_pos).set_z_index(3)
        self.add(sde_particle)

        # Data for the SDE particle state
        sde_particle_data = {
            "mobj": sde_particle,
            "t": 0.0,  # Current time in simulation
            "val": 0.0,  # Current value (W_t)
            "color": RED,
            "prev_pos": sde_start_pos,
            "path_segments": VGroup().set_z_index(1)
        }
        self.add(sde_particle_data["path_segments"])

        # SDE Particle Updater
        def update_sde_particle(mobj, dt):
            data = sde_particle_data  # Get the state

            # Reset logic: 25.0 / 3 paths = ~8.33 sec per path
            if data["t"] > (animation_duration / 3.0):
                data["t"] = 0.0
                data["val"] = 0.0
                data["prev_pos"] = axes_stoch.c2p(0, 0)
                data["mobj"].move_to(axes_stoch.c2p(0, 0))
                # Clear the old path completely
                data["path_segments"].remove(*data["path_segments"])
                return  # Skip the rest of the update for this frame

            # Update time and value
            data["t"] += dt

            # Calculate dW (the random step)
            # We scale sqrt(dt) to make the walk more visually apparent
            dW = np.random.normal(scale=np.sqrt(dt)) * 2.0
            data["val"] += dW

            # Keep value within plot bounds (simple clipping)
            if data["val"] > 4.0: data["val"] = 4.0
            if data["val"] < -4.0: data["val"] = -4.0

            new_pos = axes_stoch.c2p(data["t"], data["val"])
            data["mobj"].move_to(new_pos)

        # Add SDE Updaters
        sde_driver = Dot().set_opacity(0)
        sde_driver.add_updater(update_sde_particle)
        self.add(sde_driver)

        # Add the *same* fading path updater, just with different data
        sde_particle_data["path_segments"].add_updater(
            lambda m, dt: update_fading_path(m, dt, sde_particle_data, max_segments=100)
        )

        # --------------------------------------------------
        # Run Both Simulations
        # --------------------------------------------------

        # This single wait call will run all active updaters (both 3-body
        # and SDE) simultaneously for 25 seconds.

        self.wait(animation_duration)


class SDE_Scene(Scene):
    def construct(self):
        # 0. Global Setup
        self.camera.background_color = "#1a1a2e"  # Dark space background
        animation_duration = 25.0

        # 1. Title and Layout
        title = Text("Stochastic Process (SDE)", font_size=36).to_edge(UP)
        sde_formula = MathTex(r"dX_t = \mu X_t dt + \sigma X_t dW_t", font_size=32, color=RED).next_to(title, DOWN,
                                                                                                       buff=0.5)
        # We'll show a simpler form for the label
        #sde_label = MathTex(r"(Simulating dX_t = dW_t)", font_size=24, color=GREY).next_to(sde_formula, DOWN, buff=0.2)

        self.play(Write(title), Write(sde_formula))
        self.wait(0.5)

        # --------------------------------------------------
        # RIGHT SIDE: SDE (Stochastic)
        # --------------------------------------------------

        # Create Axes for the plot, centered
        axes_stoch = Axes(
            x_range=[0, 8.5, 2],  # Time from 0 to 8.33
            y_range=[-4, 4, 1],  # Value
            x_length=8,  # Make it larger since it's the only element
            y_length=5,
            axis_config={"color": GREY, "include_tip": False},
        ).move_to(DOWN * 0.5)  # Center it with a slight offset down

        axes_labels = axes_stoch.get_axis_labels(x_label=Text("t", font_size=24), y_label=Text("X_t", font_size=24))
        self.play(Create(axes_stoch), Write(axes_labels))

        sde_start_pos = axes_stoch.c2p(0, 0)

        # Create the SDE particle
        sde_particle = Dot(color=RED, radius=0.08).move_to(sde_start_pos).set_z_index(3)
        self.add(sde_particle)

        # Data for the SDE particle state
        sde_particle_data = {
            "mobj": sde_particle,
            "t": 0.0,  # Current time in simulation
            "val": 0.0,  # Current value (W_t)
            "color": RED,
            "prev_pos": sde_start_pos,
            "path_segments": VGroup().set_z_index(1)
        }
        self.add(sde_particle_data["path_segments"])

        # Path Fading Updater
        def update_fading_path(segments_vgroup, dt, body_data, max_segments):
            current_pos = body_data["mobj"].get_center()
            if np.linalg.norm(current_pos - body_data["prev_pos"]) > 0.05:
                new_segment = Line(
                    body_data["prev_pos"], current_pos,
                    color=body_data["color"], stroke_width=3  # Made path slightly thicker
                )
                segments_vgroup.add(new_segment)
                body_data["prev_pos"] = current_pos

            if len(segments_vgroup) > max_segments:
                segments_vgroup.remove(segments_vgroup[0])

            for i, segment in enumerate(segments_vgroup):
                segment.set_stroke(opacity=(i / max_segments))

        # SDE Particle Updater
        def update_sde_particle(mobj, dt):
            data = sde_particle_data  # Get the state

            # Reset logic: 25.0 / 3 paths = ~8.33 sec per path
            if data["t"] > (animation_duration / 3.0):
                data["t"] = 0.0
                data["val"] = 0.0
                data["prev_pos"] = axes_stoch.c2p(0, 0)
                data["mobj"].move_to(axes_stoch.c2p(0, 0))
                # Clear the old path completely
                data["path_segments"].remove(*data["path_segments"])
                return  # Skip the rest of the update for this frame

            # Update time and value
            data["t"] += dt

            # Calculate dW (the random step)
            # We scale sqrt(dt) to make the walk more visually apparent
            dW = np.random.normal(scale=np.sqrt(dt)) * 2.0
            data["val"] += dW

            # Keep value within plot bounds (simple clipping)
            if data["val"] > 4.0: data["val"] = 4.0
            if data["val"] < -4.0: data["val"] = -4.0

            new_pos = axes_stoch.c2p(data["t"], data["val"])
            data["mobj"].move_to(new_pos)

        # Add SDE Updaters
        sde_driver = Dot().set_opacity(0)
        sde_driver.add_updater(update_sde_particle)
        self.add(sde_driver)

        # Add the fading path updater
        sde_particle_data["path_segments"].add_updater(
            lambda m, dt: update_fading_path(m, dt, sde_particle_data, max_segments=150)  # Longer tail
        )

        # --------------------------------------------------
        # Run Simulation
        # --------------------------------------------------

        self.wait(animation_duration)


class StochasticProcess(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"

        # 1. Setup Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=9,
            y_length=6,
            axis_config={"color": GREY_A},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
        ).to_edge(DOWN).add_coordinates()

        axes_labels = axes.get_axis_labels(
            x_label=Text("Education (x)", font_size=24),
            y_label=Text("Salary (Y)", font_size=24).rotate(PI / 2, about_point=ORIGIN)
        )
        self.add(axes, axes_labels)

        # 2. Define the "True" and "Model" functions
        # f(x) is the "hidden" true signal.
        def f(x):
            return 0.6 * x + 2

        # f_hat(x) is our "line of fit" model.
        def f_hat(x):
            return 0.58 * x + 2.1

        # 3. Draw the functions

        # --- THIS IS THE CORRECTION ---
        # First, create the continuous plot object
        #true_plot_line = axes.plot(f, x_range=[0, 10], color=GREEN)
        # Now, create a dashed VMobject using num_dashes
        #f_graph = DashedVMobject(true_plot_line, num_dashes=40, dashed_ratio=0.6)
        # --- END OF CORRECTION ---

        f_label = MathTex("f(x)", "\\text{ (True Signal)}", color=GREEN, font_size=28).to_edge(UP).shift(LEFT * 3)

        f_hat_graph = axes.plot(f_hat, x_range=[0, 10], color=BLUE)
        f_hat_label = MathTex("\\hat{Y} = \\hat{f}(x)", "\\text{ (Our Model)}", color=BLUE, font_size=28).next_to(
            f_label, DOWN)

        self.play(Write(f_label))

        # 4. Generate the "real" noisy data
        scatter_points = VGroup()
        for x_val in np.random.uniform(0.5, 9.5, 30):
            epsilon = np.random.normal(0, 0.8)  # The irreducible error
            y_val = f(x_val) + epsilon
            scatter_points.add(Dot(axes.c2p(x_val, y_val), color=WHITE, radius=0.05, fill_opacity=0.7))

        data_label = Text("Real Data: Y = f(x) + \u03B5", color=WHITE, font_size=28).to_edge(UP, buff=0.5).shift(
            RIGHT * 3)
        self.play(Write(data_label), FadeIn(scatter_points, scale=0.5))

        # 5. Show the model being "fit"
        self.play(Write(f_hat_label), Create(f_hat_graph))
        self.wait(1)

        # 6. Create the "Slider" animation
        x_tracker = ValueTracker(2)  # Start slider at x=2

        # The vertical slider line
        slider_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(x_tracker.get_value(), 0),
                axes.c2p(x_tracker.get_value(), 10),
                stroke_width=2,
                color=YELLOW
            )
        )
        x_label = always_redraw(
            lambda: MathTex(f"x = {x_tracker.get_value():.1f}", font_size=24)
            .next_to(slider_line, DOWN, buff=0.1)
        )

        # Dot for the model's prediction
        model_dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_tracker.get_value(), f_hat(x_tracker.get_value())),
                color=BLUE, radius=0.08
            )
        )
        model_dot_label = always_redraw(
            lambda: MathTex("\\hat{Y}", font_size=28, color=BLUE)
            .next_to(model_dot, RIGHT, buff=0.1)
        )

        # Dot for the "actual" stochastic outcome
        # This is the key: we re-sample epsilon *inside* the updater
        def get_actual_point():
            x_val = x_tracker.get_value()
            epsilon = np.random.normal(0, 0.8)  # New \epsilon every frame
            y_val = f(x_val) + epsilon
            return axes.c2p(x_val, y_val)

        actual_dot = always_redraw(
            lambda: Dot(get_actual_point(), color=RED, radius=0.08)
        )
        actual_dot_label = always_redraw(
            lambda: MathTex("Y", font_size=28, color=RED)
            .next_to(actual_dot, RIGHT, buff=0.1)
        )

        # Brace to show epsilon
        epsilon_brace = always_redraw(
            lambda: BraceBetweenPoints(
                model_dot.get_center(),  # From prediction
                actual_dot.get_center(),  # To actual
                direction=RIGHT,
                buff=0.1,
                color=RED
            )
        )
        epsilon_label = always_redraw(
            lambda: MathTex("\\epsilon", "\\text{ (Noise)}", font_size=24, color=RED)
            .next_to(epsilon_brace, RIGHT, buff=0.1)
        )

        self.play(Create(slider_line),
                  FadeIn(x_label, model_dot, actual_dot, model_dot_label, actual_dot_label, epsilon_brace,
                         epsilon_label))

        # 7. Animate the slider moving
        self.play(x_tracker.animate.set_value(9), run_time=6, rate_func=linear)

        # 8. Final Conclusion
        final_text = MathTex(
            "\\mathbb{E}[\\hat{Y}]", "\\neq", "Y",
            font_size=40
        ).to_edge(DOWN, buff=1.5).shift(LEFT * 3)
        final_text[0].set_color(BLUE)
        final_text[2].set_color(RED)

        arrow = Arrow(model_dot.get_center(), actual_dot.get_center(), buff=0.1, color=WHITE)

        self.play(Write(final_text), Create(arrow))
        self.wait(3)