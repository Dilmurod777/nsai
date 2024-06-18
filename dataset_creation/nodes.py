class Node:
    def __init__(self, name, access_attribute, value_attributes=None, node_attributes=None):
        self.name = name
        self.access_attribute = access_attribute
        self.value_attributes = value_attributes
        self.node_attributes = node_attributes


def get_root_node():

    general_info = Node(name='general information', access_attribute='general')
    reference = Node(name='reference node', access_attribute='references', value_attributes=['reference', 'title'])
    tools_equipment = Node(name='tools and equipment', access_attribute='tools_equipment',
                           value_attributes=['reference', 'description'])
    zone = Node(name='zone item', access_attribute='zones', value_attributes=['zone', 'area'])
    figure = Node(name='figure', access_attribute='figures', value_attributes=['title', 'figure_items'])
    warning = Node(name='warning', access_attribute='warnings', value_attributes=['content'])

    action = Node(name='action', access_attribute='actions')
    instruction = Node(name='instruction', access_attribute='instructions',
                       value_attributes=['order', 'content'], node_attributes=[action])
    subtask = Node(name='subtask', access_attribute='subtasks',
                   value_attributes=['subtask_id', 'content', 'figure'], node_attributes=[instruction, warning])

    preparation = Node(name='preparation subtasks', access_attribute='preparation',
                       value_attributes=[], node_attributes=[subtask])

    task = Node(name='task',
                access_attribute='tasks',
                value_attributes=['task_id', 'title'],
                node_attributes=[general_info, reference, tools_equipment, zone, preparation, figure, subtask])

    root = Node(name='manual', access_attribute='', node_attributes=[task])

    return root


def main():
    parent_node = get_root_node()
    node_attributes = parent_node.node_attributes

    while node_attributes:
        new_node_attributes = []

        for node in node_attributes:
            if node.value_attributes:
                for attr in node.value_attributes:
                    print(attr)

            if node.node_attributes:
                for attr in node.node_attributes:
                    print(attr.access_attribute)

                new_node_attributes.extend(node.node_attributes)
                parent_node = node

        node_attributes = new_node_attributes


if __name__ == '__main__':
    main()

