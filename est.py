# Step 1: Define the main class - Primary Processes Modules
class Ppm:
    def __init__(self, p1, p2):
        self.ppm_1 = p1 # Initialize with the name of the processes
        self.ppm_2 = p2
        
    def display_process(self):
        print(f"The Primary Process modules used in the transformation are: {self.ppm_1} and {self.ppm_2}")

# Define child class - Basic operations
class BasicOperation (Ppm):

    # Step 5: Constructor for the child class
    def __init__(self, press, pull):
        self.bop_1 = press  # Initialize with the name of the processes
        self.bop_2 = pull

        super().__init__("forming", "curing")

    def display_process_1(self):
        print(f"The basic operations used in the primary processes are: {self.bop_1} and {self.bop_2}")

    def press(self):
        compressive_strength = 200  # Default value for compressive strength
        area = 10  # Default value for area
        s_d= 10

        # Step 2: Get the user input for the parameter
        s_u = float(input("Enter the value for 's' (thickness reduction/strain): "))
        area_u = float(input("Enter the value for 'a' (area): "))
        cs_u = float(input("Enter the value for 'c' (compressive strength): "))

        def calculate_w(compressive_strength, area, s):
            # Step 1: Perform the calculation W = compressive_strength * area * s
            return compressive_strength * area * s
            # Step 2: Return the calculated result



        w = calculate_w(compressive_strength, area, s_d)
        w_u = calculate_w(cs_u, area_u, s_u)

        print("The default value of W is" + str(w))
        print("The user defined value of W is" + str(w_u))

    def pull(self):
        tensile_strength = 200  # Default value for tensile strength
        area = 10  # Default value for area
        s_d = 10

        # Step 2: Get the user input for the parameter
        s_u = float(input("Enter the value for 's' (thickness reduction/strain): "))
        area_u = float(input("Enter the value for 'a' (area): "))
        ts_u = float(input("Enter the value for 'c' (tensile strength): "))

        def calculate_w(tensile_strength, area, s):
            # Step 1: Perform the calculation W = compressive_strength * area * s
            return tensile_strength * area * s
            # Step 2: Return the calculated result

        w = calculate_w(tensile_strength, area, s_d)
        wp_u = calculate_w(ts_u, area_u, s_u)

    print("The default value of W is" + str(wp))
    print("The user defined value of W is" + str(wp_u))
#test
# Example usage of the BasicOperation class and press method
if __name__ == "__main__":

    ppm = Ppm("forming","curing")
    # Create an instance of BasicOperation class
    basic_op = BasicOperation("press","pull")

    # Call the press method to calculate W and print it
    output_press = basic_op.press()

    output_pull = basic_op.pull()


     