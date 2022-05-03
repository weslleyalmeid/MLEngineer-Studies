from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle
import os.path
import ipdb

app = Flask('__name__')
app.config['BASIC_AUTH_USERNAME'] = 'weslley'
app.config['BASIC_AUTH_PASSWORD'] = 'almeida'

basic_auth = BasicAuth(app)


ROOT_DIR = os.path.dirname(os.path.abspath( __file__ ))
MODELS_DIR = os.path.join(ROOT_DIR, 'models')

def load_model(path):
    model_path = os.path.join(path, 'model.pkl')
    model = pickle.load(open(model_path, 'rb'))
    return model

@app.route('/')
def home():
    return "Minha primeira API."

@app.route('/sentimento/<string:frase>')
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


app.run(debug=True)