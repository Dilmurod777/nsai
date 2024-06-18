from flask import Flask, request, jsonify
from preprocessor import Preprocessor
from semantic_parser import SemanticParser

app = Flask(__name__)

preprocessor = Preprocessor(train_mode=False,
                            query_field_vocab_path='dataset/vocabs/query_field_vocab.txt',
                            program_field_vocab_path='dataset/vocabs/program_field_vocab.txt')

semantic_parser = SemanticParser(data_preprocessor=preprocessor,
                                 model_path='models/model_1.pt',
                                 max_length=60)


@app.route('/predict', methods=['POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        programs = semantic_parser.predict(query)
        response = {
            'programs': programs
        }
    else:
        response = 'this is POST method'
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
