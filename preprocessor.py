import os
from argparse import ArgumentParser
from torchtext.data import Field, TabularDataset
import torch


class Preprocessor:
    def __init__(self, train_mode, dataset_file_path=None, query_field_vocab_path=None, program_field_vocab_path=None):
        self.token_next = '<nxt>'
        self.token_start = '<sos>'
        self.token_end = '<eos>'
        self.max_vocab_size = 100
        self.save_vocab_dir_path = 'dataset/vocabs'

        self.query_field = Field(tokenize=self.tokenizer, use_vocab=True, init_token=self.token_start, eos_token=self.token_end, lower=True)
        self.program_field = Field(tokenize=self.tokenizer, use_vocab=True, init_token=self.token_start, eos_token=self.token_end, lower=False)

        if train_mode:
            self.preprocess_dataset(dataset_file_path)
        else:
            self.set_vocabs(query_field_vocab_path, program_field_vocab_path)

    @staticmethod
    def tokenizer(text):
        text = text.strip()
        tokens = text.split(' ')
        return tokens

    def preprocess_dataset(self, dataset_file_path):
        self.fields = {
            'query_text': ('query', self.query_field),
            'program_text': ('program', self.program_field)
        }
        self.data = TabularDataset.splits(path='./',
                                          train=dataset_file_path,
                                          format='csv',
                                          fields=self.fields)[0]

        self.query_field.build_vocab(self.data, max_size=self.max_vocab_size, min_freq=1)
        self.program_field.build_vocab(self.data, max_size=self.max_vocab_size, min_freq=1, specials=[self.token_next])

        self.save_vocab(self.query_field.vocab, 'query_field_vocab.txt')
        self.save_vocab(self.program_field.vocab, 'program_field_vocab.txt')

    def set_vocabs(self, query_field_vocab_path, program_field_vocab_path):
        # self.query_field.vocab = self.read_vocab(query_field_vocab_path)
        # self.program_field.vocab = self.read_vocab(program_field_vocab_path)

        self.query_field_string_to_index = self.read_vocab(query_field_vocab_path)
        self.program_field_string_to_index = self.read_vocab(program_field_vocab_path)

        self.query_field_index_to_string = self.make_index_to_string(self.query_field_string_to_index)
        self.program_field_index_to_string = self.make_index_to_string(self.program_field_string_to_index)

    @staticmethod
    def make_index_to_string(string_to_index):
        index_to_string = {}
        for string, index in string_to_index.items():
            index_to_string[index] = string
        return index_to_string

    @staticmethod
    def read_vocab(vocab_path):
        vocab = dict()
        with open(vocab_path, 'r') as file:
            for line in file:
                index, token = line.split(',')
                vocab[token.strip()] = int(index)
        return vocab

    def save_vocab(self, vocab, vocab_name):
        save_path = os.path.join(self.save_vocab_dir_path, vocab_name)
        with open(save_path, 'w') as f:
            for token, index in vocab.stoi.items():
                f.write(f'{index},{token}\n')
        print(f'Vocab: {vocab_name} is saved in {save_path}')


def main(args):
    print(torch.__version__)
    # preprocessor = Preprocessor(train_mode=True, dataset_file_path=args.dataset_path)
    # preprocessor = Preprocessor(train_mode=False,
    #                             query_field_vocab_path='dataset/vocabs/query_field_vocab.txt',
    #                             program_field_vocab_path='dataset/vocabs/program_field_vocab.txt')



    # print(preprocessor.query_field.vocab.stoi)
    # print(preprocessor.program_field.vocab.stoi)

    # config = {
    #     "query_vocab_size": 89,
    #     "program_vocab_size": 49,
    #     "embedding_dim": 256,
    #     "num_heads": 8,
    #     "num_encoder_layers": 3,
    #     "num_decoder_layers": 3,
    #     "dropout": 0,
    #     "max_len": 30,
    #     "forward_expansion": 6,
    #     "query_pad_idx": 1
    # }
    #
    # query_indices = [0, 1, 2, 3, 4, 5]
    # query_tensor = torch.LongTensor(query_indices).unsqueeze(1)
    # src_seq_length, N = query_tensor.shape
    # src_positions = torch.arange(0, src_seq_length).unsqueeze(1).expand(src_seq_length, N)
    # src_mask = query_tensor.transpose(0, 1) == 1 #self.src_pad_idx
    # # print(query_tensor.shape, src_positions.shape)
    #
    #
    # outputs = [0, 1, 2, 3, 4]
    # program_tensor = torch.LongTensor(outputs).unsqueeze(1)
    # trg_seq_length, N = program_tensor.shape
    # trg_positions = torch.arange(0, trg_seq_length).unsqueeze(1).expand(trg_seq_length, N)
    # trg_mask = torch.triu(torch.full((trg_seq_length, trg_seq_length), float('-inf')), diagonal=1)
    #
    # seq2seq = Seq2Seq(config)
    # res = seq2seq(query_tensor, query_tensor, src_mask, program_tensor, trg_positions, trg_mask)
    # inputs = ['query_tensor', 'src_positions', 'src_mask', 'program_tensor', 'trg_positions', 'trg_mask']
    # outputs = ['output']
    # dynamic_axes = {'query_tensor': {0: 'dim_1', 1: 'dim_2'},
    #                 'src_positions': {0: 'dim_1', 1: 'dim_2'},
    #                 'src_mask': {0: 'dim_1', 1: 'dim_2'},
    #                 'program_tensor': {0: 'dim_1', 1: 'dim_2'},
    #                 'trg_positions': {0: 'dim_1', 1: 'dim_2'},
    #                 'trg_mask': {0: 'dim_1', 1: 'dim_2'},
    #                 'output': {0: 'dim_1', 1: 'dim_2'}
    #                 }
    #
    #
    # torch.onnx.export(seq2seq,
    #                   (query_tensor, src_positions, src_mask, program_tensor, trg_positions, trg_mask),
    #                   'embeddings_model.onnx',
    #                   input_names=inputs,
    #                   output_names=outputs,
    #                   dynamic_axes=dynamic_axes,
    #                   export_params=True,
    #                   do_constant_folding=True,
    #                   opset_version=13
    #                   )


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--dataset_path", default='dataset/q2p_new.csv')
    args = parser.parse_args()
    main(args)
