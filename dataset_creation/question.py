from program import ProgramsCreator

NUMBER = '<NUMBER>'

class Node:
    def __init__(self, type, id_attr, current_id_attr, id_token, source, str_attr, list_attr):
        self.type = type
        self.id_attr = id_attr
        self.current_id_attr = current_id_attr
        self.id_token = id_token
        self.parent = None
        self.child = None
        self.source = source
        self.string_attributes = str_attr
        self.list_attributes = list_attr


def create_nodes():
    task_node = Node('tasks', 'task_id', 'current_task_id', 'this task', 'root', ['task_id', 'title'], ['zones',
                                                                                           # 'general',
                                                                                           # 'preparation',
                                                                                           'subtasks',
                                                                                           'references',
                                                                                           'figures',
                                                                                           'tools_equipment'])
    subtask_node = Node('subtasks', 'subtask_id', 'current_subtask_id', 'this subtask', 'prev', ['subtask_id', 'figure', 'content'], ['instructions',
                                                                                                                      'warnings',
                                                                                                                      'notes',
                                                                                                                      # 'actions',
                                                                                                                      'cautions'])
    instruction_node = Node('instructions', 'order', 'current_instruction_order', 'this instruction', 'prev', ['content', 'order'], ['warnings',
                                                                                                                 'cautions',
                                                                                                                 'actions',
                                                                                                                 'notes'])
    action_node = Node('actions', None, None, None, 'prev', [], [])

    task_node.child = subtask_node
    subtask_node.parent = task_node
    subtask_node.child = instruction_node
    instruction_node.parent = subtask_node
    instruction_node.child = action_node
    action_node.parent = instruction_node

    nodes = {
        'tasks': task_node,
        'subtasks': subtask_node,
        'instructions': instruction_node,
        'actions': action_node
    }
    return nodes


