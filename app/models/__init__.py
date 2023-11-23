from datetime import datetime

from sqlalchemy.orm import aliased

from app import db, login_manager
from sqlalchemy import ForeignKey, text
from app.functions import execute, empty, generate_token, serialize_values
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import session


@login_manager.user_loader
def get_user(user_id):
    return serialize_values(FuncionarioRH.query.filter_by(id=user_id).first())


class FuncionarioRH(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30))
    email = db.Column(db.String(20))
    telefone = db.Column(db.Integer)
    cpf = db.Column(db.Integer)
    senha = db.Column(db.String(110))
    foto = db.Column(db.Text)
    email_confirmado = db.Column(db.Boolean, default=False)

    def getRepetido(self):
        repetidos = []
        dados = execute(f"""
            SELECT 
                cpf = '{self.cpf}' as 'CPF',
                telefone = '{self.telefone}' as 'Telefone',
                email = '{self.email}' as 'E-mail'
            FROM teste.funcionario_rh 
            WHERE 
                cpf = '{self.cpf}' or 
                telefone = '{self.telefone}' or 
                email = '{self.email}'""")
        if not empty(dados):
            for key, value in (dados[0]).items():
                if value == 1:
                    repetidos.append(key)
        return repetidos

    def deleteConfirmations(self):
        return execute(f"""DELETE FROM teste.token_usuario WHERE user_id = {self.id} AND action = 'tokenUser'""")

    def deleteRecoveries(self):
        return execute(f"""DELETE FROM teste.token_usuario WHERE user_id = {self.id} AND action = 'passwordRecovery'""")

    def emailExists(self):
        funcionario = self.query.filter_by(email=self.email).first()
        return not empty(funcionario)

    def exists(self):
        funcionario = self.query.filter_by(email=self.email).first()
        senha_correta = check_password_hash(funcionario.senha, self.senha)
        if not empty(funcionario) and senha_correta:
            return funcionario
        else:
            return False

    def save(self):
        try:
            if self.id is None:
                self.senha = generate_password_hash(self.senha)
                db.session.add(self)
                db.session.commit()
                return self.id
            else:
                funcionario = self.query.get(self.id)
                if funcionario:
                    campos = self.__dict__
                    for campo, valor in campos.items():
                        if campo != 'id' and campo != '_sa_instance_state' and hasattr(funcionario, campo):
                            setattr(funcionario, campo, valor)
                            continue
                    db.session.commit()
                    return self.id
                else:
                    print("Registro não encontrado no banco de dados.")
                    return False
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    def get_where(*var):
        return FuncionarioRH.query.filter_by(var)

    def __repr__(self):
        return '<FuncionarioRH %r>' % self.id


