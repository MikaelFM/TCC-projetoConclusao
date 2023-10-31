from sqlalchemy.orm import aliased

from app import db
from sqlalchemy import ForeignKey, text
from app.functions import execute, empty, generate_token

class FuncionarioRH(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30))
    email = db.Column(db.String(20))
    telefone = db.Column(db.Integer)
    cpf = db.Column(db.Integer)
    senha = db.Column(db.String(10))
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
        funcionario = self.query.filter_by(email=self.email, senha=self.senha).first()
        if not empty(funcionario):
            return funcionario
        else:
            return False
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

    def __repr__(self):
        return '<FuncionarioRH %r>' % self.id


class TiposServidores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(30))
    meses_para_progressao = db.Column(db.Integer)

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

    def __repr__(self):
        return '<Servidor %r>' % self.id




class EmailProgramado(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_destinatario = db.Column(db.String(20))
    data_hora_envio = db.Column(db.DateTime)

    def __init__(self, email_destinatario, data_hora_envio):
        self.email_destinatario = email_destinatario
        self.data_hora_envio = data_hora_envio

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

    def __repr__(self):
        return '<Eventos %r>' % self.id


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
