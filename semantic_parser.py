import torch
import re

# NUMBER = '<NUMBER>'
NUMBER = '<number>'


class SemanticParser:
    def __init__(self, data_preprocessor, model_path, max_length, device=None):
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.device = device

        self.data_preprocessor = data_preprocessor
        self.max_length = max_length

        # self.model = Seq2Seq(config, device)
        # self.model.load_state_dict(torch.load(filename))

        self.model = torch.load(model_path)
        self.model.eval()

    @staticmethod
    def replace_word_number(txt):
        matches = re.findall(r"(\d+)", txt)
        for m in matches:
            txt = txt.replace(m, NUMBER)
        return txt

    def prep_query(self, query):
        query = self.replace_word_number(query)
        query = query.lower()
        # query = re.sub(r"[^a-zA-Z0-9]+", ' ', query)
        query = query.replace(',', ' ')
        return query


    def predict(self, query):
        query = self.prep_query(query)
        print(query)
        tokens = self.data_preprocessor.tokenizer(query)

        # Add <sos> and <eos> in beginning and end respectively
        tokens.insert(0, self.data_preprocessor.query_field.init_token)
        tokens.append(self.data_preprocessor.query_field.eos_token)

        # Convert the tokenized sequence into integers
        query_indices = [self.data_preprocessor.query_field_string_to_index[tok] for tok in tokens if tok in self.data_preprocessor.query_field_string_to_index.keys()]
        # query_indices = list(filter((self.data_preprocessor.query_field_string_to_index['<unk>']).__ne__, query_indices))

        # Convert to Tensor
        query_tensor = torch.LongTensor(query_indices).unsqueeze(1).to(self.device)

        # Init the program sequence with <sos>
        outputs = [self.data_preprocessor.program_field_string_to_index['<sos>']]

        # Generating the program
        for i in range(self.max_length):

            # Create program output tensor
            program_tensor = torch.LongTensor(outputs).unsqueeze(1).to(self.device)

            # Predict next token
            with torch.no_grad():
                output = self.model(query_tensor, program_tensor)

            # Get the word with the highest probability
            word_idx = output.argmax(2)[-1, :].item()
            # Append to outputs
            outputs.append(word_idx)

            if word_idx == self.data_preprocessor.program_field_string_to_index['<eos>']:
                break

        # print(i, self.max_length)

        # Decode to english
        program = [self.data_preprocessor.program_field_index_to_string[idx] for idx in outputs][1:-1]
        # Convert to list of instructions
        program_text = ' '.join(program).split(' <nxt> ')

        # torch.onnx.export(self.model, tuple([query_tensor, program_tensor]), "model.onnx")
        return program_text
