import numpy as np
import json
from scipy import constants
from pint import UnitRegistry, Quantity
import os

# Load input data from the JSON file
with open('input.json', 'r') as input_json:
    input_data = json.load(input_json)

class Process_Operation:
    def __init__(self, params, ureg: UnitRegistry = UnitRegistry(), name: str = None) -> None:
        self.ureg = ureg
        self.Q_ = ureg.Quantity
        
        if not name:
            self.json_file_name = 'input_data.json'
        else:
            self.json_file_name = name + '.json'
        
        self._parse_params(params)

    @staticmethod
    def get_cls_information():
        cls_info = {
            'cls_name': 'Name of the corresponding python-class.',
            'display_name': 'Name that will be visible for the user',
            'description_text': 'Description for the given model',
            'parameter_list': [
                {'name': 'json_file', 'description': '.json-file containing timeseries data', 'default_value': 'input_data.json', 'mandatory': False},
                {'name': 'press_compressive_strength', 'description': '.', 'default_value': 335, 'dtype': 'float', 'mandatory': False},
                {'name': 'press_area', 'description': 'Surface Area of the press (mm^2).', 'default_value': 2410335.18, 'dtype': 'float', 'mandatory': False},
                {'name': 'press_s', 'description': ' ', 'default_value': 78, 'dtype': 'float', 'mandatory': False},
                {'name': 'pull_tensile_strength', 'description': '', 'default_value': 200, 'mandatory': False},
                {'name': 'pull_area', 'description': '', 'default_value': 500, 'dtype': 'float', 'mandatory': False},
                {'name': 'pull_s', 'description': '', 'default_value': 0.655, 'dtype': 'float', 'mandatory': False},

                 # New parameters for oil leak and hydraulic pressure calculation
                {'name': 'gap_b', 'description': 'Gap width (b) in meters for oil leak calculation.', 'default_value': 0.1, 'dtype': 'float', 'mandatory': True},
                {'name': 'delta', 'description': 'Gap height (delta) in meters for oil leak calculation.', 'default_value': 0.001, 'dtype': 'float', 'mandatory': True},
                {'name': 'delta_p', 'description': 'Pressure difference (delta_p) in Pascals.', 'default_value': 100000, 'dtype': 'float', 'mandatory': True},
                {'name': 'mu', 'description': 'Dynamic viscosity (mu) of the oil in Pa.s.', 'default_value': 0.1, 'dtype': 'float', 'mandatory': True},
                {'name': 'l', 'description': 'Length (l) in meters for oil leak calculation.', 'default_value': 1, 'dtype': 'float', 'mandatory': True},
                {'name': 'v', 'description': 'Velocity (v) in meters per second for oil leak calculation.', 'default_value': 0.01, 'dtype': 'float', 'mandatory': True},

            # Parameters for hydraulic pressure (hp_para function)
                {'name': 'num_stages', 'description': 'Number of stages in the hydraulic system.', 'default_value': 3, 'dtype': 'int', 'mandatory': True},
                {'name': 'oil_density', 'description': 'Oil density in kg/m^3.', 'default_value': 850, 'dtype': 'float', 'mandatory': True},
                {'name': 'pipe_lengths', 'description': 'List of pipe lengths (L) in meters for each stage.', 'default_value': [1.0, 1.2, 1.5], 'dtype': 'list', 'mandatory': True},
                {'name': 'inner_diameters', 'description': 'List of inner diameters (d) in meters for each stage.', 'default_value': [0.05, 0.04, 0.03], 'dtype': 'list', 'mandatory': True},
                {'name': 'friction_factors', 'description': 'List of friction loss factors (λ) for each stage.', 'default_value': [0.03, 0.04, 0.05], 'dtype': 'list', 'mandatory': True},
                {'name': 'local_resistance_factors', 'description': 'List of local resistance factors (ζ) for each stage.', 'default_value': [1.5, 1.6, 1.7], 'dtype': 'list', 'mandatory': True},
                {'name': 'num_valves', 'description': 'List of number of valves (b_j) for each stage.', 'default_value': [2, 3, 4], 'dtype': 'list', 'mandatory': True},
                {'name': 'valve_areas', 'description': 'List of valve areas (A_0) in square meters for each stage.', 'default_value': [0.001, 0.002, 0.003], 'dtype': 'list', 'mandatory': True},
                {'name': 'flow_coefficients', 'description': 'List of flow coefficients (C_d) for each stage.', 'default_value': [0.6, 0.7, 0.8], 'dtype': 'list', 'mandatory': True},
                {'name': 'piston_areas', 'description': 'List of piston areas (A_j) in square meters for each stage.', 'default_value': [0.01, 0.02, 0.03], 'dtype': 'list', 'mandatory': True},
                {'name': 'slider_displacements', 'description': 'List of slider displacements (l_j) in meters for each stage.', 'default_value': [0.05, 0.06, 0.07], 'dtype': 'list', 'mandatory': True},
                {'name': 'stage_times', 'description': 'List of stage times (t_j) in seconds for each stage.', 'default_value': [10, 15, 20], 'dtype': 'list', 'mandatory': True},

            # Parameters for press waiting time calculation
                {'name': 't_ins', 'description': 'Time for insertion (t_ins) in seconds.', 'default_value': 5, 'dtype': 'float', 'mandatory': True},
                {'name': 't_close', 'description': 'Time for closing (t_close) in seconds.', 'default_value': 10, 'dtype': 'float', 'mandatory': True},
                {'name': 't_form', 'description': 'Time for forming (t_form) in seconds.', 'default_value': 15, 'dtype': 'float', 'mandatory': True},
                {'name': 't_cur', 'description': 'Time for curing (t_cur) in seconds.', 'default_value': 20, 'dtype': 'float', 'mandatory': True},
                {'name': 't_open', 'description': 'Time for opening (t_open) in seconds.', 'default_value': 10, 'dtype': 'float', 'mandatory': True},
                {'name': 't_take', 'description': 'Time for taking out (t_take) in seconds.', 'default_value': 5, 'dtype': 'float', 'mandatory': True},
            ],
        }
        return cls_info

    def _parse_params(self, params):
        self.params = params

    def _get_param(self, key):
        default_value = [x['default_value'] for x in Process_Operation.get_cls_information()['parameter_list'] if x['name'] == key][0]
        return self.params.get(key, default_value)

    def minimum_energy_demand(self):
        return self.Q_(0.0, 'kWh')

    def loss_energy_demand(self):
        return self.Q_(0.0, 'kWh')

    def assistand_energy_demand(self):
        return self.Q_(0.0, 'kWh')
    
    def total_energy_demand(self):
        return self.minimum_energy_demand() + self.loss_energy_demand() + self.assistand_energy_demand()

