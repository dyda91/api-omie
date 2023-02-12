import requests
from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify, json
from datetime import date, datetime
from models.models import Ops, Movimentos_estoque, Estrutura_op
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
    dados = Movimentos_estoque.query.paginate(page=page,per_page=20)
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
     
    ano_dia = date.today().strftime("%Y%d")
    hora_minuto = datetime.now().strftime("%H%M")
    numero_op = ano_dia + hora_minuto

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
        numero_op = numero_op
        situação = "Aberta"       
        descrição = data_resp.get("descricao")
        quantidade = float(request.form.get("quantidade"))
        data_abertura = data_atual
        hora_abertura = hora_atual

        novo_item = Ops(numero_op=numero_op, situação=situação, item=item, descrição=descrição, quantidade=quantidade, data_abertura = data_abertura, hora_abertura = hora_abertura)

        db.session.add(novo_item)
        db.session.commit()

        flash (f'OP para o item {item} Aberta com sucesso', category='soccess')

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

    for row in estrutura_op["itens"]:
        op = numero_op
        qtd_unitaria = float(row.get('quantProdMalha'))
        nova_estrutura = Estrutura_op(op_referencia=op, 
                                    item_estrutura=row.get("codProdMalha"), 
                                    descricao_item=row.get("descrProdMalha"),
                                    quantidade_item=quantidade * qtd_unitaria)
        db.session.add(nova_estrutura)
        db.session.commit()


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


@app.route('/estrutura_op/<numero_op>', methods = ['GET','POST'])
def estrutura_op(numero_op):
    op = numero_op
    item = request.form.get("item")
    descricao = request.form.get("descricao")
    op_qtd = request.form.get("op_qtd")
    ref = [op, item, descricao, op_qtd]
    itens_movimentados = Movimentos_estoque.query.filter_by(op_referencia = op).all()   
    op_dados = Ops.query.filter_by(numero_op = op).all()
     
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

    item_recomendado_estrutura = Estrutura_op.query.filter_by(op_referencia = op).all()

    return render_template("estrutura_op.html", itens_movimentados=itens_movimentados, estrutura_op=estrutura_op, ref=ref, item_recomendado_estrutura=item_recomendado_estrutura, op_dados=op_dados)


@app.route('/movimento_estoque', methods = ['GET','POST'])
def movimento_estoque():

    data_atual = date.today().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M")
    if request.method == 'POST':
        op_referencia = request.form.get("op")
        
        id = request.form.get("id")
        item_movimento = request.form.get("item")
        quantidade_movimento = float(request.form.get("quantidade"))
        item_referencia = request.form.get("item_referencia")

        data = {
                    "call":"ConsultarProduto",
                    "app_key": app_key,
                    "app_secret": app_secret,
                    "param":[{
                        "codigo": item_movimento
                        }
                    ]}

        response = requests.post(url=url_produtos, json=data)
        data_resp = response.json()

        descricao = data_resp.get("descricao")

        saldo = {"call":"ObterEstoqueProduto",
                    "app_key":app_key,
                    "app_secret":app_secret,
                    "param":[{
                            "cCodigo":item_movimento,
                            "dDia": data_atual
                }]
                }

        response = requests.post(url=url_estrutura, json=saldo)
        saldo_resp = response.json()
        saldo_anterior = float(1000000)
        # saldo = saldo_resp["listaEstoque"][0]
        # # saldo_anterior = float(saldo.get("nSaldo"))
        
        novo_movimento = Movimentos_estoque(item_movimento=item_movimento, 
                                            descricao=descricao, 
                                            op_referencia=op_referencia, 
                                            item_referencia=item_referencia, 
                                            saldo_anterior=saldo_anterior, 
                                            quantidade_movimento=quantidade_movimento, 
                                            saldo_atual = saldo_anterior - quantidade_movimento,
                                            data_movimento = data_atual,
                                            hora_movimento = hora_atual)
        if id != None:
            deleta_item = Estrutura_op.query.get(id)
            db.session.delete(deleta_item)

        db.session.add(novo_movimento)  
        db.session.commit()

    return redirect(request.referrer)


@app.route('/encerra_op', methods=['GET', 'POST'])
def encerra_op():
    if request.method == 'POST':
        id = request.form.get('id')
        situacao = request.form.get('situacao')
        encerra = Ops.query.get(id)  
        encerra.situação = situacao
        db.session.commit()
        if situacao == "Aberta":
            flash (f'Op Reaberta com sucesso', category='soccess')
        else:
            flash (f'Op Encerrada com sucesso', category='soccess')
    return redirect(url_for('ordens_producao'))


@app.route('/deleta_movimento_item', methods=['GET', 'POST'])
def deleta_movimento_item():
    id = request.form.get("id")
    movimento = Movimentos_estoque.query.get(id)

    db.session.delete(movimento)
    db.session.commit()   


    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)