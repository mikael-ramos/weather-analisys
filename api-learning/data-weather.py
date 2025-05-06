from flask import Flask, jsonify, render_template
import requests  # Importe a biblioteca 'requests' para fazer chamadas HTTP externas
from dotenv import load_dotenv
import os
import pandas as pd
app = Flask(__name__)

load_dotenv()

def dados_api(cidade):
    API_KEY = os.getenv("API_KEY")
    # Use a variável 'cidade' na URL da API!
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()



@app.route("/")
def home():
    return "Acesse /clima/<cidade> para ver dados do clima."

@app.route("/clima/<cidade>")
def get_clima(cidade):
    
    
    try:
        # Extrai os dados JSON da resposta
        dados_clima = dados_api(cidade)




        
        return jsonify(dados_clima), 200  # Status 200 = OK
    
    #tratatamento de erros....nunca que eu vou conseguir lembrar isso
    except requests.exceptions.HTTPError as err:
        return jsonify({"erro": f"Erro na API: {str(err)}"}), 500
    except Exception as err:
        return jsonify({"erro": f"NUH UH, problema entre o teclado e a cadeira: {str(err)}"}), 500
    





if __name__ == '__main__':
    app.run(debug=True)