class QuestionsCreator:
    def __init__(self):
        self.nodes = create_nodes()
        self.programs_creator = ProgramsCreator(self.nodes)

        self.show_commands = [
            'show the',
            'display the',
            'demonstrate',
            'illustrate'
            # 'what is the'
        ]
        self.execute_commands = [
            'execute',
            'show execution of',
            'run',
            'run execution of',
            'perform execution of',
            'play execution of',
            'present execution of'
        ]
        self.detach_commands = [
            'detach',
            'remove',
            'disconnect',
            'uninstall',
            'disassemble',
            'isolate',
            'separate'
        ]
        self.attach_commands = [
            'attach',
            'install',
            'connect',
            'put',
            'position',
            'locate',
        ]
        self.number = NUMBER
        self.numbers = [
            [self.number],
            [self.number, self.number],
            [self.number, self.number, self.number]
        ]
        self.figure_sides = [
            'left',
            'right',
            'top',
            'bottom',
            'front',
            'bottom'
        ]
        self.highlight_commands = [
            [
                'show highlight of',
                'highlight',
                'display highlight of',
                'turn on highlight of'
            ],
            [
                'hide highlight from',
                'reset highlight of',
                'turn off highlight of',
                'remove highlight from'
            ]

        ]
        self.close_look_commands = [
            'show close look of',
            'show closer',
            'display close look of',
            'display closer',
            'demonstrate close look of',
            'demonstrate closer',
            'show close view of',
            'view closer',
            'display close view of',
            'demonstrate close view of',
        ]
        self.scale_figure_commands = [
            [
                'scale up',
                'show scale up look',
                'display scale up look',
                'demonstrate scale up look',
                'illustrate scale up look',
                'show scale up view',
                'display scale up view',
                'demonstrate scale up view',
                'illustrate scale up view'
            ],
            [
                'scale down'
                'scale down',
                'show scale down look',
                'display scale down look',
                'demonstrate scale down look',
                'illustrate scale down look',
                'show scale down view',
                'display scale down view',
                'demonstrate scale down view',
                'illustrate scale down view'
            ]
        ]
        self.scale_figure_ratios = [
            ['1.5', '2', '3'],
            ['0.5', '0.25', '0.1']
        ]
        self.side_by_side_commands = [
            'show side by side look',
            'display side by side look',
            'demonstrate side by side look',
            'illustrate side by side look',
            'show side by side view',
            'display side by side view',
            'demonstrate side by side view',
            'illustrate side by side view'
        ]
        self.animate_figure_commands = [
            [
                'animate',
                'explore',
                'play animation of',
            ],
            [
                'stop animating',
                'stop exploring',
                'stop animation of',
            ]
        ]
        self.visibility_commands = [
            [
                'show',
                'make visible',
                'turn on visibility of'
            ],
            [
                'hide',
                'make invisible',
                'turn off visibility of'
            ]
        ]
        self.reset_figure_commands = [
            'reset',
            'reconstruct',
            'set initial position for',
            'set initial look for',
            'set initial view for',
            'reset view for'
        ]

        self.not_understood_commands = [
            '',
            ' '
        ]

    def string_attribute_question(self):
        q2p = []
        for key, node in self.nodes.items():
            for attr in node.string_attributes:
                for command in self.show_commands:
                    question = ' '.join([command, attr, 'of', node.id_token])

                    program = self.programs_creator.get_specific(node.type, 'this')
                    program += self.programs_creator.unique_node_query_attr(attr)
                    program += [['ShowInfo', 'prev']]

                    q2p.append((question, program))
        return q2p

    def show_summary(self):
        q2p = []

        for key, node in self.nodes.items():
            for command in self.show_commands:
                if node.type == 'actions':
                    continue

                question = ' '.join([command, 'summary', 'for', node.id_token])

                program = self.programs_creator.get_specific(node.type, 'this')
                program += [['ShowInfo', 'prev']]

                q2p.append((question, program))
        return q2p

    def execute_node(self):
        q2p = []

        for key, node in self.nodes.items():
            for command in self.execute_commands:
                if node.type in ['tasks', 'actions']:
                    continue

                question = ' '.join([command, node.id_token])
                program = self.programs_creator.get_specific(node.type, 'this')
                if node.type == 'subtasks':
                    program += self.programs_creator.get_specific_type('instructions')

                program += self.programs_creator.get_specific_type('actions')
                program += [['ExecuteType', node.type, 'prev']]

                q2p.append((question, program))
        return q2p

    def detach(self):
        q2p = []
        for command in self.detach_commands:
            for number_type in self.numbers:
                for ref_specified in ['Yes']: # add No
                    if ref_specified == 'Yes':
                        question = ' '.join([command] + number_type + ['from', self.number])
                    else:
                        question = ' '.join([command] + number_type)
                    program = []

                    program += self.programs_creator.extract_create_save('detach', ref_specified, 'var_1')
                    program += self.programs_creator.get_specific('instructions', 'this')
                    program += self.programs_creator.get_specific_type('actions')
                    program += self.programs_creator.validity_and_actions('Detach', 'val_1')

                    q2p.append((question, program))

        return q2p

    def attach(self):
        q2p = []
        for command in self.attach_commands:
            for number_type in self.numbers:
                if len(number_type) > 2:
                    continue
                for ref_specified in ['Yes']: # add No
                    if ref_specified == 'Yes':
                        question = ' '.join([command] + number_type + ['to', self.number])
                    else:
                        question = ' '.join([command] + number_type)
                    program = []

                    program += self.programs_creator.extract_create_save('attach', ref_specified, 'var_1')
                    program += self.programs_creator.get_specific('instructions', 'this')
                    program += self.programs_creator.get_specific_type('actions')
                    program += self.programs_creator.validity_and_actions('Attach', 'val_1')

                    q2p.append((question, program))

        return q2p

    def show_side(self):
        q2p = []

        for show_command in self.show_commands:
            for side in self.figure_sides:
                question = ' '.join([show_command, side, 'side', 'of this figure'])
                program = self.programs_creator.get_figure()
                program += [['ShowSide', side, 'prev']]
                q2p.append((question, program))

        return q2p

    def show_highlight(self):
        q2p = []

        for i, commands in enumerate(self.highlight_commands):
            for command in commands:
                for number in self.numbers:
                    question = ' '.join([command] + number)

                    program = [
                        ['ExtractNumbers', 'Query'],
                        ['SaveVal2Var', 'prev', 'var_1'],
                    ]
                    program += self.programs_creator.get_specific('subtasks', 'this')
                    program += [
                        ['Unique', 'prev'],
                        ['QueryAttr', 'figure', 'prev'],
                        ['Filter3DAttr', 'name', 'prev', 'root3D'],
                        ['Unique', 'prev'],

                        ['Filter3DAttr', 'items', 'val_1', 'prev'],
                    ]
                    program += [['Highlight', 'on' if i == 0 else 'off', 'prev']]

                    q2p.append((question, program))
        return q2p

    def list_attribute_question(self):
        q2p = []
        for key, node in self.nodes.items():
            for attr in node.string_attributes:
                for command in self.show_commands:
                    question = ' '.join([command, attr, 'of', node.id_token])

                    program = self.programs_creator.get_specific(node.type, 'this')
                    program += self.programs_creator.unique_node_query_attr(attr)

                    q2p.append((question, program))
        return q2p

    def close_look_questions(self):
        q2p = []

        for i, command in enumerate(self.close_look_commands):
            for number in self.numbers:
                question = ' '.join([command] + number)

                program = [
                    ['ExtractNumbers', 'Query'],
                    ['SaveVal2Var', 'prev', 'var_1'],
                ]
                program += self.programs_creator.get_specific('subtasks', 'this')
                program += [
                    ['Unique', 'prev'],
                    ['QueryAttr', 'figure', 'prev'],
                    ['Filter3DAttr', 'name', 'prev', 'root3D'],
                    ['Unique', 'prev'],

                    ['Filter3DAttr', 'items', 'val_1', 'prev'],
                    ['CloseLook', 'prev']
                ]
                q2p.append((question, program))
        return q2p

    def scale_figure(self):
        q2p = []

        for i, commands in enumerate(self.scale_figure_commands):
            for command in commands:
                for ratio in self.scale_figure_ratios[i]:
                    question = ' '.join([command, 'this figure by', ratio])

                    program = [
                        ['ExtractNumbers', 'Query'],
                        ['SaveVal2Var', 'prev', 'var_1'],
                    ]

                    program += self.programs_creator.get_figure()
                    program += [['Scale', 'up' if i == 0 else 'down', 'prev', 'val_1']]

                    q2p.append((question, program))
        return q2p

    def side_by_side(self):
        q2p = []

        for i, command in enumerate(self.side_by_side_commands):
            question = ' '.join([command, 'of', 'this figure'])

            program = self.programs_creator.get_figure()
            program += [['SideBySideLook', 'prev']]

            q2p.append((question, program))
        return q2p

    def animate_figure(self):
        q2p = []

        for i, commands in enumerate(self.animate_figure_commands):
            # print(commands)
            for command in commands:

                question = ' '.join([command, 'this figure'])

                program = self.programs_creator.get_figure()
                program += [['Animate', 'on' if i == 0 else 'off', 'prev']]
                q2p.append((question, program))
        return q2p

    def visibility_figure(self):
        q2p = []

        for i, commands in enumerate(self.visibility_commands):
            for command in commands:

                question = ' '.join([command, 'this figure'])
                program = self.programs_creator.get_figure()
                program += [['Visibility', 'on' if i == 0 else 'off', 'prev']]

                q2p.append((question, program))
        return q2p

    def visibility_objects(self):
        q2p = []

        for i, commands in enumerate(self.visibility_commands):
            # print(commands)
            for command in commands:
                for number in self.numbers:

                    question = ' '.join([command] + number)


                    program = [
                        ['ExtractNumbers', 'Query'],
                        ['SaveVal2Var', 'prev', 'var_1'],
                    ]
                    program += self.programs_creator.get_figure()
                    program += [
                        ['Filter3DAttr', 'items', 'val_1', 'prev'],
                    ]

                    program += [['Visibility', 'on' if i == 0 else 'off', 'prev']]
                    q2p.append((question, program))

        return q2p

    def reset_figure(self):
        q2p = []

        for i, command in enumerate(self.reset_figure_commands):
            question = ' '.join([command, 'this figure'])
            program = self.programs_creator.get_figure()
            program += [
                ['Reset', 'prev']
            ]

            q2p.append((question, program))
        return q2p

    def not_understood(self):
        q2p = []

        for i, command in enumerate(self.not_understood_commands):
            question = ' '.join([command])
            program = [
                ['NotUnderstood']
            ]
            q2p.append((question, program))

        for commands in [self.show_commands,
                         self.visibility_commands[0], self.visibility_commands[1],
                         self.execute_commands,
                         self.reset_figure_commands,
                         self.animate_figure_commands[0], self.animate_figure_commands[1],
                         self.side_by_side_commands,
                         self.scale_figure_commands[0], self.scale_figure_commands[1],
                         self.close_look_commands,
                         self.highlight_commands[0], self.highlight_commands[1],
                         self.attach_commands,
                         self.detach_commands]:
            for i, command in enumerate(commands):
                question = ' '.join([command])
                program = [
                    ['NotUnderstood']
                ]
                q2p.append((question, program))
        return q2p








