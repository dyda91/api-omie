from enum import unique
from re import T
from config import db
# from flask_login import UserMixin




class Ops(db.Model):
    __tablename__='ops'
    id = db.Column(db.Integer, primary_key=True)   
    numero_op = db.Column(db.Integer)
    situação = db.Column(db.String)
    item = db.Column(db.String)
    descrição = db.Column(db.String)
    quantidade = db.Column(db.Integer)
    data_abertura = db.Column(db.String)
    hora_abertura = db.Column(db.String)

    movimento_est = db.relationship('Movimentos_estoque', backref='Movimentos_estoque', lazy=True)


    def __init__(self, numero_op, situação, item, descrição, quantidade, data_abertura, hora_abertura):
        self.numero_op = numero_op
        self.situação = situação
        self.item = item
        self.descrição = descrição
        self.quantidade = quantidade
        self.data_abertura = data_abertura
        self.hora_abertura = hora_abertura

       
        db.create_all()
        db.session.commit()


    def __repr__(self):
        return 'Ops: {}' .format(self.item)


class Movimentos_estoque(db.Model):
    __tablename__='movimentos_estoque'
    id = db.Column(db.Integer, primary_key=True)
    item_movimento = db.Column(db.String)
    descricao = db.Column(db.String)
    op_referencia = db.Column(db.Integer, db.ForeignKey('ops.numero_op'))
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

        db.create_all()
        db.session.commit()


    def __repr__(self):
        return 'Movimentos_estoque: {}' .format(self.op_referencia)