from argparse import ArgumentParser
from semantic_parser import SemanticParser
from preprocessor import Preprocessor
from dataset_creation.executor import Executor
from dataset_creation.dataset_creator import make_query


def main(args):
    # preprocessor = Preprocessor(train_mode=False,
    #                             query_field_vocab_path='dataset/vocabs/query_field_vocab.txt',
    #                             program_field_vocab_path='dataset/vocabs/program_field_vocab.txt')
    # semantic_parser = SemanticParser(data_preprocessor=preprocessor,
    #                                  model_path=args.model_path, max_length=60)

    root_file_path = 'data/root 5 tasks.json'
    executor = Executor(root_path=root_file_path)

    query = 'remove 13 14 from 11'

    context = ("32-11-61-000-802", "32-11-61-020-009", "1")

    # program = semantic_parser.predict(query)

    query = 'Remove the nut [42], washer [43] from the bolt [46]'
    program = [
        "FilterType tasks root",
        "FilterType subtasks prev",
        "FilterType instructions prev",
        "FilterAttr order 1 prev",
        "Unique prev",
        "QueryAttr content prev",
        "ShowInfo prev"
      ]

    query_meta = make_query(programs=program, query=query, context=context)
    reply = executor.execute(query_meta)

    print(query, program, context, reply)
    print('-' * 10, 'Reply', '-' * 10)
    print(reply)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--model_path', default='models/model_1.pt')
    args = parser.parse_args()
    main(args)
