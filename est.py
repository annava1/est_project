# Define a class - Primary Processes Modules
class Ppm:

    def __init__(self, p1, p2):
        self.ppm_1 = p1  # Initialize with the name of the primary processes forming and curing.
        self.ppm_2 = p2

    def display_process(self):
        print(f"The Primary Process modules used in the transformation are {self.ppm_1} and {self.ppm_2}")


# Define a class - Basic operations
class Bop:

    # Constructor for the class
    def __init__(self, press, pull):
        self.bop_1 = press  # Initialize with the name of the processes.
        self.bop_2 = pull

        # super().__init__("forming", "curing")

    def display_process_1(self):
        print(f"The basic operations used in the primary processes are  {self.bop_1} and {self.bop_2}")

    def press(self):
        compressive_strength = 335  # Default value for compressive strength from Excel sheet.
        area = 2410335.18  # Default value for area from Excel sheet.
        s_d = 10

        # Step 2: Get the user input for the parameter
        s_u = float(input("Enter the value for 's' (thickness reduction/strain): "))
        area_u = float(input("Enter the value for 'a' (area): "))
        cs_u = float(input("Enter the value for 'c' (compressive strength): "))

        def calculate_w(c, a, s):
            # Step 1: Perform the calculation W = compressive_strength * area * s
            return c * a * s
            # Step 2: Return the calculated result


        w = calculate_w(compressive_strength, area, s_d)
        w_u = calculate_w(cs_u, area_u, s_u)

        print("The default value of W is " + str(w))
        print("The user defined value of W is " + str(w_u))

    def pull(self):
        tensile_strength = 200  # Default value for tensile strength
        area = 10  # Default value for area
        s_d = 10

        # Step 2: Get the user input for the parameter
        s_u = float(input("Enter the value for 's' (thickness reduction/strain): "))
        area_u = float(input("Enter the value for 'a' (area): "))
        ts_u = float(input("Enter the value for 'c' (tensile strength): "))

        def calculate_w(ts, a, s):
            # Step 1: Perform the calculation W = compressive_strength * area * s
            return ts * a * s
            # Step 2: Return the calculated result

        w = calculate_w(tensile_strength, area, s_d)
        wp_u = calculate_w(ts_u, area_u, s_u)

        print("The default value of W is " + str(w))
        print("The user defined value of W is " + str(wp_u))


