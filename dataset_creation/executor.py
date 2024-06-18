from catalog import GeneralCatalog, KnowledgeCatalog, Actions3DCatalog
import json


class Executor(GeneralCatalog, KnowledgeCatalog, Actions3DCatalog):
    def __init__(self, root_path):
        self.root_path = root_path
        self.root = self.read_knowledge()
        self.root3D = [
            {
                'name': '402-32-11-61-990-802-A'
            },
            {
                'name': '402-32-11-61-990-802-B'
            },
            {
                'name': '402-32-11-61-990-802-C'
            },
            {
                'name': '401-32-45-11-990-801-A'
            },
            {
                'name': '401-32-45-11-990-801-B'
            },
            {
                'name': '401-32-45-11-990-801-C'
            }
        ]
        self.generic_attributes = {'None': None, 'False': False, 'True': True}

    def set_runtime_parameters(self, query_meta):
        self.Query = query_meta['query']
        self.prev = None
        self.val_1 = None
        self.val_2 = None
        self.val_3 = None

        self.current_task_id = query_meta['context']['current_task_id']
        self.current_subtask_id = query_meta['context']['current_subtask_id']
        self.current_instruction_order = query_meta['context']['current_instruction_order']

    def read_knowledge(self):
        with open(self.root_path, 'r') as f:
            data = json.load(f)
        return data

    def SaveVal2Var(self, value, var_name):
        var2val_dict = {'var_1': 'val_1', 'var_2': 'val_2', 'var_3': 'val_3'}
        setattr(self, var2val_dict[var_name], value)
        return value

    def get_parameters(self, parameters):
        parameter_values = []
        for parameter in parameters:
            if parameter in self.generic_attributes.keys():
                value = self.generic_attributes[parameter]
            elif hasattr(self, parameter):
                value = getattr(self, parameter)
            else:
                value = parameter
            parameter_values.append(value)
        return parameter_values

    def get_function(self, function):
        if hasattr(self, function):
            return getattr(self, function)
        else:
            print(f'No such function {function} in Executor or Catalog class')
            raise f'No such function {function} in Executor or Catalog class'

    def execute(self, query_meta):
        self.set_runtime_parameters(query_meta)
        for program in query_meta['programs']:
            program_components = program.split(' ')
            function_name = program_components[0]
            parameter_names = program_components[1:]

            params = self.get_parameters(parameter_names)
            function = self.get_function(function_name)
            self.prev = function(*params)

        return self.prev