class forming_process(Process_Operation):
    def __init__(self, params, ureg: UnitRegistry = UnitRegistry(), name:str=None) -> None:
        super().__init__(params, ureg, name)

    @staticmethod
    def get_cls_information():
        cls_info = {
            'metadata': {
                'cls_name': 'forming_process',
                'display_name': 'Forming process',
                'description_text': 'Basic operation to describe mechanical operations like press and pull',
            },
            'parameter_list': [
                {'name': 'json_file', 'description': '.json-file containing timeseries data', 'default_value': 'input_data.json', 'mandatory': True},
                {'name': 'press_compressive_strength', 'description': '.', 'default_value': 335, 'dtype': 'float', 'mandatory': False},
                {'name': 'press_area', 'description': 'Surface Area of the press (mm^2).', 'default_value': 2410335.18, 'dtype': 'float', 'mandatory': False},
                {'name':'press_s', 'description': ' ', 'default_value': 78, 'dtype': 'float', 'mandatory': False},
                {'name': 'pull_tensile_strength', 'description': '', 'default_value': 200, 'mandatory': False},
                {'name': 'pull_area', 'description': '', 'default_value': 500, 'dtype': 'float', 'mandatory': False},
                {'name': 'pull_s', 'description': '', 'default_value': 0.655, 'dtype': 'float', 'mandatory': False},

            # New parameters for oil leak and hydraulic pressure calculation
                {'name': 'gap_b', 'description': 'Gap width (b) in meters for oil leak calculation.', 'default_value': 0.1, 'dtype': 'float', 'mandatory': True},
                {'name': 'delta', 'description': 'Gap height (delta) in meters for oil leak calculation.', 'default_value': 0.001, 'dtype': 'float', 'mandatory': True},
                {'name': 'delta_p', 'description': 'Pressure difference (delta_p) in Pascals.', 'default_value': 100000, 'dtype': 'float', 'mandatory': True},
                {'name': 'mu', 'description': 'Dynamic viscosity (mu) of the oil in Pa.s.', 'default_value': 0.1, 'dtype': 'float', 'mandatory': True},
                {'name': 'l', 'description': 'Length (l) in meters for oil leak calculation.', 'default_value': 1, 'dtype': 'float', 'mandatory': True},
                {'name': 'v', 'description': 'Velocity (v) in meters per second for oil leak calculation.', 'default_value': 0.01, 'dtype': 'float', 'mandatory': True},

            # Parameters for hydraulic pressure (hp_para function)
                {'name': 'num_stages', 'description': 'Number of stages in the hydraulic system.', 'default_value': 3, 'dtype': 'int', 'mandatory': True},
                {'name': 'oil_density', 'description': 'Oil density in kg/m^3.', 'default_value': 850, 'dtype': 'float', 'mandatory': True},
                {'name': 'pipe_lengths', 'description': 'List of pipe lengths (L) in meters for each stage.', 'default_value': [1.0, 1.2, 1.5], 'dtype': 'list', 'mandatory': True},
                {'name': 'inner_diameters', 'description': 'List of inner diameters (d) in meters for each stage.', 'default_value': [0.05, 0.04, 0.03], 'dtype': 'list', 'mandatory': True},
                {'name': 'friction_factors', 'description': 'List of friction loss factors (λ) for each stage.', 'default_value': [0.03, 0.04, 0.05], 'dtype': 'list', 'mandatory': True},
                {'name': 'local_resistance_factors', 'description': 'List of local resistance factors (ζ) for each stage.', 'default_value': [1.5, 1.6, 1.7], 'dtype': 'list', 'mandatory': True},
                {'name': 'num_valves', 'description': 'List of number of valves (b_j) for each stage.', 'default_value': [2, 3, 4], 'dtype': 'list', 'mandatory': True},
                {'name': 'valve_areas', 'description': 'List of valve areas (A_0) in square meters for each stage.', 'default_value': [0.001, 0.002, 0.003], 'dtype': 'list', 'mandatory': True},
                {'name': 'flow_coefficients', 'description': 'List of flow coefficients (C_d) for each stage.', 'default_value': [0.6, 0.7, 0.8], 'dtype': 'list', 'mandatory': True},
                {'name': 'piston_areas', 'description': 'List of piston areas (A_j) in square meters for each stage.', 'default_value': [0.01, 0.02, 0.03], 'dtype': 'list', 'mandatory': True},
                {'name': 'slider_displacements', 'description': 'List of slider displacements (l_j) in meters for each stage.', 'default_value': [0.05, 0.06, 0.07], 'dtype': 'list', 'mandatory': True},
                {'name': 'stage_times', 'description': 'List of stage times (t_j) in seconds for each stage.', 'default_value': [10, 15, 20], 'dtype': 'list', 'mandatory': True},

            # Parameters for press waiting time calculation
                {'name': 't_ins', 'description': 'Time for insertion (t_ins) in seconds.', 'default_value': 5, 'dtype': 'float', 'mandatory': True},
                {'name': 't_close', 'description': 'Time for closing (t_close) in seconds.', 'default_value': 10, 'dtype': 'float', 'mandatory': True},
                {'name': 't_form', 'description': 'Time for forming (t_form) in seconds.', 'default_value': 15, 'dtype': 'float', 'mandatory': True},
                {'name': 't_cur', 'description': 'Time for curing (t_cur) in seconds.', 'default_value': 20, 'dtype': 'float', 'mandatory': True},
                {'name': 't_open', 'description': 'Time for opening (t_open) in seconds.', 'default_value': 10, 'dtype': 'float', 'mandatory': True},
                {'name': 't_take', 'description': 'Time for taking out (t_take) in seconds.', 'default_value': 5, 'dtype': 'float', 'mandatory': True},
            ]   
        }
        return cls_info
    
    def _parse_params(self, params) -> None:
        self.params = {
            'press_compressive_strength': float(input_data['parameters'].get('press_compressive_strength', {}).get('value', 335)),
            'press_area': float(input_data['parameters'].get('press_area', {}).get('value', 2410335.18)),
            'press_s': float(input_data['parameters'].get('press_s', {}).get('value', 78)),
            'pull_tensile_strength': float(input_data['parameters'].get('pull_tensile_strength', {}).get('value', 200)),
            'pull_area': float(input_data['parameters'].get('pull_area', {}).get('value', 500)),
            'pull_s': float(input_data['parameters'].get('pull_s', {}).get('value', 0.655)), 

        }

    def press(self):
        # Get the parameters for press
        compressive_strength = self.Q_(self._get_param('press_compressive_strength'), 'Pa')
    
        # Convert press_area from mm^2 to m^2
        press_area = self.Q_(self._get_param('press_area'), 'mm**2').to('m**2')
    
        # Displacement (s_d) should be in meters (m)
        s_d = self.Q_(self._get_param('press_s'), 'm')

       
        try:
        # Check the types of the magnitudes
            print(f"Compressive Strength magnitude: {compressive_strength.magnitude}, type: {type(compressive_strength.magnitude)}")
            print(f"Press Area magnitude: {press_area.magnitude}, type: {type(press_area.magnitude)}")
            print(f"Displacement magnitude: {s_d.magnitude}, type: {type(s_d.magnitude)}")

         # Ensure we're using the magnitudes for scalar operations
            w = compressive_strength.magnitude * press_area.magnitude * s_d.magnitude
            print(f"Calculated Work (w): {w}")
        except Exception as e:
            print(f"Error during multiplication: {e}")
        return None

     # Ensure the work is in Joules (J) before converting to kWh
        w_in_joules = w.to('J')
        print(f"Work in Joules: {w_in_joules}")

    # Convert from Joules to kWh
        w_in_kwh = w_in_joules.to('kWh')
        print(f"The calculated work for the press process is: {w_in_kwh}")

        return w_in_kwh


    def pull(self):
        tensile_strength = self.Q_(self._get_param('pull_tensile_strength'), 'Pa')
        pull_area = self.Q_(self._get_param('pull_area'), 'm**2')
        s_d = self.Q_(self._get_param('pull_s'), 'm')

        w = tensile_strength * pull_area * s_d
        w_in_joules = w.to('J')  # Convert to Joules before kWh
        w_in_kwh = w_in_joules.to('kWh')
        print(f"The calculated work for the pull process is: {w_in_kwh}")
        return w_in_kwh
    
    # Oil leak calculations remain the same
    def calculate_oil_leak(self):

        b = self.Q_(self._get_param('gap_b'), 'm')           # Width of the gap (meters)
        delta = self.Q_(self._get_param('delta'), 'm')       # Thickness of the oil film (meters)
        delta_p = self.Q_(self._get_param('delta_p'), 'Pa')  # Pressure difference (Pascal)
        mu = self.Q_(self._get_param('mu'), 'Pa*s')          # Dynamic viscosity of oil (Pa·s)
        l = self.Q_(self._get_param('l'), 'm')               # Length (meters)
        v = self.Q_(self._get_param('v'), 'm/s')             # Speed (meters/second)


        term1 = (b * delta ** 3 * delta_p) / (12 * mu * l)
        term2 = (b * delta * v) / 2
        q = term1 - term2

        print(f"The oil leak rate is: {q:.6f}")
        p = delta_p * q
        print(f"The power loss due to leaking oil is: {p:.6f}")

    # Function to calculate pressure loss (HP parameters are read from JSON)
    def hp_para(self):
        self.num_stages = self._get_param('num_stages')
        self.oil_density = self._get_param('oil_density')

        # Read arrays of values for each stage
        self.pipe_lengths = self._get_param('pipe_lengths')
        self.inner_diameters = self._get_param('inner_diameters')
        self.friction_factors = self._get_param('friction_factors')
        self.local_resistance_factors = self._get_param('local_resistance_factors')
        self.num_valves = self._get_param('num_valves')
        self.valve_areas = self._get_param('valve_areas')
        self.flow_coefficients = self._get_param('flow_coefficients')
        self.piston_areas = self._get_param('piston_areas')
        self.slider_displacements = self._get_param('slider_displacements')
        self.stage_times = self._get_param('stage_times')

    # Calculation functions for flow rate, velocity, pressure loss, etc.
    def calculate_flow_rate(self,j):
        return self.piston_areas[j] * self.slider_displacements[j] / self.stage_times[j]

    def calculate_velocity(self, j, q_j):
        a_pipe = 3.14159 * (self.inner_diameters[j] / 2) ** 2
        return q_j / a_pipe

    def calculate_piping_loss(self, j, v_j):
        friction_loss = (self.friction_factors[j] * self.pipe_lengths[j] * self.oil_density * v_j ** 2) / (2 * self.inner_diameters[j])
        local_resistance_loss = (self.local_resistance_factors[j] * self.oil_density * v_j ** 2) / 2
        return friction_loss + local_resistance_loss

    def calculate_valve_loss(self, j, q_j):
        return (self.oil_density / 2) * (q_j / (self.flow_coefficients[j] * self.valve_areas[j])) ** 2

    def calculate_pressure_loss(self):
        total_loss = 0
        for j in range(self.num_stages):
            q_j = self.calculate_flow_rate(j)
            v_j = self.calculate_velocity(j, q_j)
            piping_loss = self.calculate_piping_loss(j, v_j)
            valve_loss = self.calculate_valve_loss(j, q_j)
            total_loss += piping_loss + self.num_valves[j] * valve_loss

        return total_loss

    # Waiting time calculation for press
    def calculate_press_waiting_time(self):
        t_ins = self._get_param('t_ins')
        t_close = self._get_param('t_close')
        t_form = self._get_param('t_form')
        t_cur = self._get_param('t_cur')
        t_open = self._get_param('t_open')
        t_take = self._get_param('t_take')

        total_waiting_time = (t_ins + t_close + t_form + t_cur + t_open + t_take)
        print(f"Total waiting time: {total_waiting_time}")

        # Calculate energy loss (integration over waiting time if needed)
        energy_loss = simps(self.calculate_pressure_loss(), total_waiting_time)
        print(f"Energy loss due to waiting: {energy_loss:.6f} J")

# Load params and initialize forming_process with parsed input data
params = input_data['parameters']
forming_proc = forming_process(params)

# Call the press and pull functions
forming_proc.press()
forming_proc.pull()

forming_proc.calculate_oil_leak()

forming_proc.hp_para()
forming_proc.calculate_flow_rate()
forming_proc.calculate_velocity()
forming_proc.calculate_piping_loss()
forming_proc.calculate_valve_loss()
forming_proc.calculate_pressure_loss()


 