class Lop:

    def __init__(self, num_stages):
        self.num_stages = num_stages
        self.pipe_lengths = []
        self.inner_diameters = []
        self.friction_factors = []
        self.local_resistance_factors = []
        self.valve_areas = []
        self.flow_coefficients = []
        self.num_valves = []
        self.oil_density = None
        self.flow_rates = []
        self.slider_displacements = []
        self.stage_times = []
        self.piston_areas = []

    #Leakage loss due to the lubricating oil

    def para(self):
        b = float(input("Enter the width of the gap (b): "))
        delta = float(input("Enter the height of the gap (clearance, δ): "))
        delta_p = float(input("Enter the pressure difference (Δp): "))
        mu = float(input("Enter the dynamic viscosity of oil (μ): "))
        l = float(input("Enter the length of the gap (L): "))
        v = float(input("Enter the velocity (v): "))

        self.calculate_oil_leak(b, delta, delta_p, mu, l, v)

    # Function to calculate oil leak using the given formula
    def calculate_oil_leak(self, b, delta, delta_p, mu, l, v):
        # First part of the equation: (b * delta^3 * delta_p) / (12 * mu * L)
        term1 = (b * delta ** 3 * delta_p) / (12 * mu * l)

        # Second part of the equation: (b * delta * v) / 2
        term2 = (b * delta * v) / 2

        # Oil leak rate (q)
        q = term1 - term2

        # Print the result
        print(f"The oil leak rate is: {q:.6f}")

        #Leaking power loss
        p = delta_p * q

        # Print the result
        print(f"The power loss due to leaking oil is: {p:.6f}")

        #Pressure loss in the Hydraulic pressure

    def hp_para(self):
        self.oil_density = float(input("Enter the oil density (kg/m^3): "))
        for j in range(self.num_stages):
            print(f"Enter data for stage {j + 1}:")
            self.pipe_lengths.append(float(input(f"Pipe length (L) for stage {j + 1} (m): ")))
            self.inner_diameters.append(float(input(f"Inner diameter (d) for stage {j + 1} (m): ")))
            self.friction_factors.append(float(input(f"Friction loss factor (λ) for stage {j + 1}: ")))
            self.local_resistance_factors.append(float(input(f"Local resistance factor (ζ) for stage {j + 1}: ")))
            self.num_valves.append(int(input(f"Number of valves (b_j) for stage {j + 1}: ")))
            self.valve_areas.append(float(input(f"Valve area (A_0) for stage {j + 1} (m^2): ")))
            self.flow_coefficients.append(float(input(f"Flow coefficient (C_d) for stage {j + 1}: ")))
            self.piston_areas.append(float(input(f"Piston area (A_j) for stage {j + 1} (m^2): ")))
            self.slider_displacements.append(float(input(f"Slider displacement (l_j) for stage {j + 1} (m): ")))
            self.stage_times.append(float(input(f"Time for stage (t_j) for stage {j + 1} (s): ")))

    def calculate_flow_rate(self, j):
        # Calculate the flow rate q_j for stage j
        return self.piston_areas[j] * self.slider_displacements[j] / self.stage_times[j]

    def calculate_velocity(self, j, q_j):
        # Calculate the average flow velocity v_j for stage j
        A_pipe = 3.14159 * (self.inner_diameters[j] / 2) ** 2  # Cross-sectional area of the pipe
        return q_j / A_pipe

    def calculate_piping_loss(self, j, v_j):
        # Calculate the pressure loss in the piping components Δp for stage j
        friction_loss = (self.friction_factors[j] * self.pipe_lengths[j] * self.oil_density * v_j ** 2) / (
                    2 * self.inner_diameters[j])
        local_resistance_loss = (self.local_resistance_factors[j] * self.oil_density * v_j ** 2) / 2
        return friction_loss + local_resistance_loss

    def calculate_valve_loss(self, j, q_j):
        # Calculate the pressure loss in the valve components Δp for stage j
        return (self.oil_density / 2) * (q_j / (self.flow_coefficients[j] * self.valve_areas[j])) ** 2

    def calculate_pressure_loss(self):
        total_loss = 0
        for j in range(self.num_stages):
            # Step 1: Calculate the flow rate q_j for stage j
            q_j = self.calculate_flow_rate(j)

            # Step 2: Calculate the average velocity v_j for stage j
            v_j = self.calculate_velocity(j, q_j)

            # Step 3: Calculate the piping loss Δp for stage j
            piping_loss = self.calculate_piping_loss(j, v_j)

            # Step 4: Calculate the valve loss Δp for stage j
            valve_loss = self.calculate_valve_loss(j, q_j)

            # Step 5: Sum the total loss for stage j
            total_loss += piping_loss + self.num_valves[j] * valve_loss

        return total_loss

if __name__ == "__main__":
    ppm = Ppm("forming", "curing")
    ppm.display_process()
    # Create an instance of BasicOperation class
    basic_op = Bop("press", "pull")
    basic_op.display_process_1()
    # Call the press method to calculate W and print it
    basic_op.press()
    basic_op.pull()

    num_stages = int(input("Enter the number of stages in the hydraulic circuit: "))
    lop = Lop(num_stages)
    lop.para()
    lop.hp_para()
    total_pressure_loss = lop.calculate_pressure_loss()
    print(f"Total Pressure Loss in the Hydraulic Circuit: {total_pressure_loss:.2f} Pa")






