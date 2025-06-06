import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

#coeficiente: quanto a x influencia no consumo
#intercepto: valor de energia consumida quando a temperatura é zero, após escalonamento
psv = pd.read_csv('baseEnergia.csv')

encoder_dia = LabelEncoder()
encoder_tipo = LabelEncoder()
psv['dia_semana'] = encoder_dia.fit_transform(psv['dia_semana'])
psv['tipo_construção'] = encoder_tipo.fit_transform(psv['tipo_construção'])

x1=psv.tipo_construção   ##residencial é por exemplo um prédio com vários apartamentos de residencia
x2=psv.área
x3=psv.número_ocupantes
x4=psv.aparelhos
x5=psv.temperatura_média
x6=psv.dia_semana
y=psv.energia_consumida

xall=psv.drop(['energia_consumida'],axis=1)  ##esse une todas as variáveis, excluindo o y


#Regressão com 1 variável
def predicao(x,nome_coluna):  #esse (x) é o que o código espera que nós passemos de valor quando a função for chamada. nesse caso é x1... que passa pra análise1 que passa para ela.
      x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
      reg= LinearRegression().fit(x_train.values.reshape(-1,1),y_train)
      print(f"\nCorrelação entre {nome_coluna} e energia_consumida:")
      print(psv[[nome_coluna, 'energia_consumida']].corr())
      print("Coeficiente: ", reg.coef_) #quanto maior o coeficiente, mais ele influência
      print("Intercepto:  ", reg.intercept_)
      y_pred =reg.predict(x_test.values.reshape(-1,1))
      print("\n.............. ...  ..................")
      mae(y_test,y_pred)
      return x_test, y_test, y_pred  # Retorna as variáveis

#regressão múltipla
def predicaoM(x):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    reg= LinearRegression().fit(x_train,y_train)
    print(psv[xall.columns.tolist() + ['energia_consumida']].corr()['energia_consumida'])
    print("Coeficiente: ", reg.coef_) #quanto maior o coeficiente, mais ele influência
    print("Intercepto:  ", reg.intercept_)
    y_pred =reg.predict(x_test)
    print("\n.............. ...  ..................")
    mae(y_test,y_pred)
    return x_test, y_test, y_pred, reg # Retorna as variáveis


def mae(y_test,y_pred):  # não precisa colocar mae aqui pq ela já tá em predicao()
      mae= mean_absolute_error(y_test,y_pred)
      print("erro MAE",mae)
      erro_percentual = (mae / y_test.mean()) * 100
      print(f"Erro percentual médio: {erro_percentual:.2f}%")
      if(erro_percentual<20):
       print("Erro aceitável")
      else:
          print("Erro grave")

def grafico_dispersao(x, y, x_test,y_test, y_pred, titulo, xlabel, ylabel):
# vendo se preveu bem
    fig, ax = plt.subplots()
    ax.scatter(y_pred, y_test)
    ax.plot([min(y_test), max(y_test)], [min(y_pred), max(y_pred)], '--r')
    ax.set_xlabel("Consumo previsto")
    ax.set_ylabel("Consumo original")
    ax.set_title(titulo)
    plt.show()
# gráfico de análise 
    plt.scatter(x, y, color='blue', label='Dados reais')
    plt.plot(x_test, y_pred, color='red', label='Regressão Linear') #linha de regressão. tendencia de y subir com x
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"Influência de {xlabel} no {ylabel}")
    plt.legend()
    plt.show()
# Funções de análise
def analise1(x):
    print("Construção x Consumo")
    x_test, y_test, y_pred = predicao(x,"tipo_construção")
    df = pd.DataFrame({'Tipo de Construção': x_test.values, 'Consumo Original': y_test, 'Consumo Previsto': y_pred})
    grupo = df.groupby('Tipo de Construção').mean()
    
    fig, ax = plt.subplots()
    indice = np.arange(len(grupo))
    width = 0.4
    plt.bar(indice - width/2, grupo['Consumo Original'], width, label='Consumo Original')
    plt.bar(indice + width/2, grupo['Consumo Previsto'], width, label='Consumo Previsto', alpha=0.7)
    plt.xticks(indice, grupo.index)
    plt.xlabel("Tipo de Construção")
    plt.ylabel("Consumo Médio de Energia")
    plt.title("Construção X Consumo\n(0: Residencial, 1: Comercial, 2: Industrial)")

    plt.legend()
    plt.show()

