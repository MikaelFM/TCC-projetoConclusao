from datetime import datetime

from sqlalchemy.orm import aliased

from app import db, login_manager, scheduler
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
    login_padrao = db.Column(db.String(258))
    senha_padrao = db.Column(db.String(110))
    def deleteConfirmations(self):
        return execute(f"""DELETE FROM teste.token_usuario WHERE user_id = {self.id} AND action = 'tokenUser'""")

    def emailExists(self):
        funcionario = self.query.filter_by(email=self.email).first()
        return not empty(funcionario)

    def exists(self):
        funcionario = self.query.filter_by(login_padrao=self.login_padrao).first()
        if funcionario is None:
            return False
        senha_correta = check_password_hash(funcionario.senha_padrao, self.senha_padrao)
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
    nome = db.Column(db.String(85))
    email = db.Column(db.String(256))
    telefone = db.Column(db.String(11))
    cpf = db.Column(db.String(11))
    data_admissao = db.Column(db.DateTime)
    data_criacao = db.Column(db.DateTime)
    cargo = db.Column(db.String(40))
    foto = db.Column(db.Text)
    id_tipo = db.Column(db.Integer, ForeignKey('tipos_servidores.id'))
    email_confirmado = db.Column(db.Boolean, default=False)


    @staticmethod
    def getServidores():
        return execute("SELECT s.* FROM servidor s")

    def getRepetido(self):
        repetidos = []
        id = self.id if self.id is not None else 0
        dados = execute(f"""
            SELECT 
                cpf = '{self.cpf}' as 'CPF',
                telefone = '{self.telefone}' as 'Telefone',
                email = '{self.email}' as 'E-mail'
            FROM teste.servidor 
            WHERE 
                (
                    cpf = '{self.cpf}' or 
                    telefone = '{self.telefone}' or 
                    email = '{self.email}'
                )   and 
                id != {id}
                """)
        if not empty(dados):
            for key, value in (dados[0]).items():
                if value == 1:
                    repetidos.append(key)
        return repetidos
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

    def exists(self):
        funcionario = self.query.filter_by(email=self.email, cpf=self.cpf).first()
        if funcionario is None:
            return False
        if not empty(funcionario):
            return funcionario
        else:
            return False

    def __repr__(self):
        return '<Servidor %r>' % self.id


class EmailProgramado(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('servidor.id'))
    data_hora_envio = db.Column(db.DateTime, nullable=True)
    assunto = db.Column(db.String(100), nullable=True)
    texto = db.Column(db.Text, nullable=True)
    enviado = db.Column(db.Boolean, nullable=True)
    evento_vinculado = db.Column(db.Integer, db.ForeignKey('eventos.id'))

    def __init__(self, id, id_destinatario, data_hora_envio, assunto, texto, evento_vinculado, enviado=False):
        self.id = id
        self.id_destinatario = id_destinatario
        self.data_hora_envio = data_hora_envio
        self.assunto = assunto
        self.texto = texto
        self.evento_vinculado = evento_vinculado
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
        return execute(
            "SELECT e.*, s.email as email_destinatario "
            "FROM email_programado e "
            "LEFT JOIN servidor s "
            "ON s.id = e.id_destinatario"
        )

    @staticmethod
    def getRegistros():
        return execute(
            "SELECT e.*, CAST(e.data_hora_envio AS CHAR) as data_hora_envio, s.email as email_destinatario, s.nome as nome_destinatario, ev.descricao "
            "FROM email_programado e "
            "LEFT JOIN servidor s ON s.id = e.id_destinatario "
            "LEFT JOIN eventos ev ON ev.id = e.evento_vinculado "
            "WHERE enviado = 1"
        )

    def __repr__(self):
        return '<EmailProgramado %r>' % self.id


class Eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date)
    descricao = db.Column(db.String(50))
    categoria = db.Column(db.Integer, db.ForeignKey('categoria_eventos.id'))
    servidor_responsavel = db.Column(db.Integer, db.ForeignKey('servidor.id'))
    privacidade = db.Column(db.Integer, db.ForeignKey('privacidade_tipos.id'))

    def __init__(self, id, data, descricao, categoria, funcionario_responsavel, servidor_responsavel, privacidade):
        self.id = id
        self.data = data
        self.descricao = descricao
        self.categoria = categoria
        self.funcionario_responsavel = funcionario_responsavel
        self.servidor_responsavel = servidor_responsavel
        self.privacidade = privacidade

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
    def getEventos():
        return execute(f"""
            SELECT e.*, s.nome as nome_servidor, e.descricao, ce.descricao as title,
            CONCAT(CAST(e.data AS CHAR), ' 00:00') as data,
            (SELECT COALESCE((count(*) > 0), 0) FROM email_programado WHERE evento_vinculado = e.id) as has_vinculo
            FROM eventos e 
            LEFT JOIN servidor s ON e.servidor_responsavel = s.id 
            LEFT JOIN categoria_eventos ce ON e.categoria = ce.id
            WHERE (e.servidor_responsavel = :user_id OR e.privacidade = 1)
            ORDER BY data ASC
            """, {"user_id": session['user_id']})



class TokenUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('servidor.id'))
    token = db.Column(db.String(255))
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token
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
    def getFuncionarioToken(token):
        return execute(f"""
                    SELECT user.*,
                    TIMESTAMPDIFF (MINUTE, t.timestamp, now()) >= 60 as expirado
                    FROM token_usuario t
                    LEFT JOIN servidor user ON user.id = t.user_id
                    WHERE t.token = '{token}'
                    """)

    @staticmethod
    def createTokenUsuario(email, action):
        user_id = (Servidor.query.filter_by(email=email).first()).id
        token = generate_token()
        token_usuario = TokenUsuario(user_id=user_id, token=token)
        token_usuario.save()
        return token

    def __repr__(self):
        return '<TokenUsuario %r>' % self.id

class Arquivos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arquivo = db.Column(db.LargeBinary)
    nome = db.Column(db.String(20))
    tipo = db.Column(db.String(10))
    tamanho = db.Column(db.Float)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now)
    inserido_por = db.Column(db.Integer, db.ForeignKey('servidor.id'))

    def __init__(self, id, nome, arquivo, tipo, tamanho, inserido_por):
        self.id = id
        self.nome = nome
        self.arquivo = arquivo
        self.tipo = tipo
        self.tamanho = tamanho
        self.inserido_por = inserido_por

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
    def getArquivos():
        return execute(f"""
            SELECT a.*, CAST(arquivo AS CHAR) AS arquivo, CAST(data_atualizacao AS CHAR) AS data_atualizacao
            FROM arquivos a 
            LEFT JOIN servidor s ON s.id = a.inserido_por
            WHERE a.inserido_por IS NULL
            """, {"user_id": session['user_id']})

    def __repr__(self):
        return f"Arquivo(id={self.id}, nome={self.nome}, tipo={self.tipo}, inserido_por={self.inserido_por})"

class CategoriaEventos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(30))
    arquivo_base_envio = db.Column(db.LargeBinary)
    texto_envio = db.Text()
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
    def getPrivacidadeTipos():
        return execute("SELECT * FROM privacidade_tipos")


class ServidorEvento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('eventos.id'))
    id_servidor = db.Column(db.Integer, db.ForeignKey('servidor.id'))

    def __init__(self, id, id_evento, id_servidor):
        self.id = id
        self.id_evento = id_evento
        self.id_servidor = id_servidor

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