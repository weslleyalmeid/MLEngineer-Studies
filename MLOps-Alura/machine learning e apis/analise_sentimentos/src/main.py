from flask import Flask
from textblob import TextBlob

app = Flask('meu_app')

@app.route('/')
def home():
    return "Minha primeira API."

@app.route('/sentimento/<string:frase>')
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt_br', to='en')
    polaridade = tb_en.sentiment.polarity
    return f'<h1>polaridade: {polaridade}</h1>'


app.run(debug=True)