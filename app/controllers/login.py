from app.models import TokenUsuario, FuncionarioRH, Servidor
import app.functions.email as _email
from app.functions import custom_render_template as render_template
from flask import session
def login(email, senha, remember):
    funcionario = (FuncionarioRH(login_padrao=email, senha_padrao=senha)).exists()
    if funcionario:
        session.permanent = False
        if remember == 'true':
            session.permanent = True
        session['user_id'] = funcionario.id
        return {'success': True, 'msg': '', 'confirmarEmail': False}
    else:
        servidor = (Servidor(email=email, cpf=senha)).exists()
        if servidor:
            if servidor.email_confirmado == 1:
                session.permanent = False
                if remember == 'true':
                    session.permanent = True
                session['user_id'] = funcionario.id
                return {'success': True, 'msg': '', 'confirmarEmail': False}
            else:
                return {'success': True, 'msg': '', 'confirmarEmail': True}
        else:
            return {'success': False, 'msg': 'Usuário e/ou senha incorretos'}

def makeEmailConfirmation(email):
    try:
        token = TokenUsuario.createTokenUsuario(email, 'tokenUser')
        _email.send(email, 'Código de Confirmação',
                    f"Clique para confirmar seu e-mail: http://127.0.0.1:5000/confirmation/{token}")
        return {'success': True, 'msg': 'Enviado com sucesso'}
    except Exception as e:
        return {'success': False, 'msg': str(e)}


def confirmEmail(token):
    type = "email"
    tokenUser = TokenUsuario.getFuncionarioToken(token)
    if len(tokenUser) == 0: # inválido
        return render_template("return_token.html", type=type, response="invalid")
    else:
        if tokenUser[0]['expirado'] == 1: # expirado
            return render_template("confirmation.html", token="expirado")
        elif tokenUser[0]['email_confirmado'] == 1: # em uso
            return render_template("return_token.html")
        elif tokenUser[0]['email_confirmado'] == 0: # sucesso
            servidor = Servidor(id=tokenUser[0]['id'], email_confirmado=True)
            servidor.save()
            servidor.deleteConfirmations()
            return render_template("return_token.html")
        else:
            print("Ocorreu algum erro")
            return render_template("return_token.html", type=type, response="invalid")

def checkEmailExists(email):
    funcionario = FuncionarioRH(email=email)
    return {'exists':funcionario.emailExists()}