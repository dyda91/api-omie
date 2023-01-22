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

    def __init__(self, numero_op, situação, item, descrição, quantidade):
        self.numero_op = numero_op
        self.situação = situação
        self.item = item
        self.descrição = descrição
        self.quantidade = quantidade

        db.create_all()
        db.session.commit()


    def __repr__(self):
        return 'Ops: {}' .format(self.item)