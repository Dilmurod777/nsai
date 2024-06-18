import os.path
import json
import csv
from executor import Executor
from question import QuestionsCreator
from context import ContextManager
import re


def convert_format(programs):
    result = []
    for program in programs:
        program_string = ' '.join(program)
        result.append(program_string)
    return result


def make_query(programs, query, context):
    query_meta = {
        'query': query,
        'programs': programs,
        'context': {
            'current_task_id': context[0],
            'current_subtask_id': context[1],
            'current_instruction_order': context[2]
        }
    }
    return query_meta


def get_query_metas(q2p2c, executor):
    query_metas = []
    for question, program, context in q2p2c:
        program = convert_format(program)
        query_meta = make_query(programs=program, query=question, context=context)

        reply = executor.execute(query_meta)

        query_meta['reply'] = reply
        query_metas.append(query_meta)

    return query_metas


def write_query_metas(query_metas, folder):
    for i, query_meta in enumerate(query_metas):
        query_meta_path = os.path.join(folder, '{0:04}'.format(i) + '.json')

        json_object = json.dumps(query_meta)
        with open(query_meta_path, 'w') as outfile:
            outfile.write(json_object)


def make_csv_dataset(query_metas, file_path='../dataset/q2p_new.csv'):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['query_text', 'program_text'])
        for i, query_meta in enumerate(query_metas):
            programs_text = ' <nxt> '.join(query_meta['programs'])
            query_text = replace_numbers(query_meta['query'])
            # query_text = query_meta['query']
            csv_writer.writerow([query_text, programs_text])


def replace_numbers(query):
    numbers = re.findall(r"\d+\.\d+|\d+", query)
    numbers += re.findall("MAIN_LANDING_GEAR", query)

    number_replace = '<NUMBER>'
    for number in numbers:
        idx = query.find(number)
        if idx > -1:
            query = ''.join([query[:idx], number_replace, query[idx + len(number):]])
    return query


def main():
    root_file_path = '../data/root 5 tasks.json'
    executor = Executor(root_path=root_file_path)

    questions_creator = QuestionsCreator()
    context_manager = ContextManager()

    q2p2c_all = []

    # q2p = questions_creator.string_attribute_question()
    # q2p2c = context_manager.get_random_context(q2p)
    # q2p2c_all += q2p2c

    q2p = questions_creator.show_summary()
    q2p2c = context_manager.get_random_context(q2p)
    q2p2c_all += q2p2c

    q2p = questions_creator.execute_node()
    q2p2c = context_manager.get_random_context(q2p)
    q2p2c_all += q2p2c

    q2p = questions_creator.detach()
    q2p2c = context_manager.get_random_context(q2p, action='detach')
    q2p2c_all += q2p2c

    q2p = questions_creator.attach()
    q2p2c = context_manager.get_random_context(q2p, action='attach')
    q2p2c_all += q2p2c

    q2p = questions_creator.show_side()
    q2p2c = context_manager.get_random_context(q2p)
    q2p2c_all += q2p2c
    # ____>
    q2p = questions_creator.show_highlight()
    q2p2c = context_manager.get_random_context(q2p, action='highlight')
    q2p2c_all += q2p2c
    # ____>
    q2p = questions_creator.close_look_questions()
    q2p2c = context_manager.get_random_context(q2p, action='close_look')
    q2p2c_all += q2p2c

    q2p = questions_creator.scale_figure()
    q2p2c = context_manager.get_random_context(q2p)
    q2p2c_all += q2p2c

    q2p = questions_creator.side_by_side()
    q2p2c = context_manager.get_random_context(q2p)
    q2p2c_all += q2p2c

    q2p = questions_creator.animate_figure()
    q2p2c = context_manager.get_random_context(q2p)
    q2p2c_all += q2p2c

    q2p = questions_creator.visibility_figure()
    q2p2c = context_manager.get_random_context(q2p)
    q2p2c_all += q2p2c

    q2p = questions_creator.visibility_objects()
    q2p2c = context_manager.get_random_context(q2p, action='visibility')
    q2p2c_all += q2p2c

    q2p = questions_creator.reset_figure()
    q2p2c = context_manager.get_random_context(q2p)
    q2p2c_all += q2p2c

    # q2p = questions_creator.not_understood()
    # q2p2c = context_manager.get_random_context(q2p)
    # q2p2c_all += q2p2c

    query_metas = get_query_metas(q2p2c_all, executor)
    print(len(query_metas))
    write_query_metas(query_metas, folder='../data/q1')
    make_csv_dataset(query_metas, file_path='../dataset/q2p_new_1.csv')


if __name__ == '__main__':
    main()
