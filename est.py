# Step 1: Define the main class - Primary Processes Modules


class Ppm:
    def __init__(self, forming, curing):
        self.ppm_1 = forming # Initialize with the name of the processes
        self.ppm_2 = curing
        
    def display_process(self):
        print(f"The Primary Process modules used in the transformation are: {self.ppm_1} and {self.ppm_2}") # Step 1: Two main ppm


class BasicOperation(Ppm):

    # Step 5: Constructor for the child class
    def __init__(self, press, pull):
        self.bop_1 = press  # Initialize with the name of the processes
        self.bop_2 = pull

    def display_process(self):
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
            w = compressive_strength * area * s
            # Step 2: Return the calculated result
            return w


        w = self.calculate_w(compressive_strength, area, s_d)
        w = self.calculate_w(cs_u, area_u, s_u)

        # Step 4: Return the calculated result
        return w

# Example usage of the BasicOperation class and press method
if __name__ == "__main__":

    ppm = Ppm()
    # Create an instance of BasicOperation class
    basic_op = BasicOperation()

    # Call the press method to calculate W and print it
    output_press = basic_op.press()

    # Make sure to print the result
    print(f"The calculated value of W is: {output_press}")
     