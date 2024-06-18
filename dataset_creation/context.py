from executor import Executor
from question import QuestionsCreator, create_nodes
import re
import random


class ContextManager:
    def __init__(self):
        root_file_path = '../data/root 5 tasks.json'
        self.executor = Executor(root_path=root_file_path)
        self.nodes = create_nodes()

        self.question_creator = QuestionsCreator()

    def get_random(self):
        tasks = []
        for data_object in self.executor.root:
            if 'tasks' in data_object.keys():
                tasks += data_object['tasks']

        subtask, instruction = None, None

        while subtask is None or instruction is None:

            task = random.choice(tasks)

            subtasks = task['subtasks']
            subtask = random.choice(subtasks)

            if 'instructions' not in subtask.keys() or 'figure' not in subtask.keys():
                continue

            instructions = subtask['instructions']
            instruction = random.choice(instructions)
        return task['task_id'], subtask['subtask_id'], instruction['order']

    def get_figure_context(self, action, question):
        numbers = [m.start() for m in re.finditer(self.question_creator.number, question)]
        possible_contexts = []

        for data_object in self.executor.root:
            tasks = data_object['tasks']
            for task in tasks:
                subtasks = task['subtasks']
                for subtask in subtasks:
                    if 'instructions' not in subtask.keys() or 'figure' not in subtask.keys():
                        continue
                    instructions = subtask['instructions']
                    for instruction in instructions:
                        if 'actions' not in instruction.keys():
                            continue
                        actions = instruction['actions']

                        figure_items = None
                        for figure in task['figures']:
                            if figure['title'] == subtask['figure']:
                                figure_items = figure['figure_items'].keys()
                                possible_contexts.append(
                                    ((task['task_id'], subtask['subtask_id'], instruction['order']), figure_items))
                                break

        context, figure_items = random.choice(possible_contexts)

        items = random.sample(figure_items, len(numbers))

        for i in range(len(numbers)):
            idx = question.find(self.question_creator.number)
            question = question[:idx] + str(items[i]) + question[idx + len(self.question_creator.number):]

        return question, context

    def get_action_context(self, action, question, all_context=False):
        numbers = [m.start() for m in re.finditer(self.question_creator.number, question)]
        from_or_to_in = 1 if 'from' in question or 'to' in question else 0

        possible_contexts = []

        for data_object in self.executor.root:
            tasks = data_object['tasks']
            for task in tasks:
                subtasks = task['subtasks']
                for subtask in subtasks:
                    if 'instructions' not in subtask.keys():
                        continue
                    instructions = subtask['instructions']
                    for instruction in instructions:
                        if 'actions' not in instruction.keys():
                            continue
                        actions = instruction['actions']

                        if len(actions) >= len(numbers) - from_or_to_in and action in actions[0].keys():
                            possible_contexts.append(((task['task_id'], subtask['subtask_id'], instruction['order']), actions))

        if all_context:
            questions, contexts = [], []
            for possible_context in possible_contexts:
                context, actions = possible_context

                # print(question, context, actions)

                question = self.prep_question_string(question, numbers, from_or_to_in, actions, action)

                questions.append(question)
                contexts.append(context)

            return questions, contexts
        else:
            context, actions = random.choice(possible_contexts)
            question = self.prep_question_string(question, numbers, from_or_to_in, actions, action)
            return question, context


        # for i in range(len(numbers) - from_or_to_in):
        #     idx = question.find(self.question_creator.number)
        #     question = question[:idx] + actions[i][action][0] + question[idx + len(self.question_creator.number):]
        #
        # if from_or_to_in:
        #     idx = question.find(self.question_creator.number)
        #     question = question[:idx] + actions[0][action][1] + question[idx + len(self.question_creator.number):]

        # return question, context

    def prep_question_string(self, question, numbers, from_or_to_in, actions, action):
        for i in range(len(numbers) - from_or_to_in):
            idx = question.find(self.question_creator.number)
            question = question[:idx] + actions[i][action][0] + question[idx + len(self.question_creator.number):]

        if from_or_to_in:
            idx = question.find(self.question_creator.number)
            question = question[:idx] + actions[0][action][1] + question[idx + len(self.question_creator.number):]

        return question

    def get_random_context(self, q2p, action=None, all_context=False):
        q2p2c = []

        for question, program in q2p:
            if action in ['attach', 'detach']:
                question, context = self.get_action_context(action, question, all_context)
            elif action in ['highlight', 'close_look', 'visibility']:
                question, context = self.get_figure_context(action, question)
            else:
                context = self.get_random()

            if all_context:
                for i in range(question):
                    q2p2c.append((question[i], program, context[i]))
            else:
                q2p2c.append((question, program, context))

        return q2p2c

    def get_one_to_all_context(self):
        pass
