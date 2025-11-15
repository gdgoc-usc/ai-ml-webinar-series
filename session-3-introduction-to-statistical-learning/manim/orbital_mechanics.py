from manim import *
import numpy as np


class OrbitalMechanicsLoop(Scene):
    def construct(self):
        # 0. Global Setup
        self.camera.background_color = "#1a1a2e"  # Dark space background

        # 1. Create the central body (star)
        # Place at one focus of the ellipse, not the origin.
        # We will shift the orbits to match.
        focus_shift = np.array([-2.0, 0, 0])
        central_body = Dot(color=YELLOW, radius=0.3).move_to(focus_shift).set_z_index(2)
        self.add(central_body)

        # 2. Define PERFECT, LOOPING paths (not simulated)
        # Use ParametricFunction to create perfect ellipses
        # t goes from 0 to 2*PI, guaranteeing a loop

        # Path 1: Large Ellipse
        path_1 = ParametricFunction(
            lambda t: np.array([
                4.0 * np.cos(t),  # Semi-major axis = 4.0
                2.5 * np.sin(t),  # Semi-minor axis = 2.5
                0
            ]) + focus_shift,  # Shift orbit so star is at focus
            t_range=[0, 2 * PI]
        )

        # Path 2: Smaller, Rotated Ellipse
        path_2_func = lambda t: np.array([
            2.5 * np.cos(t),  # Semi-major axis = 2.5
            2.0 * np.sin(t),  # Semi-minor axis = 2.0
            0
        ])
        path_2 = ParametricFunction(
            lambda t: rotate_vector(path_2_func(t), angle=PI / 4) + focus_shift,
            t_range=[0, 2 * PI]
        )

        # 3. Create the orbiters
        orbiter_1 = Dot(color=BLUE_C, radius=0.1).set_z_index(3)
        orbiter_2 = Dot(color=GREEN_C, radius=0.1).set_z_index(3)

        # Place orbiters at their starting positions
        orbiter_1.move_to(path_1.get_start())
        orbiter_2.move_to(path_2.get_start())

        # 4. Create VGroups to hold the fading path segments
        # We must manage the path segments manually for fading
        path_segments_1 = VGroup().set_z_index(1)
        path_segments_2 = VGroup().set_z_index(1)

        # Store previous positions. Must be a list to be mutable inside the updater.
        orbiter_1_prev_pos = [path_1.get_start()]
        orbiter_2_prev_pos = [path_2.get_start()]

        self.add(path_segments_1, path_segments_2, orbiter_1, orbiter_2)

        # 5. Define the Fading Path Updater
        def update_path_fading(segments_vgroup, dt, orbiter_color, orbiter_obj, prev_pos_list):
            current_pos = orbiter_obj.get_center()

            # Only add a new segment if the orbiter has moved
            if np.linalg.norm(current_pos - prev_pos_list[0]) > 0.01:
                new_segment = Line(
                    prev_pos_list[0],
                    current_pos,
                    color=orbiter_color,
                    stroke_width=3
                )
                segments_vgroup.add(new_segment)
                prev_pos_list[0] = current_pos  # Update the "previous" position

            # Control the tail length
            max_segments = 60  # Adjust this to make the tail longer or shorter
            if len(segments_vgroup) > max_segments:
                segments_vgroup.remove(segments_vgroup[0])  # Remove the oldest segment

            # Apply fading opacity to all segments
            for i, segment in enumerate(segments_vgroup):
                # Opacity goes from 0.0 (oldest) to 1.0 (newest)
                segment.set_stroke(opacity=(i / max_segments))

        # 6. Define the Orbiter Movement Updater
        # This updater moves the orbiter along its parametric path based on "time"
        def update_orbiter(mob, path, time_tracker):
            # Get alpha (0.0 to 1.0) from the time tracker
            # Use % 1.0 to make the alpha loop
            alpha = time_tracker.get_value() % 1.0
            mob.move_to(path.point_from_proportion(alpha))

        # 7. Use a ValueTracker to drive the looping animation
        # We will animate this tracker from 0 to N (e.g., 2 loops)
        time_tracker = ValueTracker(0)

        # 8. Add all updaters
        orbiter_1.add_updater(lambda m: update_orbiter(m, path_1, time_tracker))
        orbiter_2.add_updater(lambda m: update_orbiter(m, path_2, time_tracker))

        path_segments_1.add_updater(lambda m, dt: update_path_fading(m, dt, BLUE_C, orbiter_1, orbiter_1_prev_pos))
        path_segments_2.add_updater(lambda m, dt: update_path_fading(m, dt, GREEN_C, orbiter_2, orbiter_2_prev_pos))

        # 9. Play the animation
        # We animate the time_tracker from 0 to 2 (two full loops)
        # A 5-second GIF is a good, short length.
        # The rate_func=linear is crucial for a smooth, non-jerky loop.
        self.play(
            time_tracker.animate.set_value(2.0),  # Set value to 2.0 for 2 loops
            run_time=5.0,  # This is the total duration of the GIF
            rate_func=linear
        )


