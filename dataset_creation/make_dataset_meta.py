import json
from nodes import get_root_node
import re
from explore import get_contexts
from executor import Executor


params_dict = {
    'instruction': ['order', 'content'],
    'subtask': ['subtask_id', 'content', 'figure'],
    'task': ['task_id', 'title']
}

items_id_dict = {
    'instruction': 'order',
    'subtask': 'subtask_id',
    'task': 'task_id'
}

node_params_dict = {
    'instruction': ['actions'],
    'subtask': ['instructions'],
    'task': ['general', 'references', 'tools_equipment', 'zones', 'preparation', 'figures', 'subtasks'],
    'manual': ['tasks']
}

request_styling_dict = {
    'general': 'general notes',
    'tools_equipment': 'tools',
    'preparation': 'preparation steps'
}

items_relation_dict = {
    'instruction': ['subtask', 'task', 'manual'],
    'subtask': ['task', 'manual'],
    'task': ['manual'],
    'manual': []
}

items_relation_for_ids_dict = {
    'instruction': ['subtask', 'task'],
    'subtask': ['task']
}


def make_programs_format(programs):
    programs = ' <nxt> '.join(programs)
    return programs


def func_001(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    data_item_code = '<instruction subtask task>'
    param_code = '<param>'

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            for param in params_dict[node]:
                request = meta_text.replace(param_code, param).replace(data_item_code, node)
                meta_programs = questions_meta['programs'][node]
                meta_programs = make_programs_format(meta_programs)
                programs = meta_programs.replace(param_code, param)

                all_requests.append(request)
                all_programs.append(programs)
                all_context_nodes.append(node)
    return all_requests, all_programs, all_context_nodes


def func_002(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    data_item_code = '<subtask task>'
    data_item_id_code = '<subtask_id task_id>'
    param_code = '<param>'

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            for param in params_dict[node]:
                request = meta_text.replace(param_code, param)
                request = request.replace(data_item_code, node)
                request = request.replace(data_item_id_code, '<' + items_id_dict[node] + '>')

                meta_programs = questions_meta['programs'][node]
                meta_programs = make_programs_format(meta_programs)
                programs = meta_programs.replace(param_code, param)

                all_requests.append(request)
                all_programs.append(programs)
                all_context_nodes.append(node)
    return all_requests, all_programs, all_context_nodes


def func_003(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    data_item_code = '<instruction subtask task manual>'
    param_code = '<node_param>'

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            for param in node_params_dict[node]:
                request_param = param
                if param in request_styling_dict.keys():
                    request_param = request_styling_dict[param]

                request = meta_text.replace(param_code, request_param)
                request = request.replace(data_item_code, node)

                meta_programs = questions_meta['programs'][node]
                meta_programs = make_programs_format(meta_programs)
                programs = meta_programs.replace(param_code, param)

                all_requests.append(request)
                all_programs.append(programs)
                all_context_nodes.append(node)

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            for param in node_params_dict[node]:
                request_param = param
                if param in request_styling_dict.keys():
                    request_param = request_styling_dict[param]

                for parent_item in items_relation_dict[node]:
                    request = meta_text.replace(param_code, request_param)
                    request = request.replace(data_item_code, parent_item)

                    meta_programs = questions_meta['param_relational_programs'][node][parent_item]
                    meta_programs = make_programs_format(meta_programs)
                    programs = meta_programs.replace(param_code, param)

                    all_requests.append(request)
                    all_programs.append(programs)
                    all_context_nodes.append(node)

    return all_requests, all_programs, all_context_nodes


def func_004(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    data_item_code = '<subtask task>'
    data_item_id_code = '<subtask_id task_id>'
    param_code = '<node_param>'

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            for param in node_params_dict[node]:
                request_param = param
                if param in request_styling_dict.keys():
                    request_param = request_styling_dict[param]

                request = meta_text.replace(param_code, request_param)
                request = request.replace(data_item_code, node)
                request = request.replace(data_item_id_code, '<' + items_id_dict[node] + '>')

                meta_programs = questions_meta['programs'][node]
                meta_programs = make_programs_format(meta_programs)
                programs = meta_programs.replace(param_code, param)

                # print(request, '|', programs)

                all_requests.append(request)
                all_programs.append(programs)
                all_context_nodes.append(node)

    for meta_text in questions_meta['text']:
        for node in ['instruction', 'subtask']:
            for param in node_params_dict[node]:
                for parent_node in items_relation_for_ids_dict[node]:

                    request = meta_text.replace(param_code, param)
                    request = request.replace(data_item_code, parent_node)
                    request = request.replace(data_item_id_code, '<' + items_id_dict[parent_node] + '>')

                    meta_programs = questions_meta['param_relational_programs'][node][parent_node]
                    meta_programs = make_programs_format(meta_programs)
                    programs = meta_programs.replace(param_code, param)

                    # print(request, '|', programs)

                    all_requests.append(request)
                    all_programs.append(programs)
                    all_context_nodes.append(node)

    return all_requests, all_programs, all_context_nodes


def func_005(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    data_item_code = '<instruction subtask task manual>'
    param_code = '<node_param>'

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            for param in node_params_dict[node]:
                request_param = param
                if param in request_styling_dict.keys():
                    request_param = request_styling_dict[param]

                request = meta_text.replace(param_code, request_param)
                request = request.replace(data_item_code, node)

                meta_programs = questions_meta['programs'][node]
                meta_programs = make_programs_format(meta_programs)
                programs = meta_programs.replace(param_code, param)

                all_requests.append(request)
                all_programs.append(programs)
                all_context_nodes.append(node)

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            for param in node_params_dict[node]:
                request_param = param
                if param in request_styling_dict.keys():
                    request_param = request_styling_dict[param]

                for parent_item in items_relation_dict[node]:
                    request = meta_text.replace(param_code, request_param)
                    request = request.replace(data_item_code, parent_item)

                    meta_programs = questions_meta['param_relational_programs'][node][parent_item]
                    meta_programs = make_programs_format(meta_programs)
                    programs = meta_programs.replace(param_code, param)

                    all_requests.append(request)
                    all_programs.append(programs)
                    all_context_nodes.append(node)

    return all_requests, all_programs, all_context_nodes


def func_006(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    data_item_code = '<subtask task>'
    data_item_id_code = '<subtask_id task_id>'
    param_code = '<node_param>'

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            for param in node_params_dict[node]:
                request_param = param
                if param in request_styling_dict.keys():
                    request_param = request_styling_dict[param]

                request = meta_text.replace(param_code, request_param)
                request = request.replace(data_item_code, node)
                request = request.replace(data_item_id_code, '<' + items_id_dict[node] + '>')

                meta_programs = questions_meta['programs'][node]
                meta_programs = make_programs_format(meta_programs)
                programs = meta_programs.replace(param_code, param)

                # print(request, '|', programs)

                all_requests.append(request)
                all_programs.append(programs)
                all_context_nodes.append(node)

    for meta_text in questions_meta['text']:
        for node in ['instruction', 'subtask']:
            for param in node_params_dict[node]:
                for parent_node in items_relation_for_ids_dict[node]:

                    request = meta_text.replace(param_code, param)
                    request = request.replace(data_item_code, parent_node)
                    request = request.replace(data_item_id_code, '<' + items_id_dict[parent_node] + '>')

                    meta_programs = questions_meta['param_relational_programs'][node][parent_node]
                    meta_programs = make_programs_format(meta_programs)
                    programs = meta_programs.replace(param_code, param)

                    # print(request, '|', programs)

                    all_requests.append(request)
                    all_programs.append(programs)
                    all_context_nodes.append(node)

    return all_requests, all_programs, all_context_nodes


def func_007(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    data_item_code = '<instruction subtask task>'

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            request = meta_text
            request = request.replace(data_item_code, node)

            meta_programs = questions_meta['programs'][node]
            programs = make_programs_format(meta_programs)

            # print(request, '|', programs)
            all_requests.append(request)
            all_programs.append(programs)
            all_context_nodes.append(node)

    return all_requests, all_programs, all_context_nodes


def func_008(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    data_item_code = '<instruction subtask task>'

    for meta_text in questions_meta['text']:
        for node in re.sub('[<>]', '', data_item_code).split(' '):
            request = meta_text
            request = request.replace(data_item_code, node)

            meta_programs = questions_meta['programs'][node]
            programs = make_programs_format(meta_programs)

            # print(request, '|', programs)
            all_requests.append(request)
            all_programs.append(programs)
            all_context_nodes.append(node)

    return all_requests, all_programs, all_context_nodes


def func_009(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []

    for meta_text in questions_meta['text']:
        request = meta_text

        meta_programs = questions_meta['programs']
        programs = make_programs_format(meta_programs)

        all_requests.append(request)
        all_programs.append(programs)
        all_context_nodes.append('detach')

    return all_requests, all_programs, all_context_nodes


def func_010(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []

    for meta_text in questions_meta['text']:
        request = meta_text

        meta_programs = questions_meta['programs']
        programs = make_programs_format(meta_programs)

        all_requests.append(request)
        all_programs.append(programs)
        all_context_nodes.append('attach')

    return all_requests, all_programs, all_context_nodes


def func_011(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []
    param_code = '<param>'
    figure_sides = [
        'left',
        'right',
        'top',
        'bottom',
        'front',
        'bottom'
    ]

    for meta_text in questions_meta['text']:
        for side in figure_sides:
            request = meta_text.replace(param_code, side)
            meta_programs = questions_meta['programs']
            meta_programs = make_programs_format(meta_programs)
            programs = meta_programs.replace(param_code, side)

            all_requests.append(request)
            all_programs.append(programs)
            all_context_nodes.append('figures')

    return all_requests, all_programs, all_context_nodes


def func_012(questions_meta):
    all_requests, all_programs, all_context_nodes = [], [], []

    for meta_text in questions_meta['text']:
        request = meta_text

        meta_programs = questions_meta['programs']
        programs = make_programs_format(meta_programs)

        all_requests.append(request)
        all_programs.append(programs)
        all_context_nodes.append('figures')

    return all_requests, all_programs, all_context_nodes




def qm_001(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []
    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node + 's']:
            query_meta = make_query(programs=program, query=request, context=query_context)

            reply = executor.execute(query_meta)

            query_meta['reply'] = reply
            query_metas.append(query_meta)

    return query_metas


def qm_002(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []
    access_dict = {
        'subtask': ['<subtask_id>', 'current_subtask_id'],
        'task': ['<task_id>', 'current_task_id']
    }

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node + 's']:
            request = request.replace(access_dict[context_node][0], query_context[access_dict[context_node][1]])

            query_meta = make_query(programs=program, query=request, context=query_context)

            reply = executor.execute(query_meta)

            query_meta['reply'] = reply
            query_metas.append(query_meta)

    return query_metas


def qm_003(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        if 'of this manual' in request:
            context_node = 'manual'

        for query_context in available_contexts[context_node + 's']:

            query_meta = make_query(programs=program, query=request, context=query_context)

            reply = executor.execute(query_meta)
            query_meta['reply'] = reply
            query_metas.append(query_meta)

    return query_metas


def qm_004(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []
    access_dict = {
        'subtask': ['<subtask_id>', 'current_subtask_id'],
        'task': ['<task_id>', 'current_task_id']
    }

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]


        if '<subtask_id>' in request:
            context_node = 'subtask'
        elif '<task_id>' in request:
            context_node = 'task'

        for query_context in available_contexts[context_node + 's']:

            request = request.replace(access_dict[context_node][0], query_context[access_dict[context_node][1]])

            query_meta = make_query(programs=program, query=request, context=query_context)

            reply = executor.execute(query_meta)
            query_meta['reply'] = reply
            query_metas.append(query_meta)

    return query_metas


def qm_005(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]



        if 'this manual' in request:
            context_node = 'manual'


        for query_context in available_contexts[context_node + 's']:

            query_meta = make_query(programs=program, query=request, context=query_context)
            reply = executor.execute(query_meta)
            query_meta['reply'] = reply
            query_metas.append(query_meta)

    return query_metas


def qm_006(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []
    access_dict = {
        'subtask': ['<subtask_id>', 'current_subtask_id'],
        'task': ['<task_id>', 'current_task_id']
    }

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        if 'this manual' in request:
            context_node = 'manual'

        if '<subtask_id>' in request:
            context_node = 'subtask'
        elif '<task_id>' in request:
            context_node = 'task'

        for query_context in available_contexts[context_node + 's']:

            request = request.replace(access_dict[context_node][0], query_context[access_dict[context_node][1]])

            query_meta = make_query(programs=program, query=request, context=query_context)

            reply = executor.execute(query_meta)
            query_meta['reply'] = reply
            query_metas.append(query_meta)

    return query_metas


def qm_007(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node + 's']:

            query_meta = make_query(programs=program, query=request, context=query_context)

            reply = executor.execute(query_meta)
            query_meta['reply'] = reply
            query_metas.append(query_meta)

            # print(request, '|', program, '|', query_context, '|', reply)

    return query_metas


def qm_008(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node + 's']:

            query_meta = make_query(programs=program, query=request, context=query_context)

            reply = executor.execute(query_meta)
            query_meta['reply'] = reply
            query_metas.append(query_meta)

            # print(request, '|', program, '|', query_context, '|', reply)

    return query_metas


def qm_009(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node]:

            temp_q = make_query(programs=[
                "FilterType tasks root",
                "FilterType subtasks prev",
                "FilterAttr subtask_id current_subtask_id prev",
                "FilterType instructions prev",
                "FilterAttr order current_instruction_order prev",
                "FilterType actions prev",
            ], query='', context=query_context)
            actions = executor.execute(temp_q)

            if len(actions) == 1:
                request = all_requests[i]
                request = request.replace('<number1>', actions[0]['detach'][0])
                request = request.replace('<number2>', actions[0]['detach'][1])

                query_meta = make_query(programs=program, query=request, context=query_context)

                reply = executor.execute(query_meta)

                if 'Please check validity of your request' in reply:
                    continue

                query_meta['reply'] = reply
                query_metas.append(query_meta)

                # print(request, '|', query_context, '|', reply)

            elif len(actions) > 1:
                number1 = ''
                for action in actions:
                    number1 += action['detach'][0] + ' '
                number1 = number1.strip()
                number2 = actions[0]['detach'][1]

                request = all_requests[i]
                request = request.replace('<number1>', number1)
                request = request.replace('<number2>', number2)

                query_meta = make_query(programs=program, query=request, context=query_context)

                reply = executor.execute(query_meta)

                if 'Please check validity of your request' in reply:
                    continue

                query_meta['reply'] = reply
                query_metas.append(query_meta)

            else:
                print('Shit!', len(actions))

    return query_metas


def qm_010(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node]:

            temp_q = make_query(programs=[
                "FilterType tasks root",
                "FilterType subtasks prev",
                "FilterAttr subtask_id current_subtask_id prev",
                "FilterType instructions prev",
                "FilterAttr order current_instruction_order prev",
                "FilterType actions prev",
            ], query='', context=query_context)
            actions = executor.execute(temp_q)

            if len(actions) == 1:
                request = all_requests[i]
                request = request.replace('<number1>', actions[0]['attach'][0])
                request = request.replace('<number2>', actions[0]['attach'][1])

                query_meta = make_query(programs=program, query=request, context=query_context)

                reply = executor.execute(query_meta)

                if 'Please check validity of your request' in reply:
                    continue

                query_meta['reply'] = reply
                query_metas.append(query_meta)

                # print(request, '|', query_context, '|', reply)

            elif len(actions) > 1:
                number1 = ''
                for action in actions:
                    number1 += action['attach'][0] + ' '
                number1 = number1.strip()
                number2 = actions[0]['attach'][1]

                request = all_requests[i]
                request = request.replace('<number1>', number1)
                request = request.replace('<number2>', number2)

                query_meta = make_query(programs=program, query=request, context=query_context)

                reply = executor.execute(query_meta)

                if 'Please check validity of your request' in reply:
                    continue

                query_meta['reply'] = reply
                query_metas.append(query_meta)

            else:
                print('Shit!', len(actions))

    return query_metas


def qm_011(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node]:

            query_meta = make_query(programs=program, query=request, context=query_context)
            # print('-->', request, '|', query_context)
            reply = executor.execute(query_meta)
            query_meta['reply'] = reply
            query_metas.append(query_meta)

            # print(request, '|', program, '|', query_context, '|', reply)

    return query_metas


def qm_012(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node]:

            temp_q = make_query(programs=[
                "FilterType tasks root",
                "FilterAttr task_id current_task_id prev",
                "FilterType figures prev",
                "SaveVal2Var prev var_1",
                
                "FilterType tasks root",
                "FilterType subtasks prev",
                "FilterAttr subtask_id current_subtask_id prev",
                "Unique prev",
                "QueryAttr figure prev",
                "FilterAttr title prev val_1",
            ], query='', context=query_context)
            figure = executor.execute(temp_q)

            if len(figure) == 0:
                continue

            figure = figure[0]['figure_items']
            items = []
            keys = list(figure.keys())
            for i in range(3):
                item = ' '.join(keys[:i + 1])
                items.append(item)

            for item in items:
                request = all_requests[i]
                request = request.replace('<number>', item)

                query_meta = make_query(programs=program, query=request, context=query_context)
                reply = executor.execute(query_meta)

                query_meta['reply'] = reply
                query_metas.append(query_meta)

                # print(request, '|', query_context, '|', reply)
    return query_metas


def qm_017(all_requests, all_programs, all_context_nodes, available_contexts, executor):
    query_metas = []

    for i in range(len(all_requests)):
        request = all_requests[i]
        program = all_programs[i]
        program = program.split(' <nxt> ')
        context_node = all_context_nodes[i]

        for query_context in available_contexts[context_node]:
            for ratio in ['2', '3', '4']:

                request = all_requests[i]
                request = request.replace('<ratio>', ratio)

                # print(request, '|', query_context)

                query_meta = make_query(programs=program, query=request, context=query_context)
                reply = executor.execute(query_meta)

                query_meta['reply'] = reply
                query_metas.append(query_meta)

                # print(request, '|', query_context, '|', reply)
    return query_metas


def make_query(programs, query, context):
    query_meta = {
        'query': query,
        'programs': programs,
        'context': context
    }
    return query_meta


def get_query_metas():
    questions_meta = 'questions_meta.json'
    available_contexts = get_contexts()

    root_file_path = '../data/root 5 tasks.json'
    executor = Executor(root_path=root_file_path)

    functions_dict = {
        '001': func_001,
        '002': func_002,
        '003': func_003,
        '004': func_004,
        '005': func_005,
        '006': func_006,
        '007': func_007,
        '008': func_008,
        '009': func_009,
        '010': func_010,
        '011': func_011,
        '012': func_012,
        '013': func_012,
        '014': func_012,
        '015': func_012,
        '016': func_012,
        '017': func_012,
        '018': func_012,
        '019': func_012,
        '020': func_012
    }
    query_meta_dict = {
        '001': qm_001,
        '002': qm_002,
        '003': qm_003,
        '004': qm_004,
        '005': qm_005,
        '006': qm_006,
        '007': qm_007,
        '008': qm_008,
        '009': qm_009,
        '010': qm_010,
        '011': qm_011,
        '012': qm_012,
        '013': qm_012,
        '014': qm_012,
        '015': qm_012,
        '016': qm_012,
        '017': qm_017,
        '018': qm_017,
        '019': qm_011,
        '020': qm_011
    }
    with open(questions_meta, 'r') as f:
        data = json.load(f)

    all_requests, all_programs, all_context_nodes, all_query_metas = [], [], [], []
    for item in data:

        questions_meta = item
        question_id = item['id']
        if int(question_id) not in range(21):
            continue
        requests, programs, context_nodes = functions_dict[question_id](questions_meta)
        query_metas = query_meta_dict[question_id](requests, programs, context_nodes, available_contexts, executor)

        all_requests.extend(requests)
        all_programs.extend(programs)
        all_context_nodes.extend(context_nodes)
        all_query_metas.extend(query_metas)

    # print(len(all_requests), len(all_programs), len(all_context_nodes), len(all_query_metas))

    print(len(all_query_metas))
    # print(all_query_metas)
    return all_query_metas

def main():
    pass

if __name__ == '__main__':
    main()