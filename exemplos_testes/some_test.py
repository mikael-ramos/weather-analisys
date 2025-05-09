from flask import Flask, jsonify, render_template
import requests  
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, insert,MetaData,Table,Column,Integer,String,REAL,Connection
import sqlite3

'''
Estagio atual: tentando obter o response dos dados para previsão de 5 dias
falta: 
    - exibir na rota
    - armazenar

Pós isso iniciar a manipulaçao destes dados armazenados no banco...

'''


load_dotenv()
API_KEY = os.getenv("API_KEY")


class Dbinfo:
    def __init__(self,dbuser,dbpassword,dbhost,dbtable_name):

        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbhost = dbhost
        self.dbtable_name = dbtable_name


class Api_requi:
    def __init__(self,api_key,data_return,cidade_api,url_api):
        self.api_key = api_key
        self.data_return = data_return
        self.cidade_api = cidade_api
        self.url_api = url_api

 
  
api_outroute = Api_requi(API_KEY,[],"","")
api_outroute.cidade_api = "Sidney" #Nome da cidade pra ser pesquisado diretamente fora do flask
URL = f"http://api.openweathermap.org/data/2.5/weather?q={api_outroute.cidade_api}&appid={API_KEY}&units=metric&lang=pt_br"
response = requests.get(URL)
response.json()
api_outroute.data_return = response.json() #retorna o json
df_datareturn = pd.DataFrame([api_outroute.data_return])
dados_filtrados = []
print(df_datareturn['coord'][0]['lon'])


'''
if api_outroute.cidade_api != "":
    for index, row in df_datareturn.iterrows():
        
        cidade_req = row['name']
        lon = row['coord']['lon']
        lat = row['coord']['lat']
        temp = row['main']['temp']
        descricao_clima = row['weather'][0]['description']  
        humidade = row['main']['humidity']

        
        
        dados_filtrados.append({
            'cidade': cidade_req,
            'longitude': lon,
            'latitude': lat,
            'temperatura': temp,
            'clima': descricao_clima,
            'umidade': humidade
        })


    cidade_pg = str(dados_filtrados[0]['cidade'])
    longitude_pg = float(dados_filtrados[0]['longitude'])
    latitude_pg = float(dados_filtrados[0]['latitude'])
    temperatura_pg = float(dados_filtrados[0]['temperatura'])
    clima_pg = str(dados_filtrados[0]['clima'])
    umidade_pg = float(dados_filtrados[0]['umidade'])

'''




app = Flask(__name__)
metadata_obj = MetaData()

weather_table =Table(
    "weather_data",
    metadata_obj,
    Column("cidade", String(255)),
    Column("lon", REAL),
    Column("lat", REAL),
    Column("clima", String(255)),
    Column("umidade", REAL),
    Column("temperatura", REAL),
)




@app.route("/")
def index_page():
    return "Pagina inicial sem data"
    

