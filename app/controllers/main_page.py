from flask import session
from app.models import *


def getDados():
    type = session['type']

    dados = {
        'tipo': type,
        'arquivos': Arquivos.getArquivos(type),
        'eventos': Eventos.getEventos(type),
        'tiposPrivacidade': PrivacidadeTipos.getPrivacidadeTipos()
    }

    if type == 'funcionario':
        dados['registros'] = EmailProgramado.getRegistros()
        dados['servidores'] = Servidor.getServidores()
        dados['tipoServidores'] = TiposServidores.getTipoServidores()
    else:
        dados['nome'] = Servidor(id=session['user_id']).get_nome_by_id()
        dados['notifications'] = Eventos.getNotifications()

        return dados
