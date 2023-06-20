from app import db
from sqlalchemy import ForeignKey

class FuncionarioRH(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30))
    email = db.Column(db.String(20))
    telefone = db.Column(db.Integer)
    cpf = db.Column(db.Integer)
    senha = db.Column(db.String(10))
    foto = db.Column(db.Text)

    def __init__(self, nome, email, telefone, cpf, senha, foto):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cpf = cpf
        self.senha = senha
        self.foto = foto

    def __repr__(self):
        return '<FuncionarioRH %r>' % self.id


class TiposServidores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(30))
    meses_para_progressao = db.Column(db.Integer)

    def __init__(self, descricao, meses_para_progressao):
        self.descricao = descricao
        self.meses_para_progressao = meses_para_progressao

    def __repr__(self):
        return '<TiposServidores %r>' % self.id


class Servidor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30))
    email = db.Column(db.String(20))
    telefone = db.Column(db.Integer)
    cpf = db.Column(db.Integer)
    data_admissao = db.Column(db.DateTime)
    data_criacao = db.Column(db.DateTime)
    cargo = db.Column(db.String(20))
    foto = db.Column(db.Text)
    id_tipo = db.Column(db.Integer, ForeignKey('tipos_servidores.id'))

    def __init__(self, nome, email, telefone, cpf, data_admissao, data_criacao, cargo, foto, id_tipo):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cpf = cpf
        self.data_admissao = data_admissao
        self.data_criacao = data_criacao
        self.cargo = cargo
        self.foto = foto
        self.id_tipo = id_tipo

    def __repr__(self):
        return '<Servidor %r>' % self.id


class EmailProgramado(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_destinatario = db.Column(db.String(20))
    data_hora_envio = db.Column(db.DateTime)

    def __init__(self, email_destinatario, data_hora_envio):
        self.email_destinatario = email_destinatario
        self.data_hora_envio = data_hora_envio

    def __repr__(self):
        return '<EmailProgramado %r>' % self.id


class Eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_responsavel = db.Column(db.Integer, ForeignKey('funcionario_rh.id'))
    data = db.Column(db.Date)
    hora = db.Column(db.Date)
    descricao = db.Column(db.String(100))
    id_programacao_email = db.Column(db.Integer, ForeignKey('email_programado.id'))

    def __init__(self, id_responsavel, data, hora, descricao, id_programacao_email):
        self.id_responsavel = id_responsavel
        self.data = data
        self.hora = hora
        self.descricao = descricao
        self.id_programacao_email = id_programacao_email

    def __repr__(self):
        return '<Eventos %r>' % self.id