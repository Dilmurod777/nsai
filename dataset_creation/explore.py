import json


def read_knowledge(root_path):
    with open(root_path, 'r') as f:
        data = json.load(f)
    return data


def get_contexts():
    root_file_path = '../data/root 5 tasks.json'
    data = read_knowledge(root_file_path)

    tasks = data[0]['tasks']
    t, s, i, a = 0, 0, 0, 0
    t = len(tasks)

    context_template = {
        'current_task_id': '',
        'current_subtask_id': '',
        'current_instruction_order': ''
    }

    contexts = {
        'manuals': [context_template],
        'tasks': [],
        'subtasks': [],
        'instructions': [],
        'actions': [],
        'detach': [],
        'attach': [],
        'figures': []
    }

    for task in tasks:
        sample_context = context_template.copy()
        sample_context['current_task_id'] = task['task_id']

        if 'subtasks' in task:
            subtasks = task['subtasks']
            s += len(subtasks)

            for subtask in subtasks:
                sample_context = sample_context.copy()
                sample_context['current_subtask_id'] = subtask['subtask_id']

                if 'instructions' in subtask:
                    instructions = subtask['instructions']
                    i += len(instructions)

                    for instruction in instructions:
                        sample_context = sample_context.copy()
                        sample_context['current_instruction_order'] = instruction['order']

                        if 'actions' in instruction:
                            actions = instruction['actions']
                            a += len(actions)
                            sample_context = sample_context.copy()
                            contexts['actions'].append(sample_context)

                            for action in actions:
                                if "detach" in action:
                                    sample_context = sample_context.copy()
                                    contexts['detach'].append(sample_context)
                                elif "attach" in action:
                                    sample_context = sample_context.copy()
                                    contexts['attach'].append(sample_context)
                                break

                        contexts['instructions'].append(sample_context)

                if 'figure' in subtask:
                    figure_context = sample_context.copy()
                    # figure_context['current_instruction_order'] = '1'
                    contexts['figures'].append(figure_context)

                contexts['subtasks'].append(sample_context)
        contexts['tasks'].append(sample_context)

    # print('Tasks: ', t, 'Subtasks: ', s, 'Instructions: ', i, 'Actions: ', a)
    #
    # print(len(contexts['tasks']), len(contexts['subtasks']), len(contexts['instructions']))
    #
    # print(*contexts['tasks'], sep='\n')

    return contexts


def main():
    context = get_contexts()
    print(len(context['actions']), len(context['detach']), len(context['attach']))


if __name__ == '__main__':
    main()