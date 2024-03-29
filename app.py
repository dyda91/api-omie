import requests
from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify, json
from datetime import date, datetime, timedelta
from models.models import Ops, Movimentos_estoque, Estrutura_op, User, Lote, Saldo_por_posicao
from models.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, current_user
from config import app, db, app_key, app_secret, bcrypt, login_manager



url_produtos = "https://app.omie.com.br/api/v1/geral/produtos/"
url_estrutura = "https://app.omie.com.br/api/v1/geral/malha/"
url_consulta_estoque = "https://app.omie.com.br/api/v1/estoque/resumo/"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#============== REGISTER ============#
@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm() 
    if current_user.is_authenticated:
         return redirect( url_for('logged'))
    if form.validate_on_submit(): 

        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        new_user = User(email=form.email.data, password=encrypted_password, name=form.name.data)  

        db.session.add(new_user)
        db.session.commit() 

        flash(f'Conta criada com socesso para o usuário {form.email.data}', category='success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#=============== LOGIN ==============#
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect( url_for('logged'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        logged_user = form.email.data
        session["logged_user"] = logged_user

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("logged"))
        else:
            flash(f'Erro ao logar no usuário {form.email.data}', category='danger')
            
    return render_template('login_page.html', form=form)  

#=============Sessão====================#
@app.route("/logged")
def logged():
    if "logged_user" in session:
        logged_user = session["logged_user"]
        return redirect(url_for('index'))
    else:
        return redirect(url_for("login"))    

#============= Logout ==================#
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))  




#===================Quando usuario estiver logado ==================#
@app.route('/index', methods = ['GET','POST'])
def index():
    if not current_user.is_authenticated:
         return redirect( url_for('login'))
    return render_template('index.html')


@app.route('/busca', methods = ['GET','POST'])
def busca():
    if not current_user.is_authenticated:
         return redirect( url_for('login'))
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
    item = request.form.get("item")
    if not current_user.is_authenticated:
         return redirect( url_for('login'))
    
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

@app.route('/teste_diego', methods = ['GET','POST'])
def teste_diego():
    
    item = request.form.get('teste_item')
    
    data = {
                "call":"ConsultarProduto",
                "app_key": app_key,
                "app_secret": app_secret,
                "param":[{
                    "codigo": item
                        }
                ]}
    response = requests.post(url=url_produtos, json=data)
    teste = response.json()
    
    fam = 22222
    operacao = (fam/2)
    
    
    
    return render_template('teste.html',teste = teste, operacao = operacao)








@app.route('/itens', methods = ['GET','POST'])
def itens():
    if not current_user.is_authenticated:
         return redirect( url_for('login'))
    pagina = 1
    data = {
        "call":"ListarProdutos",
        "app_key": app_key,
        "app_secret":app_secret,
        "param":[{
            "pagina": pagina,
            "registros_por_pagina": 20,
            "apenas_importado_api": "N",
            "filtrar_apenas_omiepdv": "N"	
            }
        ]}
    response = requests.post(url=url_produtos, json=data)
    lista_itens = response.json()

    return  render_template('itens.html',  lista_itens = lista_itens  )


@app.route('/update', methods=['GET', 'POST'])
def update():
        if not current_user.is_authenticated:
            return redirect( url_for('login'))
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
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    return  render_template('consulta_estoque.html')

@app.route('/estoque', methods = ['GET','POST'])
def estoque():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
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
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    page = request.args.get('page', 1, type=int)
    dados = Movimentos_estoque.query.paginate(page=page,per_page=20)
    return  render_template('lista_movimento.html',  movimentos = dados)

@app.route('/lista_movimento_filtro', methods = ['GET','POST'])
def lista_movimento_filtro():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    data_movimento = request.form.get("data_movimento")
    filtro = Movimentos_estoque.query.filter_by(data_movimento = data_movimento).all()
    
    return  render_template('lista_movimento_filtro.html', filtro = filtro)

# ================================== OPS ===============================================#


@app.route('/ordens_producao', methods = ['GET','POST'])
def ordens_producao():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
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

   


    return redirect(url_for('ordens_producao'))

@app.route('/update_op', methods=['GET', 'POST'])
def update_op():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    
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
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    item = Ops.query.get(id)

    db.session.delete(item)
    db.session.commit()

    flash (f'Op deletada com sucesso', category='soccess')

    return redirect(url_for('ordens_producao'))



# ================================== LOTES ==============================================================

@app.route('/op/<numero_op>', methods = ['GET','POST'])
def op(numero_op):
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    op = numero_op
    item = request.form.get("item")
    descricao = request.form.get("descricao")
    op_qtd = request.form.get("op_qtd")
    ref = [op, item, descricao, op_qtd]
    lotes = Lote.query.filter_by(op_referencia = op).all()   
    op_info = Ops.query.filter_by(numero_op = op).all()

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
     
    

    return render_template("lotes.html", lotes=lotes, ref=ref, op_info=op_info, op=op, item_recomendado_estrutura=item_recomendado_estrutura,  estrutura_op= estrutura_op)


