import numpy as np
import json
from scipy import constants
from pint import UnitRegistry, Quantity
import os

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
            'parameter_list': {
                'Parameter': 'Here all parameters and a description should be entered',
            }
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
                {'name': 'T_ambient', 'description': 'Ambient temperature (°C)', 'default_value': 25, 'dtype': 'float', 'mandatory': False},
                {'name': 'T_sky', 'description': 'Sky temperature (in °C). If unknown, the ambient temperature is used.', 'default_value': None, 'dtype': 'float | None', 'mandatory': False},
                {'name': 'epsilon', 'description': 'Emission factor for thermal radiation (float between 0.0 and 1.0)', 'default_value': 0.1, 'dtype': 'float', 'mandatory': False},
                {'name': 'eta_el', 'description': 'Efficiency of heating elements (float between 0.0 and 1.0)', 'default_value': 0.7, 'dtype': 'float', 'mandatory': False},
            ],
        }
        return cls_info
    
    def _parse_params(self, params) -> None:
        self.params = params
        # Parse from input_data if needed (already loaded)
        
        self.params = {
            'press_compressive_strength': input_data['parameters'].get('press_compressive_strength', {}).get('value', 335),
            'press_area': input_data['parameters'].get('press_area', {}).get('value', 2410335.18),
            'press_s': input_data['parameters'].get('press_s', {}).get('value', 78),
            'pull_tensile_strength': input_data['parameters'].get('pull_tensile_strength', {}).get('value', 200),
            'pull_area': input_data['parameters'].get('pull_area', {}).get('value', 500),
            'pull_s': input_data['parameters'].get('pull_s', {}).get('value', 0.655),
        }
    def press(self):

        compressive_strength = self.Q_(self._get_param('press_compressive_strength')['value'], 'Pa')
        press_area = self.Q_(self._get_param('press_area')['value'], 'm**2')
        s_d = self.Q_(self._get_param('press_s_d')['value'], 'm')

        w = compressive_strength * press_area * s_d
        w_in_kwh = w.to('kWh')
        print(f"The calculated work for the press process is: {w_in_kwh}")
        return w_in_kwh

    def pull(self):
        tensile_strength = self.Q_(self._get_param('pull_tensile_strength'), 'Pa')
        pull_area = self.Q_(self._get_param('pull_area'), 'm**2')
        s_d = self.Q_(self._get_param('pull_s_d'), 'm')

        w = tensile_strength * pull_area * s_d
        w_in_kwh = w.to('kWh')
        print(f"The calculated work for the pull process is: {w_in_kwh}")
        return w_in_kwh



 



