from dataset_creation.executor import Executor


def main():
    root_file_path = 'data/root 5 tasks.json'
    executor = Executor(root_path=root_file_path)

    query_meta = {
        'query': 'Detach 42, 43 from 46',
        'programs': [
            'ExtractNumbers Query',
            'CreateActions detach Yes prev',
            'SaveVal2Var prev var_1',
            'FilterType tasks root',
            'FilterType subtasks prev',
            'FilterAttr subtask_id current_subtask_id prev',
            'FilterType instructions prev',
            'FilterAttr order current_instruction_order prev',
            'FilterType actions prev',
            'CheckActionsValidity val_1 prev',
            'Detach prev val_1'
        ],
        'context': {
            'current_task_id': '32-11-61-000-802',
            'current_subtask_id': '32-11-61-020-007',
            'current_instruction_order': '1'
        }
    }

    result = executor.execute(query_meta)
    print(result)


if __name__ == '__main__':
    main()
