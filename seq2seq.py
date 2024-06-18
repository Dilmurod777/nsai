from torch import nn
import torch


class Seq2Seq(nn.Module):
    def __init__(self, config, device=None):
        super(Seq2Seq, self).__init__()
        self.src_pad_idx = config['query_pad_idx']

        self.src_word_embedding = nn.Embedding(config['query_vocab_size'], config['embedding_dim'])
        self.trg_word_embedding = nn.Embedding(config['program_vocab_size'], config['embedding_dim'])

        self.src_position_embedding = nn.Embedding(config['max_len'], config['embedding_dim'])
        self.trg_position_embedding = nn.Embedding(config['max_len'], config['embedding_dim'])

        self.transformer = nn.Transformer(config['embedding_dim'],
                                          config['num_heads'],
                                          config['num_encoder_layers'],
                                          config['num_decoder_layers'],
                                          config['forward_expansion'],
                                          config['dropout'])

        self.fc_out = nn.Linear(config['embedding_dim'], config['program_vocab_size'])
        self.dropout = nn.Dropout(config['dropout'])

        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.device = device
        self.to(device)

    def make_src_mask(self, src):
        src_mask = src.transpose(0, 1) == self.src_pad_idx
        return src_mask.to(self.device)

    def forward(self, src, trg):
        src_seq_length, N = src.shape
        trg_seq_length, N = trg.shape

        src_positions = torch.arange(0, src_seq_length).unsqueeze(1).expand(src_seq_length, N).to(self.device)
        trg_positions = torch.arange(0, trg_seq_length).unsqueeze(1).expand(trg_seq_length, N).to(self.device)

        src_embeds = self.dropout(
            (self.src_word_embedding(src) + self.src_position_embedding(src_positions))
        )
        trg_embeds = self.dropout(
            (self.trg_word_embedding(trg) + self.trg_position_embedding(trg_positions))
        )

        src_padding_mask = self.make_src_mask(src)
        trg_mask = self.transformer.generate_square_subsequent_mask(trg_seq_length).to(self.device)

        out = self.transformer(src_embeds,
                               trg_embeds,
                               src_key_padding_mask=src_padding_mask,
                               tgt_mask=trg_mask)

        out = self.fc_out(out)
        return out
