from argparse import ArgumentParser
from preprocessor import Preprocessor
from seq2seq import Seq2Seq
from trainer import Trainer


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def main(args):
    data_preprocessor = Preprocessor(train_mode=True, dataset_file_path=args.dataset_path)

    config = {
        'query_vocab_size': len(data_preprocessor.query_field.vocab),
        'program_vocab_size': len(data_preprocessor.program_field.vocab),
        'embedding_dim': 256,
        'num_heads': 8,
        'num_encoder_layers': 3,
        'num_decoder_layers': 3,
        'dropout': 0.0,
        'max_len': 60,
        'forward_expansion': 6,
        'query_pad_idx': data_preprocessor.query_field.vocab.stoi['<pad>']
    }
    model = Seq2Seq(config)
    print(model)
    print(f'The model has {count_parameters(model):,} trainable parameters')

    trainer = Trainer(model=model,
                      train_data=data_preprocessor.data,
                      data_preprocessor=data_preprocessor,
                      num_of_epochs=args.num_of_epochs,
                      model_save_path='models/model_1.pt')

    trainer.train()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--dataset_path', default='dataset/q2p_new_1.csv')
    parser.add_argument('--num_of_epochs', default=20)
    args = parser.parse_args()
    main(args)