@app.route("/clima/atual/<cidade_get>")
def get_data(cidade_get):
    api_onroute = Api_requi(API_KEY,[],cidade_get,"")
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={cidade_get}&appid={API_KEY}&units=metric&lang=pt_br"
    response_route = requests.get(URL)
    api_onroute.data_return = response_route.json()
    pd_data_filtrado = []
    pd_outData = pd.DataFrame([api_onroute.data_return])
    for index, row in pd_outData.iterrows():
        
        cidade_req = row['name'] # nome da cidade 
        cidade_cod = row['sys']['country'] #mostra a nomenclatura do país , como JP(Japão),DE(alemanha) e afins
        lon = row['coord']['lon'] #aqui é coordenadas da longitude
        lat = row['coord']['lat'] #coordenadas no caso, latitude
        temp = row['main']['temp'] #temperatura atual
        feels_like = row['main']['feels_like'] #sensação térmica
        temp_min = row['main']['temp_min'] #temperatura minima
        temp_max = row['main']['temp_max'] #temperatura maxima
        umidade = row['main']['humidity'] #porcentagem de umidade
        descricao_clima = row['weather'][0]['description'] #descrição do clima 
        vento_velocidade = row['wind']['speed'] # velocidade do vento em metros por segundo m/s
        visibilidade = row['visibility']# distancia de visibilidade ? mostra atÉ qnts kilometros é visivel, a proposito ele está mostrando em metros 
        pressao_atmosferica = row['main']['pressure'] #pressão atmosférica a partir do nivel do mar ta na unidade hectopascal ? 1 hectopascal é o equivalente a 100 pascals
        #rain_amount = row['rain']['1h'] #Precipitação da chuva por mm/h no tempo de 1 hora
        #snow_amount = row['snow']['1h'] # Então, mesma coisa com a neve 
        date_time = row['dt'] #basicamente data/horario no formato de unix time
        #NOTAS, se não estiver chuvendo ou nevando , vai dar erro na requisição e não vai exibir na rota :D
        
        


        
        
        pd_data_filtrado.append({
            'cidade': cidade_req,
            'codigo_cidade': cidade_cod,
            'longitude': lon,
            'latitude': lat,
            'pressao_atmosferica': pressao_atmosferica,
            'temperatura': temp,
            'temperatura_minima': temp_min,
            'temperatura_maxima': temp_max,
            'sensacao_termica': feels_like,
            'clima': descricao_clima,
            'velocidade_vento': vento_velocidade,
            'umidade': umidade,
            'visibilidade': visibilidade,
            #'precipitacao_chuva': rain_amount,
            #'precipitacao_neve': snow_amount,
            'unix_time': date_time
     
        })

    
    return pd_data_filtrado


@app.route("/clima/previsao/<cidade_get>")
def data_previsao(cidade_get):
    api_getcord = Api_requi(API_KEY,[],cidade_get,"")
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={cidade_get}&appid={API_KEY}&units=metric&lang=pt_br"
    response_route = requests.get(URL)
    api_getcord.data_return = response_route.json()
    pd_data_filtrado = []
    pd_outData = pd.DataFrame([api_getcord.data_return])

    lat_for_api = pd_outData["coord"][0]['lat']
    lon_for_api = pd_outData["coord"][0]['lon']
    api_previsao = Api_requi(API_KEY,[],cidade_get,"")
    api_previsao.url_api = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat_for_api}&lon={lon_for_api}&units=metric&cnt=40&appid={API_KEY}"
    response_prev = requests.get(api_previsao.url_api)
    response_prev_json = response_prev.json()
    print(response_prev_json)

    df_list = pd.json_normalize(response_prev_json['list'], sep='_')  # Separação com '_'

    # Processar a coluna 'weather' (lista de dicionários)
    weather_normalized = pd.json_normalize(df_list['weather'].apply(lambda x: x[0] if x else {}))
    weather_normalized = weather_normalized.add_prefix('weather_')
    df_list = pd.concat([df_list.drop('weather', axis=1), weather_normalized], axis=1)

    # Normalizar os dados da cidade (city) e adicionar prefixo
    df_city = pd.json_normalize(response_prev_json['city'], sep='_').add_prefix('city_')

    # Combinar os dados (como há apenas uma cidade, cruzamos os dados)
    df_final = pd.merge(df_list, df_city, how='cross') 

    # Renomear colunas (substituir '.' por '_', redundante aqui devido ao sep='_')
    df_final.columns = df_final.columns.str.replace('.', '_')

    # Resultado final
    df_final
    
    return response_prev_json

if __name__ == "__main__":
    app.run(debug = False)



#configuração para conexão e insert com postgree local
'''
#Conexão direta com o banco de dados na maquina local
engine = create_engine("postgresql+psycopg2://postgres:POST_PASS@localhost/weather_test")


stmt = insert(weather_table).values(cidade=cidade_pg,lon=longitude_pg,lat=latitude_pg,clima=clima_pg,umidade=umidade_pg,temperatura=temperatura_pg)
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
'''
