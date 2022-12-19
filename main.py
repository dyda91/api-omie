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


url_produtos = "https://app.omie.com.br/api/v1/geral/produtos/"
url_estrutura = "https://app.omie.com.br/api/v1/geral/malha/"



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
        response = requests.post(url=url_produtos, json=data)
        busca = response.json()
    
        return  render_template('busca.html',  busca = busca)



@app.route('/estrutura', methods = ['GET','POST'])
def estrutura():
    item = "cba-4301"
    if request.method == 'POST':
        item = request.form["estrutura"]
        if item == None:
            item = "cba-4301"
        else:
            data = {
                    "call":"ConsultarEstrutura",
                    "app_key": app_key,
                    "app_secret": app_secret,
                    "param":[{
                        "codProduto": item
                        }
                    ]}
            response = requests.post(url=url_estrutura, json=data)
            estrutura = response.json()

            return render_template("estrutura.html", estrutura=estrutura)

# data = {
#                 "call":"ConsultarEstrutura",
#                 "app_key": app_key,
#                 "app_secret": app_secret,
#                 "param":[{
#                     "codProduto": "cba-4301"
#                     }
#                 ]}
# response = requests.post(url=url_estrutura, json=data)
# estrutura = response.json()


# itemm = estrutura.get('ident')

# print(itemm)



@app.route('/itens', methods = ['GET','POST'])
def itens():
    data = {
        "call":"ListarProdutos",
        "app_key": app_key,
        "app_secret":app_secret,
        "param":[{
            "pagina": 1,
            "registros_por_pagina": 7400,
            "apenas_importado_api": "N",
            "filtrar_apenas_omiepdv": "N"	
            }
        ]}
    response = requests.post(url=url_produtos, json=data)
    lista_itens = response.json()

    return  render_template('itens.html',  lista_itens = lista_itens  )



if __name__ == "__main__":
    app.run(debug=True)