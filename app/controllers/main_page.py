from flask import session
from app.models import *

def getDados():
    dados = {}
    user_id = session['user_id']
    user = get_user(user_id)
    registros = Registros.getRegistros()
    arquivos = Arquivos.getArquivos()
    servidores = Servidor.getServidores()
    eventos = Eventos.getEventos()
    tipoServidores = TiposServidores.getTipoServidores()
    return {
        'nome': user['nome'],
        'registros': registros,
        'arquivos': arquivos,
        'servidores': servidores,
        'eventos': eventos,
        'tipoServidores': tipoServidores
    }