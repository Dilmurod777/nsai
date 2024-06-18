from tqdm import tqdm
from torch.optim import Adam, lr_scheduler
from torch import nn
from torchtext.data import BucketIterator
import torch


class Trainer:
    def __init__(self, model, train_data, data_preprocessor, device=None, num_of_epochs=20, batch_size=8, lr=3e-4,
                 model_save_path='models/model.pt'):
        self.train_data = train_data
        self.model = model
        self.data_preprocessor = data_preprocessor

        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.device = device

        self.query_pad_idx = self.data_preprocessor.query_field.vocab.stoi['<pad>']
        self.learning_rate = lr
        self.num_of_epochs = num_of_epochs
        self.batch_size = batch_size

        self.optimizer = Adam(self.model.parameters(), lr=self.learning_rate)
        self.scheduler = lr_scheduler.ReduceLROnPlateau(self.optimizer, factor=0.1, patience=10, verbose=True)
        self.criterion = nn.CrossEntropyLoss(ignore_index=self.query_pad_idx)

        self.train_data_loader = self.create_data_loader()
        self.model_save_path = model_save_path

    def create_data_loader(self):
        train_data_loader = BucketIterator.splits((self.train_data,),
                                                  batch_size=self.batch_size,
                                                  sort_within_batch=True,
                                                  sort_key=lambda x: len(x.query),
                                                  device=self.device)[0]
        return train_data_loader

    def train(self):
        self.model.train()

        for epoch in range(self.num_of_epochs):
            pbar = tqdm(desc='Epoch {}'.format(epoch + 1))
            losses = []

            for i, batch in enumerate(self.train_data_loader):
                # Get the inputs and targets
                inp_seq, target = batch.query, batch.program

                # Forward pass
                output = self.model(inp_seq, target[:-1, :])

                # Reshape the output and targets for criterion
                output = output.reshape(-1, output.shape[2])  # (trg_seq_len * N, trg_vocab_size)
                target = target[1:].reshape(-1)

                self.optimizer.zero_grad()

                # Calculate Loss
                loss = self.criterion(output, target)
                losses.append(loss.item())

                # Backprop and Optimize
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1)
                self.optimizer.step()

                # Metrics
                pbar.update(1)
                pbar.set_postfix({'Loss': loss.item()})

            mean_loss = sum(losses) / len(losses)
            self.scheduler.step(mean_loss)

            print(f'Epoch {epoch + 1}: Mean Loss = {mean_loss}\n')
            pbar.close()

        # Save Model
        torch.save(self.model, self.model_save_path)
        print(f'Model saved to {self.model_save_path}')
        # torch.save(self.state_dict(), filename)