class TiposServidores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(30))
    tabela_progressao = db.Column(db.JSON)

    def __init__(self, descricao, meses_para_progressao):
        self.descricao = descricao
        self.meses_para_progressao = meses_para_progressao

    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
                db.session.commit()
                return self.id
            else:
                funcionario = self.query.get(self.id)
                if funcionario:
                    campos = self.__dict__
                    for campo, valor in campos.items():
                        if campo != 'id' and campo != '_sa_instance_state' and hasattr(funcionario, campo):
                            setattr(funcionario, campo, valor)
                            continue
                    db.session.commit()
                    return self.id
                else:
                    print("Registro não encontrado no banco de dados.")
                    return False
        except Exception as e:
            print(e)
            db.session.rollback()
            return None
    @staticmethod
    def getTipoServidores():
        return execute("SELECT t.id, t.descricao, CAST(JSON_UNQUOTE(tabela_progressao) AS CHAR) AS tabela_progressao FROM tipos_servidores t")
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

    def __init__(self, id, nome, email, telefone, cpf, data_admissao, cargo, foto, id_tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cpf = cpf
        self.data_admissao = data_admissao
        self.cargo = cargo
        self.foto = foto
        self.id_tipo = id_tipo

    @staticmethod
    def getServidores():
        return execute("SELECT s.* FROM servidor s")
    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
                db.session.commit()
                return self.id
            else:
                this = self.query.get(self.id)
                if this:
                    campos = self.__dict__
                    for campo, valor in campos.items():
                        if campo != 'id' and campo != '_sa_instance_state' and hasattr(this, campo):
                            setattr(this, campo, valor)
                            continue
                    db.session.commit()
                    return self.id
                else:
                    print("Registro não encontrado no banco de dados.")
                    return False
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    def __repr__(self):
        return '<Servidor %r>' % self.id


class EmailProgramado(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    destinatario = db.Column(db.String(30))
    data_hora_envio = db.Column(db.DateTime)
    assunto = db.Column(db.String(100))
    texto = db.Column(db.Text)
    enviado = db.Column(db.Boolean)

    def __init__(self, destinatario, data_hora_envio, assunto, texto, enviado=False):
        self.destinatario = destinatario
        self.data_hora_envio = data_hora_envio
        self.assunto = assunto
        self.texto = texto
        self.enviado = enviado

    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
                db.session.commit()
                return self.id
            else:
                this = self.query.get(self.id)
                if this:
                    campos = self.__dict__
                    for campo, valor in campos.items():
                        if campo != 'id' and campo != '_sa_instance_state' and hasattr(this, campo):
                            setattr(this, campo, valor)
                            continue
                    db.session.commit()
                    return self.id
                else:
                    print("Registro não encontrado no banco de dados.")
                    return False
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    @staticmethod
    def getProgramacaoEmails():
        return execute("SELECT * FROM email_programado")

    def __repr__(self):
        return '<EmailProgramado %r>' % self.id


class Eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_inicio = db.Column(db.Date)
    hora_inicio = db.Column(db.Time)
    data_fim = db.Column(db.Date)
    hora_fim = db.Column(db.Time)
    descricao = db.Column(db.String(50))
    categoria = db.Column(db.Integer, db.ForeignKey('categoria_eventos.id'))
    funcionario_responsavel = db.Column(db.Integer, db.ForeignKey('funcionario_rh.id'))
    servidor_responsavel = db.Column(db.Integer, db.ForeignKey('servidor.id'))
    id_programacao_email = db.Column(db.Integer, db.ForeignKey('email_programado.id'))
    privacidade = db.Column(db.Integer, db.ForeignKey('privacidade_tipos.id'))

    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
                db.session.commit()
                return self.id
            else:
                funcionario = self.query.get(self.id)
                if funcionario:
                    campos = self.__dict__
                    for campo, valor in campos.items():
                        if campo != 'id' and campo != '_sa_instance_state' and hasattr(funcionario, campo):
                            setattr(funcionario, campo, valor)
                            continue
                    db.session.commit()
                    return self.id
                else:
                    print("Registro não encontrado no banco de dados.")
                    return False
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    @staticmethod
    def getEventos():
        return execute(f"""
            SELECT e.*, fr.nome as nome_funcionario, s.nome as nome_servidor, e.descricao, ce.descricao as title
            FROM eventos e 
            LEFT JOIN funcionario_rh fr ON e.funcionario_responsavel = fr.id 
            LEFT JOIN servidor s ON e.servidor_responsavel = s.id 
            LEFT JOIN categoria_eventos ce ON e.categoria = ce.id
            WHERE (e.funcionario_responsavel = :user_id OR e.privacidade = 1) AND e.data_inicio >= now()
            ORDER BY data_inicio ASC
            """, {"user_id": session['user_id']})



class TokenUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('funcionario_rh.id'))
    token = db.Column(db.String(255))
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    action = db.Column(db.String(20))

    def __init__(self, user_id, token, action):
        self.user_id = user_id
        self.token = token
        self.action = action

    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
                db.session.commit()
                return self.id
            else:
                instance = self.query.get(self.id)
                if instance:
                    campos = self.__dict__
                    for campo, valor in campos.items():
                        if campo != 'id' and campo != '_sa_instance_state' and hasattr(instance, campo):
                            setattr(instance, campo, valor)
                            continue
                    db.session.commit()
                    return self.id
                else:
                    print("Registro não encontrado no banco de dados.")
                    return False
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    @staticmethod
    def getFuncionarioToken(token, action):
        return execute(f"""
                    SELECT user.*,
                    TIMESTAMPDIFF (MINUTE, t.timestamp, now()) >= 60 as expirado
                    FROM token_usuario t
                    LEFT JOIN funcionario_rh user ON user.id = t.user_id
                    WHERE t.token = '{token}' AND t.action = '{action}'
                    """)

    @staticmethod
    def createTokenUsuario(email, action):
        user_id = (FuncionarioRH.query.filter_by(email=email).first()).id
        token = generate_token()
        token_usuario = TokenUsuario(user_id=user_id, token=token, action=action)
        token_usuario.save()
        return token

    def __repr__(self):
        return '<TokenUsuario %r>' % self.id

class Registros(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(100))
    destinatario = db.Column(db.Integer, db.ForeignKey('servidor.id'))
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    servidor = db.relationship('Servidor', backref=db.backref('registros', lazy=True))

    def __init__(self, descricao, destinatario, data_envio=None):
        self.descricao = descricao
        self.destinatario = destinatario
        if data_envio is None:
            data_envio = datetime.utcnow()
        self.data_envio = data_envio

    def save(self):
        self.senha = generate_password_hash(self.senha)
        try:
            if self.id is None:
                db.session.add(self)
                db.session.commit()
                return self.id
            else:
                funcionario = self.query.get(self.id)
                if funcionario:
                    campos = self.__dict__
                    for campo, valor in campos.items():
                        if campo != 'id' and campo != '_sa_instance_state' and hasattr(funcionario, campo):
                            setattr(funcionario, campo, valor)
                            continue
                    db.session.commit()
                    return self.id
                else:
                    print("Registro não encontrado no banco de dados.")
                    return False
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    @staticmethod
    def getRegistros():
        return execute("SELECT r.*, s.nome, s.email FROM registros r LEFT JOIN servidor s ON s.id = r.destinatario")
    def __repr__(self):
        return f"Registro(id={self.id}, descricao={self.descricao}, destinatario={self.destinatario}, data_envio={self.data_envio})"

class Arquivos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arquivo = db.Column(db.LargeBinary)
    nome = db.Column(db.String(20))
    tipo = db.Column(db.String(10))
    tamanho = db.Column(db.Float)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow)
    privacidade = db.Column(db.Integer, db.ForeignKey('privacidade_tipos.id'))
    inserido_por = db.Column(db.Integer, db.ForeignKey('funcionario_rh.id'))
    funcionario_rh = db.relationship('FuncionarioRH', backref=db.backref('arquivos', lazy=True))

    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    @staticmethod
    def getArquivos():
        return execute(f"""
            SELECT a.*, f.nome as responsavel, f.email 
            FROM arquivos a 
            LEFT JOIN funcionario_rh f ON f.id = a.inserido_por
            WHERE a.inserido_por = :user_id OR a.privacidade > 0
            """, {"user_id": session['user_id']})

    def __repr__(self):
        return f"Arquivo(id={self.id}, nome={self.nome}, tipo={self.tipo}, inserido_por={self.inserido_por})"

class CategoriaEventos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(30))
    arquivo_base_envio = db.Column(db.LargeBinary)
    cor_base = db.Column(db.String(15))
    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    @staticmethod
    def getCategoriaEventos():
        return execute("SELECT * FROM categoria_eventos")

class PrivacidadeTipos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(30))

    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print(e)
            db.session.rollback()
            return None

    @staticmethod
    def getPrivacidadeTipos():
        return execute("SELECT * FROM privacidade_tipos")

