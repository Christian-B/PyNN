"""
Definition of NativeCellType class for NEST.

:copyright: Copyright 2006-2013 by the PyNN team, see AUTHORS.
:license: CeCILL, see LICENSE for details.
"""

import nest
from pyNN.models import BaseCellType

def get_defaults(model_name):
    defaults = nest.GetDefaults(model_name)
    variables = defaults.get('recordables', [])
    ignore = ['archiver_length', 'available', 'capacity', 'elementsize',
              'frozen', 'instantiations', 'local', 'model', 'recordables',
              'state', 't_spike', 'tau_minus', 'tau_minus_triplet',
              'thread', 'vp', 'receptor_types', 'events', 'type_id']
    default_params = {}
    default_initial_values = {}
    for name,value in defaults.items():
        if name in variables:
            default_initial_values[name] = value
        elif name not in ignore:
            default_params[name] = value
    return default_params, default_initial_values

def get_receptor_types(model_name):
    return nest.GetDefaults(model_name).get("receptor_types", ('excitatory', 'inhibitory'))

def get_recordables(model_name):
    return nest.GetDefaults(model_name).get("recordables", [])

def native_cell_type(model_name):
    """
    Return a new NativeCellType subclass.
    """
    assert isinstance(model_name, str)
    default_parameters, default_initial_values = get_defaults(model_name)
    receptor_types = get_receptor_types(model_name)
    recordable = get_recordables(model_name) + ['spikes']
    return type(model_name,
                (NativeCellType,),
                {'nest_model': model_name,
                 'default_parameters': default_parameters,
                 'receptor_types': receptor_types,
                 'injectable': ("V_m" in default_initial_values),
                 'recordable': recordable,
                 'standard_receptor_type': (receptor_types == ('excitatory', 'inhibitory')),
                 'nest_name': {"on_grid": model_name, "off_grid": model_name},
                 'conductance_based': ("g" in (s[0] for s in recordable)),
                 })


class NativeCellType(BaseCellType):

    def get_receptor_type(self, name):
        return nest.GetDefaults(self.nest_model)["receptor_types"][name]
