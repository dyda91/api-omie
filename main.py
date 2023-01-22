import requests
from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify, json
from datetime import date
from models.models import Ops
from config import app, db, app_key, app_secret




     
busca_data = "14/01/2023"


url_produtos = "https://app.omie.com.br/api/v1/geral/produtos/"
url_estrutura = "https://app.omie.com.br/api/v1/geral/malha/"
url_consulta_estoque = "https://app.omie.com.br/api/v1/estoque/resumo/"



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
    item = request.form['item']
    
    if request.method == 'POST':  
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



@app.route('/itens', methods = ['GET','POST'])
def itens():
    pagina = 77
    data = {
        "call":"ListarProdutos",
        "app_key": app_key,
        "app_secret":app_secret,
        "param":[{
            "pagina": pagina,
            "apenas_importado_api": "N",
            "filtrar_apenas_omiepdv": "N"	
            }
        ]}
    response = requests.post(url=url_produtos, json=data)
    lista_itens = response.json()

    return  render_template('itens.html',  lista_itens = lista_itens  )


@app.route('/update', methods=['GET', 'POST'])
def update():
        data = {
                "call":"AlterarProduto",
                "app_key":app_key,
                "app_secret":app_secret,
                "param":[{
                    "codigo":"teste0001",
                    "descricao":"Produto de teste",
                    "unidade":"UN"
                    }
            ]}

        return redirect(url_for('itens'))


@app.route('/consulta_estoque', methods = ['GET','POST'])
def consulta_estoque(): 
    return  render_template('consulta_estoque.html')

@app.route('/estoque', methods = ['GET','POST'])
def estoque():
    if request.method == 'POST':
        item = request.form.get("estoque")
        data = {"call":"ObterEstoqueProduto",
        "app_key":app_key,
        "app_secret":app_secret,
        "param":[{
            "cCodigo":item,
            "dDia": busca_data
            }]
            }
        response = requests.post(url=url_consulta_estoque, json=data)
        estoque = response.json()
               

        return  render_template('estoque.html',  estoque = estoque)

# =======================================================================================


@app.route('/ordens_producao', methods = ['GET','POST'])
def ordens_producao():
    # if not current_user.is_authenticated:
    # #      return redirect( url_for('login'))
    page = request.args.get('page', 1, type=int)
    dados = Ops.query.paginate(page=page,per_page=10) 
    return render_template('ordens_producao.html', itens = dados)

@app.route('/insert_op', methods=['POST'])
def insert_op():     
     if request.method == 'POST':
        numero_op = request.form.get("numero_op")
        situação = request.form.get("situacao")
        item = request.form.get("item")
        descrição = request.form.get("descricao")
        quantidade = request.form.get("quantidade")

        novo_item = Ops(numero_op=numero_op, situação=situação, item=item, descrição=descrição, quantidade=quantidade)

        db.session.add(novo_item)
        db.session.commit()

        flash (f'Item {item} cadastrado com sucesso', category='soccess')

        return redirect(url_for('ordens_producao'))

@app.route('/update_op', methods=['GET', 'POST'])
def update_op():
    
    if request.method == 'POST':
        edit_item = Ops.query.get(request.form.get('id'))

        edit_item.numero_op = request.form.get("numero_op")   
        edit_item.situação = request.form.get("situacao")
        edit_item.item = request.form.get("item")
        edit_item.descrição = request.form.get("descricao")
        edit_item.quantidade = request.form.get("quantidade")
        db.session.commit()
        
        flash (f'Item editado com sucesso', category='soccess')

        return redirect(url_for('ordens_producao'))
        

# @app.route('/busca_op', methods=['GET', 'POST'])
# def busca():
#     if request.method == 'POST':

#         busca = Ops.query.filter_by(item = request.form.get('search')).all()

#         return render_template('search.html', busca = busca)


@app.route('/delete_op/<id>', methods=['GET', 'POST'])
def delete(id):
    item = Ops.query.get(id)

    db.session.delete(item)
    db.session.commit()

    flash (f'Item deletado com sucesso', category='soccess')

    return redirect(url_for('ordens_producao'))



# ================================================================================================


@app.route('/estrutura_op', methods = ['GET','POST'])
def estrutura_op():
    item = request.form['item']
    
    if request.method == 'POST':  
        data = {
                "call":"ConsultarEstrutura",
                "app_key": app_key,
                "app_secret": app_secret,
                "param":[{
                    "codProduto": item
                        }
                ]}
        response = requests.post(url=url_estrutura, json=data)
        estrutura_op = response.json()
        
        return render_template("estrutura_op.html", estrutura_op=estrutura_op)



if __name__ == "__main__":
    app.run(debug=True)