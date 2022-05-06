from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle
import os
import ipdb

app = Flask('__name__')
# export BASIC_AUTH_USERNAME=weslley
# export BASIC_AUTH_PASSWORD=almeida
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)



APP_DIR = os.path.dirname(os.path.abspath( __file__ ))
SRC_DIR = os.path.dirname(APP_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)
MODELS_DIR = os.path.join(ROOT_DIR, 'models')

def load_model(path):
    model_path = os.path.join(path, 'model.pkl')
    model = pickle.load(open(model_path, 'rb'))
    return model

@app.route('/')
def home():
    return "Minha primeira API."

@app.route('/sentimento/<string:frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt_br', to='en')
    polaridade = tb_en.sentiment.polarity
    return f'<h1>polaridade: {polaridade}</h1>'

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    colunas = ['tamanho', 'ano', 'garagem']
    dados_input = [dados[col] for col in colunas]
    model = load_model(MODELS_DIR)
    preco = model.predict([dados_input])
    return jsonify(preco=preco[0])


if __name__ == '__main__':
    # para escutar chamada em todos os ambientes docker, cloud e local
    app.run(debug=False, host='0.0.0.0')