@app.route('/adicionar_lote', methods=['POST'])
def adicionar_lote():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    item = request.form.get("item")
    op_referencia = request.form.get("op_referencia")
    lote = str(int(db.session.query(db.func.max(Lote.lote)).scalar() or 0) + 1)
    numero_lote = "".join([op_referencia, "/", lote ])
    quantidade = request.form.get("quantidade")
    data_fabricacao = datetime.now().strftime('%d/%m/%Y')
    data_validade = (datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')
    novo_lote = Lote(op_referencia=op_referencia, lote=lote, numero_lote=numero_lote, quantidade=quantidade, data_fabricacao=data_fabricacao, data_validade=data_validade)
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
        qtd_unitaria = float(row.get('quantProdMalha'))
        nova_estrutura = Estrutura_op(op_referencia=op_referencia, 
                                    item_estrutura=row.get("codProdMalha"), 
                                    descricao_item=row.get("descrProdMalha"),
                                    quantidade_item=float(quantidade) * float(qtd_unitaria))

    db.session.add(nova_estrutura)    
    db.session.add(novo_lote)
    db.session.commit()

    
    return redirect(request.referrer)

@app.route('/deleta_lote', methods=['GET', 'POST'])
def deleta_lote():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    id = request.form.get("id")
    lote = Lote.query.get(id)

    db.session.delete(lote)
    db.session.commit()   


    return redirect(request.referrer)


@app.route('/estrutura_op/<numero_op>/<numero_lote>', methods = ['GET','POST'])
def estrutura_op(numero_op, numero_lote):
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    op = numero_op
    lote = numero_op + "/" + numero_lote
    itens_movimentados = Movimentos_estoque.query.filter_by(op_referencia = op).all()   
    op_dados = Ops.query.filter_by(numero_op = op).all()

    item_recomendado_estrutura = Estrutura_op.query.filter_by(op_referencia = op).all()  
    

  
    return render_template("estrutura_op.html", itens_movimentados=itens_movimentados, lote=lote, op=op, op_dados=op_dados, item_recomendado_estrutura=item_recomendado_estrutura)


@app.route('/movimento_estoque', methods = ['GET','POST'])
def movimento_estoque():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))

    data_atual = date.today().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M")
    if request.method == 'POST':
        op_referencia = request.form.get("op")
        id = request.form.get("id")
        numero_lote = request.form.get("numero_lote")
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
                    "dDia":data_atual
                    }]
                }

        response = requests.post(url=url_consulta_estoque, json=saldo)
        saldo_resp = response.json()
        saldo = 10000
        saldo_anterior = saldo
        
        novo_movimento = Movimentos_estoque(item_movimento = item_movimento, 
                                            numero_lote = numero_lote,
                                            descricao=descricao, 
                                            op_referencia=op_referencia, 
                                            item_referencia=item_referencia, 
                                            saldo_anterior=saldo_anterior, 
                                            quantidade_movimento=quantidade_movimento, 
                                            saldo_atual = saldo_anterior - quantidade_movimento,
                                            data_movimento = data_atual,
                                            hora_movimento = hora_atual)
        if id != None:
            try:
                deleta_item = Estrutura_op.query.get(id)
                db.session.delete(deleta_item)
            except:
                pass

        db.session.add(novo_movimento)  
        db.session.commit()
            
        return redirect(request.referrer)


@app.route('/encerra_op', methods=['GET', 'POST'])
def encerra_op():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
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
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    id = request.form.get("id")
    movimento = Movimentos_estoque.query.get(id)

    db.session.delete(movimento)
    db.session.commit()   


    return redirect(request.referrer)



@app.route('/movimentos_posicaos', methods=['GET', 'POST'])
def movimentos_posicaos():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))

    if request.method == 'POST':
        item = request.form.get("item")
        descricao = request.form.get("descricao")
        quantidade = request.form.get("quantidade_lote")
        op = request.form.get("op_lote")
        lote = request.form.get("lote")
        operador = request.form.get("operador")
        posicao = request.form.get("posicao")

        saldo_movimento = Saldo_por_posicao(item=item, descricao=descricao, quantidade=quantidade, op=op, lote=lote, operador=operador, posicao=posicao)

        db.session.add(saldo_movimento)  
        db.session.commit()

    return redirect(url_for('posicoes_estoque'))    

@app.route('/transferir_saldo_posicao', methods=['GET', 'POST'])
def transferir_saldo_posicao():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    
    if request.method == 'POST':
        transf_lote = Saldo_por_posicao.query.get(request.form.get('id'))
        transf_lote.posicao = request.form.get("posicao")

        db.session.commit()
        
        flash (f'Lote transferido com sucesso', category='soccess')

        return redirect(url_for('posicoes_estoque'))


@app.route('/posicoes_estoque', methods=['GET', 'POST'])
def posicoes_estoque():
    if not current_user.is_authenticated:
        return redirect( url_for('login'))
    page = request.args.get('page', 1, type=int)
    dados = Saldo_por_posicao.query.paginate(page=page,per_page=20)
    return  render_template('posicoes_estoque.html',  posicoes = dados)
    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(host='0.0.0.0', port=8080, debug=True)