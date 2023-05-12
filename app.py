from flask import Flask, request, redirect, url_for, render_template
import requests


API_KEY = '56d477db50b10f25c5f021ced27ea6a3'


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def cidade():
    if request.method == 'POST':
        nome_cidade = request.form['cidade']
        return redirect(url_for('info_cidade', nome_cidade=nome_cidade))
    return render_template('cidade.html')


@app.route('/<nome_cidade>')
def info_cidade(nome_cidade):
    rqts = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={nome_cidade}&appid={API_KEY}&lang=pt_br&units=metric')
    if 'main' in rqts.json():
        temperatura = rqts.json()['main']['temp']
        sensacao_termica = rqts.json()['main']['feels_like']
        umidade = rqts.json()['main']['humidity']
        vento = rqts.json()['wind']['speed']
        descricao = rqts.json()['weather'][0]['description']
        return render_template('cidade.html',
                               cidade=nome_cidade,
                               temperatura=temperatura,
                               sensacao_termica=sensacao_termica,
                               umidade=umidade,
                               vento=vento,
                               descricao=descricao)
    else:
        return render_template('cidade.html', cidade=nome_cidade, erro='Cidade não encontrada.')


if __name__ == '__main__':
    app.run()
