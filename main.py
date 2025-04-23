#deixar as rotas no main
from flask import Flask, render_template, request
from flask_migrate import Migrate
from usuario import bp_usuarios
from database import db
#para a previsão
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

#aplicação d flask
app = Flask(__name__)

#INICIANDO CADASTRO DE USUARIO
conexao = "sqlite:///meubanco.sqlite"

app.config['SECRET_KEY'] = 'teste'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao

#evita alerta sobre alterações no banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) #comando para executar 
# flask db init  => cria a pasta migrations
# flask db migrate => detecta mudanças no banco
# flask db upgrade => aplica mudanças no banco

# Criar as tabelas no banco de dados, se ainda não existirem
with app.app_context():
    db.create_all() #cria todas as tabelas definidas no banco de dados

#registrar a blueprint
app.register_blueprint(bp_usuarios, url_prefix='/usuarios') #Corrigi o parâmetro 'url_prefix'

migrate = Migrate(app, db) #associando

#INICIAND A PREVISÃO

# Treinamento do modelo de previsão de energia
psv = pd.read_csv('baseEnergia.csv')

encoder_dia = LabelEncoder()
encoder_tipo = LabelEncoder()
psv['dia_semana'] = encoder_dia.fit_transform(psv['dia_semana'])
psv['tipo_construção'] = encoder_tipo.fit_transform(psv['tipo_construção'])

x = psv.drop(['energia_consumida'], axis=1)
y = psv['energia_consumida']

# Treinar o modelo uma vez na inicialização do app
modelo_regressao = LinearRegression().fit(x, y)

#ABRIR PAGINA DE PREVISÃO
@app.route('/previsao', methods=['GET'])
def previsao():
    return render_template("index_previsao.html")

#ROTA PARA PREVISÃO
@app.route('/prever_consumo', methods=['GET','POST'])
def prever_consumo():
    
    try:
        tipo = int(request.form['tipo_construcao'])
        area = float(request.form['area'])
        ocupantes = int(request.form['ocupantes'])
        aparelhos = int(request.form['aparelhos'])
        temperatura = float(request.form['temperatura'])
        dia = int(request.form['dia_semana'])

        entrada = np.array([[tipo, area, ocupantes, aparelhos, temperatura, dia]])
        consumo_previsto = modelo_regressao.predict(entrada)[0]

        return render_template("index_previsao.html", resultado=f"{consumo_previsto:.2f} kWh")
    except Exception as e:
        return f"Erro ao calcular previsão: {str(e)}"
    

#DEFININDO A PAGINA DE PREVISÃO COMOA PRIMEIRA
@app.route('/', methods=['GET'])
def pagina_inicial():
    return render_template("index_previsao.html")

# Definindo a rota para '/' que aceita tanto GET quanto POST
@app.route('/', methods=['GET','POST'])
def usuario():
    if request.method == 'POST':
        # Processar os dados do formulário, se necessário
        return 'Fomulário POST recebido'
    return render_template("usuario.html")  # Ou qualquer outra página desejada para GET

if __name__ == "__main__":
    app.run(debug=True)


#INICIAND A PREVISÃO

# Treinamento do modelo de previsão de energia
psv = pd.read_csv('baseEnergia.csv')

encoder_dia = LabelEncoder()
encoder_tipo = LabelEncoder()
psv['dia_semana'] = encoder_dia.fit_transform(psv['dia_semana'])
psv['tipo_construção'] = encoder_tipo.fit_transform(psv['tipo_construção'])

x = psv.drop(['energia_consumida'], axis=1)
y = psv['energia_consumida']

# Treinar o modelo uma vez na inicialização do app
modelo_regressao = LinearRegression().fit(x, y)

#ABRIR PAGINA DE PREVISÃO
@app.route('/previsao', methods=['GET'])
def previsao():
    return render_template("index_previsao.html")

