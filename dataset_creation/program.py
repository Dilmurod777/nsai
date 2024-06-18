class ProgramsCreator:
    def __init__(self, nodes):
        self.nodes = nodes

    def unique_node_query_attr(self, attr):
        programs = [
            ['Unique', 'prev'],
            ['QueryAttr', attr, 'prev']
        ]
        return programs

    def get_all_data_object(self, data_object_type, in_data_object_type=None):
        result = []
        node = self.nodes[data_object_type]
        while node.type != in_data_object_type:
            program = ['FilterType', node.type, node.source]
            result.insert(0, program)
            node = node.parent
            if not node:
                break
        return result

    def get_specific(self, data_object_type, object_id):
        result = []
        node = self.nodes['tasks']

        while node:
            program1 = ['FilterType', node.type, node.source]
            id_attr = object_id if node.type == data_object_type else node.current_id_attr
            id_attr = node.current_id_attr if id_attr == 'this' else id_attr
            program2 = ['FilterAttr', node.id_attr, id_attr, 'prev']

            result.append(program1)
            result.append(program2)

            if node.type == data_object_type:
                break
            else:
                node = node.child
        return result

    def get_specific_type(self, data_object_type):
        node = self.nodes[data_object_type]
        program = ['FilterType', node.type, node.source]
        return [program]

    def extract_create_save(self, action_type, reference_object_specified, var):
        programs = [
            ['ExtractNumbers', 'Query'],
            ['CreateActions', action_type, reference_object_specified, 'prev'],
            ['SaveVal2Var', 'prev', var],
        ]
        return programs

    def validity_and_actions(self, action_type, var):
        programs = [
            ['CheckActionsValidity', var, 'prev'],
            [action_type, 'prev', var],
        ]
        return programs

    def get_figure(self):
        program = self.get_specific('subtasks', 'this')
        program += [
            ['Unique', 'prev'],
            ['QueryAttr', 'figure', 'prev'],
            ['Filter3DAttr', 'name', 'prev', 'root3D'],
            ['Unique', 'prev'],
        ]
        return program

