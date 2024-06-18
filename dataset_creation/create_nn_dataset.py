from make_dataset_meta import get_query_metas
from sklearn.model_selection import train_test_split
import os
import json
import csv
import re


def write_query_metas(query_metas, folder):
    for i, query_meta in enumerate(query_metas):
        query_meta_path = os.path.join(folder, '{0:06}'.format(i) + '.json')

        json_object = json.dumps(query_meta)
        with open(query_meta_path, 'w') as outfile:
            outfile.write(json_object)


def make_csv_dataset(query_metas, file_path):
    queries_dict = {}
    for i, query_meta in enumerate(query_metas):
        programs_text = ' <nxt> '.join(query_meta['programs'])
        query_text = query_meta['query']

        query_text = replace_ID(query_text)
        query_text = replace_numbers(query_text)

        queries_dict[query_text] = programs_text

        if '4<number>' in query_text:
            print(query_meta)
    #         replace numbers 8 48


    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['query_text', 'program_text'])

        for key, item in queries_dict.items():
            csv_writer.writerow([key, item])




def replace_ID(txt):
    ids = re.findall(r'[\d-]+', txt)
    for id in ids:
        if id.count('-') != 4:
            continue
        txt = txt.replace(id, '<node_id>')
    return txt


def replace_numbers(txt):
    # numbers = re.findall(r"\d+\.\d+|\d+", txt)
    # for number in numbers:
    #     txt = txt.replace(number, '<number>')
    txt = txt.split(' ')
    for i in range(len(txt)):
        if txt[i].isdigit():
            txt[i] = '<number>'
    return ' '.join(txt)



def main():

    all_queries = get_query_metas()
    train_queries, test_queries, _, _ = train_test_split(all_queries, all_queries,
                                                         test_size=0.1155, random_state=42)

    print('Train: ', len(train_queries))
    print('Test: ', len(test_queries))

    dataset_folder_path = '../dataset_of_queries/v1'
    all_queries_folder = os.path.join(dataset_folder_path, 'all_queries')
    train_queries_folder = os.path.join(dataset_folder_path, 'train_queries')
    test_queries_folder = os.path.join(dataset_folder_path, 'test_queries')

    write_query_metas(all_queries, all_queries_folder)
    write_query_metas(train_queries, train_queries_folder)
    write_query_metas(test_queries, test_queries_folder)

    all_queries_csv = os.path.join(dataset_folder_path, 'all_queries.csv')
    train_queries_csv = os.path.join(dataset_folder_path, 'train_queries.csv')
    test_queries_csv = os.path.join(dataset_folder_path, 'test_queries.csv')

    make_csv_dataset(all_queries, all_queries_csv)
    make_csv_dataset(train_queries, train_queries_csv)
    make_csv_dataset(test_queries, test_queries_csv)




    # 1. get all queries metas
    # 2. split by test (11.55%) and train

    # 3. save all queries to their folders
    # 4. get queries and convert numbers, ID to symbols
    # 5. save csv files (all, test, train)

    pass


if __name__ == '__main__':
    main()