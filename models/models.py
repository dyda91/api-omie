from enum import unique
from re import T
from config import db
from flask_login import UserMixin




class Ops(db.Model):
    __tablename__='ops'
    id = db.Column(db.Integer, primary_key=True)   
    numero_op = db.Column(db.String)
    situação = db.Column(db.String)
    item = db.Column(db.String)
    descrição = db.Column(db.String)
    quantidade = db.Column(db.Integer)
    data_abertura = db.Column(db.String)
    hora_abertura = db.Column(db.String)


    def __init__(self, numero_op, situação, item, descrição, quantidade, data_abertura, hora_abertura):
        self.numero_op = numero_op
        self.situação = situação
        self.item = item
        self.descrição = descrição
        self.quantidade = quantidade
        self.data_abertura = data_abertura
        self.hora_abertura = hora_abertura

       
        # db.create_all()
        # db.session.commit()


    def __repr__(self):
        return 'Ops: {} - {} - {} - {} - {} - {} - {} - {}' .format(self.id, self.numero_op, self.situação, self.item, self.descrição, 
                                                                    self.quantidade, self.data_abertura, self.hora_abertura)


class Movimentos_estoque(db.Model):
    __tablename__='movimentos_estoque'
    id = db.Column(db.Integer, primary_key=True)
    item_movimento = db.Column(db.String)
    descricao = db.Column(db.String)
    op_referencia = db.Column(db.Integer)
    item_referencia = db.Column(db.String)
    saldo_anterior = db.Column(db.Integer)
    quantidade_movimento = db.Column(db.Integer)
    saldo_atual = db.Column(db.Integer)
    data_movimento = db.Column(db.String)
    hora_movimento = db.Column(db.String)

    def __init__(self, item_movimento, descricao, op_referencia, 
                item_referencia, saldo_anterior, quantidade_movimento, saldo_atual,  data_movimento, hora_movimento):  

        self.item_movimento = item_movimento
        self.descricao = descricao
        self.op_referencia = op_referencia
        self.item_referencia = item_referencia
        self.saldo_anterior = saldo_anterior
        self.quantidade_movimento = quantidade_movimento
        self.saldo_atual = saldo_atual
        self.data_movimento = data_movimento
        self.hora_movimento = hora_movimento

        # db.create_all()
        # db.session.commit()


    def __repr__(self):
        return 'Movimentos_estoque: {} - {} - {} - {} - {} - {} - {} - {} - {} - {}' .format(self.id, self.item_movimento, self.descricao, self.op_referencia, 
                self.item_referencia, self.saldo_anterior, self.quantidade_movimento,  self.saldo_atual, self.data_movimento, self.hora_movimento)


class Estrutura_op(db.Model):
    __tablename__='estrutura_op'
    id = db.Column(db.Integer, primary_key=True)
    op_referencia = db.Column(db.String)
    item_estrutura = db.Column(db.String)
    descricao_item = db.Column(db.String)
    quantidade_item = db.Column(db.Float)

    def __init__(self, op_referencia, item_estrutura, descricao_item, 
                quantidade_item):  

        self.op_referencia = op_referencia
        self.item_estrutura = item_estrutura
        self.descricao_item = descricao_item
        self.quantidade_item = quantidade_item
       
        db.create_all()
        db.session.commit()


    def __repr__(self):
        return 'Movimentos_estoque: {} - {} - {} - {}' .format(self.op_referencia, self.item_estrutura, self.descricao_item,self.quantidade_item)



class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

        db.create_all()
        db.session.commit()

    def __repr__(self):
        return "<User %r>" % self.email