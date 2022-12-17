import requests
from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify, json
from dotenv import load_dotenv
import os
load_dotenv()
from flask_cors import CORS


app = Flask (__name__)
CORS(app)

app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')


url = 'https://app.omie.com.br/api/v1/geral/produtos/'

@app.route('/', methods = ['GET','POST'])
def index():
        return render_template('index.html')


@app.route('/busca', methods = ['GET','POST'])
def busca():
    if request.method == 'POST':
        item = request.form.get("search")
        data = {
                "call":"ConsultarProduto",
                "app_key": app_key,
                "app_secret": app_secret,
                "param":[{
                    "codigo": item
                    }
                ]}
        response = requests.post(url=url, json=data)
        busca = response.json()
    
        return  render_template('busca.html',  busca = busca)



# @app.route('/all_itens', methods = ['GET','POST'])
# def all_itens():
#     url = 'https://app.omie.com.br/api/v1/geral/produtos/'

#     request_type = "POST"
#     data = {
#         "call":"ListarProdutos",
#         "app_key":"706444293555",
#         "app_secret":"a51654af368ec4e34129dab2b017dab7",
#         "param":[{
#             "pagina":1,
#             "registros_por_pagina":7000,
#             "apenas_importado_api":"N",
#             "filtrar_apenas_omiepdv":"N"		
#             }
#         ]}
#     response = requests.post(url=url, json=data)
#     json = response.json()

    
#     return  render_template('index.html',  json = json  )



if __name__ == "__main__":
    app.run(debug=True)