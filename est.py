# Define the main class - Primary Processes Modules
class Ppm:
    def __init__(self, p1, p2):
        self.ppm_1 = p1 # Initialize with the name of the primary processes
        self.ppm_2 = p2
        
    def display_process(self):
        print(f"The Primary Process modules used in the transformation are {self.ppm_1} and {self.ppm_2}")

# Define class Basic operations
class Bop:

    # Constructor for the class
    def __init__(self, press, pull):
        self.bop_1 = press  # Initialize with the name of the processes
        self.bop_2 = pull

        #super().__init__("forming", "curing")

    def display_process_1(self):
        print(f"The basic operations used in the primary processes are  {self.bop_1} and {self.bop_2}")

    def press(self):
        compressive_strength = 335  # Default value for compressive strength
        area = 2410335.18  # Default value for area
        s_d= 10

        # Step 2: Get the user input for the parameter
        s_u = float(input("Enter the value for 's' (thickness reduction/strain): "))
        area_u = float(input("Enter the value for 'a' (area): "))
        cs_u = float(input("Enter the value for 'c' (compressive strength): "))

        def calculate_w(c, a, s):
            # Step 1: Perform the calculation W = compressive_strength * area * s
            return c * a * s
            # Step 2: Return the calculated result


        w=1
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



if __name__ == "__main__":

    ppm = Ppm("forming","curing")
    ppm.display_process()
    # Create an instance of BasicOperation class
    basic_op = Bop("press","pull")
    basic_op.display_process_1()
    # Call the press method to calculate W and print it
    basic_op.press()
    basic_op.pull()

    lop = Lop()
    lop.para()



     