class ThreeBodyProblemLoop(Scene):
    def construct(self):
        # 0. Global Setup
        self.camera.background_color = "#1a1a2e"  # Dark space background

        # 1. Define bodies (masses, colors, initial positions, initial velocities)
        # These values are crucial and highly sensitive for behavior.
        # Tweaking them is how you get different chaotic patterns.
        # Mass: m1, m2, m3
        # Position: p1, p2, p3
        # Velocity: v1, v2, v3

        G = 0.5  # Gravitational constant (adjusted for desired speed/scale)

        # Body 1: Central-ish, heavy
        m1 = 1.0
        p1 = np.array([0.0, 0.0, 0.0])
        v1 = np.array([0.0, 0.0, 0.0])
        color1 = YELLOW

        # Body 2: Medium mass, orbiting
        m2 = 0.5
        p2 = np.array([3.0, 0.0, 0.0])
        v2 = np.array([0.0, 0.8, 0.0])
        color2 = BLUE_C

        # Body 3: Smaller mass, orbiting
        m3 = 0.3
        p3 = np.array([0.0, -2.0, 0.0])
        v3 = np.array([0.7, 0.0, 0.0])
        color3 = GREEN_C

        # Create Mobjects for the bodies
        body1 = Dot(color=color1, radius=0.25).move_to(p1).set_z_index(3)
        body2 = Dot(color=color2, radius=0.15).move_to(p2).set_z_index(3)
        body3 = Dot(color=color3, radius=0.10).move_to(p3).set_z_index(3)
        self.add(body1, body2, body3)

        # Store states (position, velocity, mass) in dictionaries for easier updater access
        # This is where the simulation state for each body lives
        bodies_data = [
            {"mobj": body1, "pos": p1, "vel": v1, "mass": m1, "color": color1, "prev_pos": p1,
             "path_segments": VGroup().set_z_index(1)},
            {"mobj": body2, "pos": p2, "vel": v2, "mass": m2, "color": color2, "prev_pos": p2,
             "path_segments": VGroup().set_z_index(1)},
            {"mobj": body3, "pos": p3, "vel": v3, "mass": m3, "color": color3, "prev_pos": p3,
             "path_segments": VGroup().set_z_index(1)},
        ]

        # Add all path segment VGroups to the scene
        for body_data in bodies_data:
            self.add(body_data["path_segments"])

        # 2. Physics Updater Function (N-body simulation)
        # This function updates all bodies' positions and velocities
        def update_nbody_physics(mobj, dt):  # mobj is a dummy, we update all bodies
            # Need to create a new list of bodies_data for safety
            # to avoid issues when iterating and modifying in place.
            current_bodies_data = list(bodies_data)  # Create a copy

            # Calculate accelerations for all bodies
            accelerations = [np.array([0.0, 0.0, 0.0])] * len(current_bodies_data)

            for i in range(len(current_bodies_data)):
                for j in range(len(current_bodies_data)):
                    if i != j:
                        body_i = current_bodies_data[i]
                        body_j = current_bodies_data[j]

                        r_vec = body_j["pos"] - body_i["pos"]
                        r_mag_sq = np.dot(r_vec, r_vec)
                        r_mag = np.sqrt(r_mag_sq)

                        # Small epsilon to prevent division by zero if bodies collide
                        epsilon = 0.1  # This value prevents explosion if bodies get too close
                        if r_mag > epsilon:
                            # a = G * M / r^2 * r_hat
                            accelerations[i] += (G * body_j["mass"] / r_mag_sq) * (r_vec / r_mag)

            # Update velocities and positions for all bodies
            for i, body_data in enumerate(current_bodies_data):
                body_data["vel"] += accelerations[i] * dt
                body_data["pos"] += body_data["vel"] * dt
                body_data["mobj"].move_to(body_data["pos"])  # Update Mobject's position

        # 3. Fading Path Updater
        # This function manages the fading trails for each body
        def update_path_fading(segments_vgroup, dt, body_data):
            current_pos = body_data["mobj"].get_center()

            # Add new segment if moved significantly
            if np.linalg.norm(current_pos - body_data["prev_pos"]) > 0.05:  # Adjusted sensitivity
                new_segment = Line(
                    body_data["prev_pos"],
                    current_pos,
                    color=body_data["color"],
                    stroke_width=2
                )
                segments_vgroup.add(new_segment)
                body_data["prev_pos"] = current_pos  # Update the "previous" position

            # Control the tail length
            max_segments = 40  # Shorter tail for chaotic motion looks better
            if len(segments_vgroup) > max_segments:
                segments_vgroup.remove(segments_vgroup[0])  # Remove the oldest segment

            # Apply fading opacity to all segments
            for i, segment in enumerate(segments_vgroup):
                segment.set_stroke(opacity=(i / max_segments))

        # 4. Add updaters to a dummy Mobject to drive the simulation
        # The actual bodies_data is updated by the simulation updater
        # Each path_segments VGroup also gets its own updater

        # A dummy Mobject to attach the main simulation updater to
        simulation_driver = Dot().set_opacity(0)  # Invisible dot
        simulation_driver.add_updater(update_nbody_physics)
        self.add(simulation_driver)  # Add it to the scene

        # Add fading path updaters to each body's path_segments VGroup
        for body_data in bodies_data:
            body_data["path_segments"].add_updater(lambda m, dt, bd=body_data: update_path_fading(m, dt, bd))

        # 5. Play the animation

        # --- THIS IS THE UPDATED LINE ---
        animation_duration = 15.0  # Total duration of the GIF (was 15.0)
        # --- END OF UPDATE ---

        self.wait(animation_duration)  # Let the simulation run for this duration