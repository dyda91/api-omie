import requests
from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify, json
from datetime import date, datetime
from models.models import Ops, Movimentos_estoque
from config import app, db, app_key, app_secret



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
    pagina = 78
    data = {
        "call":"ListarProdutos",
        "app_key": app_key,
        "app_secret":app_secret,
        "param":[{
            "pagina": pagina,
            "registros_por_pagina": 50,
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
    data_atual = date.today().strftime("%d/%m/%Y")
    if request.method == 'POST':
        item = request.form.get("estoque")
        data = {"call":"ObterEstoqueProduto",
        "app_key":app_key,
        "app_secret":app_secret,
        "param":[{
            "cCodigo":item,
            "dDia": data_atual
            }]
            }
        response = requests.post(url=url_consulta_estoque, json=data)
        estoque = response.json()
               

        return  render_template('estoque.html',  estoque = estoque)


@app.route('/lista_movimento', methods = ['GET','POST'])
def lista_movimento():
    page = request.args.get('page', 1, type=int)
    dados = Movimentos_estoque.query.paginate(page=page,per_page=15)
    return  render_template('lista_movimento.html',  movimentos = dados)

@app.route('/lista_movimento_filtro', methods = ['GET','POST'])
def lista_movimento_filtro():
    data_movimento = request.form.get("data_movimento")
    filtro = Movimentos_estoque.query.filter_by(data_movimento = data_movimento).all()
    
    return  render_template('lista_movimento_filtro.html', filtro = filtro)

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
    data_atual = date.today().strftime("%Y-%m-%d")
    hora_atual = datetime.now().strftime("%H:%M")
    if request.method == 'POST':
        item = request.form.get("item")
        data = {
                "call":"ConsultarProduto",
                "app_key": app_key,
                "app_secret": app_secret,
                "param":[{
                    "codigo": item
                    }
                ]}
        response = requests.post(url=url_produtos, json=data)
        data_resp = response.json()
        numero_op = request.form.get("numero_op")
        situação = "Aberta"       
        descrição = data_resp.get("descricao")
        quantidade = request.form.get("quantidade")
        data_abertura = data_atual
        hora_abertura = hora_atual

        novo_item = Ops(numero_op=numero_op, situação=situação, item=item, descrição=descrição, quantidade=quantidade, data_abertura = data_abertura, hora_abertura = hora_abertura)

        db.session.add(novo_item)
        db.session.commit()

        flash (f'OP para o item {item} Aberta com sucesso', category='soccess')

        return redirect(url_for('ordens_producao'))

@app.route('/update_op', methods=['GET', 'POST'])
def update_op():
    
    if request.method == 'POST':
        edit_item = Ops.query.get(request.form.get('id'))  
        edit_item.item = request.form.get("item")
        edit_item.descrição = request.form.get("descricao")
        edit_item.quantidade = request.form.get("quantidade")

        db.session.commit()
        
        flash (f'Op editada com sucesso', category='soccess')

        return redirect(url_for('ordens_producao'))
        


@app.route('/delete_op/<id>', methods=['GET', 'POST'])
def delete(id):
    item = Ops.query.get(id)

    db.session.delete(item)
    db.session.commit()

    flash (f'Op deletada com sucesso', category='soccess')

    return redirect(url_for('ordens_producao'))



# ================================================================================================


@app.route('/estrutura_op', methods = ['GET','POST'])
def estrutura_op():
    op = request.form.get("id")
    item = request.form.get("item")   
    descricao = request.form.get("descricao")
    op_qtd = request.form.get("op_qtd")
    ref = [op, item, descricao, op_qtd]
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

        
        return render_template("estrutura_op.html", estrutura_op=estrutura_op, ref = ref)



@app.route('/movimento_estoque', methods = ['GET','POST'])
def movimento_estoque():
    item = request.form.get("item")
    op = request.form.get("id")
    op_qtd = float(request.form.get("op_qtd"))
      
    data_atual = date.today().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M")

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



    for row in estrutura["itens"]:    

            real_unitario = float(row.get('quantProdMalha'))
            quantidade_movimento = op_qtd * real_unitario
            item_movimento = row.get("codProdMalha")

            saldo = {"call":"ObterEstoqueProduto",
                 "app_key":app_key,
                 "app_secret":app_secret,
                 "param":[{
                        "cCodigo":item_movimento,
                        "dDia": data_atual
            }]
            }
            response = requests.post(url=url_consulta_estoque, json=saldo)
            saldo = response.json()
            saldo = saldo["listaEstoque"][0]
            saldo_anterior = float(saldo.get("nSaldo"))

            movimento = Movimentos_estoque( 
            item_movimento = item_movimento,
            descrProdMalha = row.get("descrProdMalha"),
            codFamMalha = row.get("codFamMalha"),
            descrFamMalha = row.get("descrFamMalha"),
            op_referencia = op,
            item_referencia = item,
            saldo_anterior = saldo_anterior,
            quantidade_movimento =  quantidade_movimento,
            saldo_atual = saldo_anterior - quantidade_movimento,
            quantProdMalha = row.get('quantProdMalha'),
            idFamMalha = row.get("idFamMalha"),
            idMalha = row.get("idMalha"),
            idProdMalha = row.get("idProdMalha"),
            intProdMalha = row.get("intProdMalha"),
            percPerdaProdMalha = row.get("percPerdaProdMalha"),
            pesoBrutoProdMalha = row.get("pesoBrutoProdMalha"),
            pesoLiqProdMalha = row.get("pesoLiqProdMalha"),            
            tipoProdMalha = row.get("tipoProdMalha"),
            uAltProdMalha = row.get("uAltProdMalha"),
            uIncProdMalha = row.get("uIncProdMalha"),
            unidProdMalha = row.get("unidProdMalha"),
            data_movimento = data_atual,
            hora_movimento = hora_atual)

            db.session.add(movimento)
            

    edita_situacao = Ops.query.get(op)
    edita_situacao.situação = "Encerrada"

    db.session.commit()

    return redirect(url_for('ordens_producao'))


if __name__ == "__main__":
    app.run(debug=True)