def analise5(x):
    x_test, y_test, y_pred = predicao(x, 'temperatura_média')
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train.values.reshape(-1,1))
    x_test_scaled = scaler.transform(x_test.values.reshape(-1,1))
    reg = LinearRegression().fit(x_train_scaled, y_train)
    y_pred = reg.predict(x_test_scaled)
    print("Coeficiente: ", reg.coef_)
    print("Intercepto: ", reg.intercept_)
    y_pred=reg.predict(x_test.values.reshape(-1,1))
    print("\n.............. ...  ..................")
    print("Erro absoluto",mean_absolute_error(y_test,y_pred)) 
    print(psv[['temperatura_média', 'energia_consumida']].corr())  #mostra a força de relação entre temperatura e consumo. bom só a partir de 0.4
    #na tabela mostrada, sempre será 1 quando (x,y) for a mesma variável (temperatura,temperatura)
    ## vendo se preveu x5 bem
    fig,ax=plt.subplots()
    ax.scatter(y_pred,y_test)
    ax.plot([3000,4600],[3000,4600],'--r')
    ax.set_title("Temperatura média x Energia consumida")
    ax.set_xlabel("Consumo previsto")
    ax.set_ylabel("Consumo original")
    plt.show()
    print("\n     ")
    #Gráfico de análise
    plt.scatter(x, y, color='blue', label='Dados reais')  # Pontos reais
    plt.plot(x_test, y_pred, color='red', label='Regressão Linear')  # Linha da regressão - Tendencia de y subir com x
    ##ele usa os x de testes e exibe os y de predição
    plt.xlabel("temperatura média")
    plt.ylabel("Consumo de energia")
    plt.title("Influência da temperatura no consumo de energia")
    plt.legend() ##Mostra as legendas estabelecidas
    plt.show()

def analise6(x):
    print("Dia da Semana x Consumo")
    x_test, y_test, y_pred = predicao(x, 'dia_semana')
    df = pd.DataFrame({'Dia da Semana': x_test.values, 'Consumo Original': y_test, 'Consumo Previsto': y_pred})
    grupo = df.groupby('Dia da Semana').mean()
    
    fig, ax = plt.subplots()
    indice = np.arange(len(grupo))
    width = 0.4
    plt.bar(indice - width/2, grupo['Consumo Original'], width, label='Consumo Original', alpha=0.7)
    plt.bar(indice + width/2, grupo['Consumo Previsto'], width, label='Consumo Previsto', alpha=0.7)
    plt.xticks(indice, grupo.index)
    plt.xlabel("Semana/Final de semana")
    plt.ylabel("Consumo Médio de Energia")
    plt.title("Comparação entre Consumo Previsto e Original por dia da semana")
    plt.legend()
    plt.show()

def analise_comum(x, nome_coluna, titulo, xlabel, ylabel): #2,3,4,5
    print(titulo)
    x_test, y_test, y_pred= predicao(x, nome_coluna)
    grafico_dispersao(x, y, x_test,y_test, y_pred, titulo, xlabel, ylabel)  


def analiseM(x):
    x_test, y_test, y_pred,reg = predicaoM(x)

    # Pegando os valores de 'aparelhos' correspondentes aos índices de x_test
    tc_test = psv.loc[x_test.index, 'tipo_construção']

    # Gráfico de dispersão com coloração por número de aparelhos
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(y_test, y_pred, c=tc_test, cmap='viridis', alpha=0.7)
    cbar = plt.colorbar(scatter)
    cbar.set_label('Tipo de construção')

    # Linha ideal (y = x)
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], '--r')

    ax.set_xlabel("Consumo original")
    ax.set_ylabel("Consumo previsto")
    ax.set_title("Análise Geral - Cor por tipo de construção")
    plt.tight_layout()
    plt.show()

def entrada(x):
    x_test, y_test, y_pred,reg =predicaoM(xall)
    tc = int(input("Digite o tipo de construção:\n 0-Residencial, 1-Comercial, 2-Industrial "))  # Entrada do usuário
    area = float(input("Digite o valor da área: "))  # Entrada do usuário
    no = int(input("Digite quantas pessoas ocupam o local: "))  # Entrada do usuário
    ap= int(input("Digite a quantidade de aparelhos do local: "))
    tm = float(input("Digite a temperatura média do local: "))  # Entrada do usuário
    ds=int(input("Digite o dia da semana:\n 0- Dia da semana, 1-final de semana "))
    consumo_prev = reg.predict([[tc,area,no,ap,tm,ds]])
    print(f"\n Consumo previsto: {consumo_prev[0]:.2f} kWh")


# Chamando análises
entrada(xall)
analiseM(xall)
analise1(x1)
analise_comum(x2, 'área', "Área x Consumo", "Área", "Consumo de Energia")
analise_comum(x3, 'número_ocupantes', "Ocupantes x Consumo", "Número de Ocupantes", "Consumo de Energia")
analise_comum(x4, 'aparelhos', "Aparelhos x Consumo", "Quantidade de Aparelhos", "Consumo de Energia")
analise_comum(x5,'temperatura_média', "Temperatura Média x Consumo", "Temperatura Média", "Consumo de Energia")
analise6(x6)

#ele provavelmente segmentou por número de aparelhos pq é um desvio padrão pequeno

